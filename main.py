import configparser
from datetime import date

import requests
from bs4 import BeautifulSoup

import utils
from webscraper import UntisWebscraper

CONFIG_WEBUNTIS_SECTION_NAME = 'WEBUNTIS'
DEBUG = True


def main():

    web_scraper = UntisWebscraper(DEBUG)

    config = read_config()

    if (config is None):
        print('No config found')
        return

    login_result = login(config['username'], config['password'],
                         config['school'], config['securityUrl'])

    if login_result.status_code == 200:
        print('Login successful')
    else:
        print('Login failed', login_result)
        return

    information = web_scraper.get_class_information(
        config['timetableUrl'], login_result.cookies)

    filename = date.today().strftime('%d_%m_%Y') + '.txt'

    with open('result/' + filename, 'w') as f:
        f.write(format_school_info(information))


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.sections()

    if not config.has_section(CONFIG_WEBUNTIS_SECTION_NAME):
        return None

    return {
        'username': config[CONFIG_WEBUNTIS_SECTION_NAME]['Username'],
        'password': utils.b64ToString(config[CONFIG_WEBUNTIS_SECTION_NAME]['PasswordB64']),
        'school': config[CONFIG_WEBUNTIS_SECTION_NAME]['SchoolName'],
        'securityUrl': config[CONFIG_WEBUNTIS_SECTION_NAME]['SecurityUrl'],
        'timetableUrl': config[CONFIG_WEBUNTIS_SECTION_NAME]['TimetableUrl'],
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
    output = ''
    for key, value in information.items():
        output += key + '\n'
        for item in set(value):
            for content in item.split('\n'):
                output += '\t' + content.strip() + '\n'
    return output


main()
