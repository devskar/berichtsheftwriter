#!/usr/bin/env python

import configparser
import json
import logging
from array import array
from datetime import date

import requests

import utils
from webscraper import UntisWebscraper

CONFIG_FILE_NAME = 'config.ini'
CONFIG_WEBUNTIS_SECTION_NAME = 'WEBUNTIS'
CONFIG_DRIVER_SECTION_NAME = 'DRIVER'
DEBUG = False

CURR_DATE = date.today().strftime('%d_%m_%Y')

logging.basicConfig(
    filename='logs/' + CURR_DATE + '.log',
    format='%(asctime)s %(levelname)s: %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def main():

    config = read_config()

    if (config is None):
        logger.error('No configuration found')
        return

    login_result = login(config['webuntisUsername'], config['webuntisPassword'],
                         config['webuntisSchool'], config['webuntisSecurityUrl'])

    if login_result.status_code == 200:
        logger.info('Login successful')
    else:
        logger.error('Login failed: ' + login_result)
        return 1

    web_scraper = UntisWebscraper(config['chromeDriverPath'], DEBUG)
    information = web_scraper.get_class_information(
        config['webuntisTimetableUrl'], login_result.cookies)
    output = format_school_info(information)

    if not output == '':
        print(output)
        # write result to file
        filepath = 'result/' + CURR_DATE + '.txt'
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output)
            logger.info('Result written to file: ' + filepath)


def read_config():
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)
    config.sections()

    if not config.has_section(CONFIG_WEBUNTIS_SECTION_NAME) and config.has_section(CONFIG_DRIVER_SECTION_NAME):
        return None

    return {
        'webuntisUsername': config[CONFIG_WEBUNTIS_SECTION_NAME]['Username'],
        'webuntisPassword': utils.b64_to_string(config[CONFIG_WEBUNTIS_SECTION_NAME]['PasswordB64']),
        'webuntisSchool': config[CONFIG_WEBUNTIS_SECTION_NAME]['SchoolName'],
        'webuntisSecurityUrl': config[CONFIG_WEBUNTIS_SECTION_NAME]['SecurityUrl'],
        'webuntisTimetableUrl': config[CONFIG_WEBUNTIS_SECTION_NAME]['TimetableUrl'],
        'chromeDriverPath': config[CONFIG_DRIVER_SECTION_NAME]['ChromeWebdriverPath']
    }


def login(username, password, school_name, security_url):
    logger.info('Logging in as: ' + username)
    headers = {
        'Accept': 'application/json'
    }

    data = {
        'school': school_name,
        'j_username': username,
        'j_password': password
    }

    result = requests.post(security_url, headers=headers, data=data)
    return result


def format_school_info(information):
    # sort the keys alphabetically
    sorted_keys = sorted(information.keys(), key=lambda x: x.lower())

    new_dict = {}
    for key in sorted_keys:
        all_items = list()

        # get all individual lesson topics
        for item in information[key]:
            all_items = all_items + item.split('\n')
        new_dict[key] = list(utils.remove_duplicates_from_list(all_items))
    return json.dumps(new_dict, indent=4,  ensure_ascii=False)


if __name__ == '__main__':
    main()
