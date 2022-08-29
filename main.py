import configparser
from re import M

import requests
from bs4 import BeautifulSoup

import utils

CONFIG_WEBUNTIS_SECTION_NAME = 'WEBUNTIS'


def main():

    config = read_config()

    if (config is None):
        print('No config found')
        return

    login_result = login(config['username'], config['password'],
                         config['school'], config['securityUrl'])

    if login_result.status_code == 200:
        print('Login successful')
    else:
        print('Login failed')
        return

    doc = load_html(config['timetableUrl'], login_result.cookies)

    print(doc)


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


def load_html(url, cookies_m):
    print('Loading HTML from: ' + url)
    print(cookies_m)

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
    }

    cookies = {
        'JSESSIONID': cookies_m['JSESSIONID'],
        'schoolname': cookies_m['schoolname'],
    }
    print(cookies)

    result = requests.get(url, cookies=cookies, headers=headers)
    doc = BeautifulSoup(result.text, 'html.parser')

    return doc


def login(username, password, school_name, security_url):
    print('Logging in as: ' + username)
    headers = {
        'Accept': 'application/json'
    }

    data = {
        'school': school_name,
        'j_username': username,
        'j_password': password,
        'token': '',
    }

    result = requests.post(security_url, headers=headers, data=data)
    return result


main()
