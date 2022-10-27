import logging
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

logger = logging.getLogger(__name__)


class UntisWebscraper:
    def __init__(self, driverPath, debug=False):
        self.debug = debug

        options = webdriver.ChromeOptions()
        if not debug:
            # options.add_argument('--incognito')
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-crash-reporter")
            options.add_argument("--disable-extensions")
            options.add_argument("--disable-in-process-stack-traces")
            options.add_argument("--disable-logging")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--log-level=3")
            options.add_argument("--output=/dev/null")

        self.driver = webdriver.Chrome(driverPath, options=options)

    def get_class_information(self, url, auth_cookies):
        logger.info('getting class informationLoading HTML from: ' + url)

        self.driver.get(url)

        cookies = [{
            'name': 'JSESSIONID',
            'value': auth_cookies['JSESSIONID']
        }, {
            'name': 'schoolname',
            'value': auth_cookies['schoolname']
        }]

        for cookie in cookies:
            self.driver.add_cookie(cookie)

        # wait until iframe loaded
        WebDriverWait(self.driver, 15).until(EC.frame_to_be_available_and_switch_to_it(
            (By.CSS_SELECTOR, '#embedded-webuntis')))

        # wait until contents of iframe loaded
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'grupetScrollContainer')))

        # there are some random a tags on the page, so we have to filter rist
        unfiltered_tags = self.driver.find_elements(by=By.TAG_NAME, value='a')

        # all 'a' tags we are interested in start with our url
        links_to_lesson_dialog = [tag.get_attribute('href') for tag in unfiltered_tags if tag.get_attribute(
            'href').startswith(url)]

        results = {}

        for link in links_to_lesson_dialog:
            self.driver.switch_to.new_window('tab')

            self.driver.get(link)
            logger.info('Loading teaching content from: ' + link)
            try:
                WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.TAG_NAME, 'textarea'))
                )
            except:
                self._close_tab_and_go_to_first()
                continue

            teaching_content = self.driver.find_element(
                by=By.TAG_NAME, value='textarea').get_attribute('value')

            # the lesson name is stored pretty randomly
            lesson_name = self.driver.find_element(by=By.CLASS_NAME, value='text-container').find_elements(
                by=By.CLASS_NAME, value='element')[-1].get_attribute('textContent')

            if not lesson_name in results:
                results[lesson_name] = [teaching_content]
            else:
                items = teaching_content.split('\n')
                for item in items:
                    results[lesson_name].append(item)
            # close the dialog
            self._close_tab_and_go_to_first()

        self.driver.quit()

        return results

    def _close_tab_and_go_to_first(self):
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])
