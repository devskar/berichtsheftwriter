import configparser
from datetime import date

import requests
from bs4 import BeautifulSoup

import utils
import webhook
from webscraper import UntisWebscraper

CONFIG_WEBUNTIS_SECTION_NAME = 'WEBUNTIS'
CONFIG_WEBHOOK_SECTION_NAME = 'WEBHOOK'
DEBUG = True


def main():

    # web_scraper = UntisWebscraper(DEBUG)

    config = read_config()

    if (config is None):
        print('No config found')
        return

    # login_result = login(config['webuntisUsername'], config['webuntisPassword'],
    #                      config['webuntisSchool'], config['webuntisSecurityUrl'])

    # if login_result.status_code == 200:
    #     print('Login successful')
    # else:
    #     print('Login failed', login_result)
    #     return

    # information = web_scraper.get_class_information(
    #     config['webuntisTimetableUrl'], login_result.cookies)
    # output = format_school_info(information)

    # if not output == '':
    #     # write result to file
    #     filepath = 'result/' + date.today().strftime('%d_%m_%Y') + '.txt'
    #     with open(filepath, 'w', encoding='utf-8') as f:
    #         f.write(output)

    # 'https://discord.com/api/webhooks/1033064718140723292/tNsjnRyjgp22kcaWh-lOx9WtD5lhIAY5qP6FAYrOYuOxvyMVhavQilGiX8hvdFHxm9Pk'

    webhook.send_file_to_webhook(
        config['webhookUrl'], 'result/23_10_2022.txt')


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()

    if not config.has_section(CONFIG_WEBUNTIS_SECTION_NAME):
        return None

    return {
        'webuntisUsername': config[CONFIG_WEBUNTIS_SECTION_NAME]['Username'],
        'webuntisPassword': utils.b64_to_string(config[CONFIG_WEBUNTIS_SECTION_NAME]['PasswordB64']),
        'webuntisSchool': config[CONFIG_WEBUNTIS_SECTION_NAME]['SchoolName'],
        'webuntisSecurityUrl': config[CONFIG_WEBUNTIS_SECTION_NAME]['SecurityUrl'],
        'webuntisTimetableUrl': config[CONFIG_WEBUNTIS_SECTION_NAME]['TimetableUrl'],
        'webhookUrl': config[CONFIG_WEBHOOK_SECTION_NAME]['WebhookUrl']
    }


def login(username, password, school_name, security_url):
    print('Logging in as: ' + username)
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
    output = ''
    for key in sorted_keys:
        output += key + '\n'
        all_items = list()

        # get all individual lesson topics
        for item in information[key]:
            all_items = all_items + item.split('\n')
        new_list = list(utils.remove_duplicates_from_list(all_items))

        # remove duplicates and write to string
        for item in new_list:
            output += '\t' + item.strip() + '\n'
    return output


main()
