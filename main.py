import sys

import requests
from bs4 import BeautifulSoup

from config import config
from resources import getters


def start(key, url):
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    except Exception as e:
        print(repr(e))
        sys.exit(1)

    if response.status_code != 200:
        print("Non success status code returned " + str(response.status_code))
        sys.exit(1)

    soup = BeautifulSoup(response.text, 'lxml')

    flats = getters[key](soup)
    print(flats)


def main():
    for key in config.keys():
        for url in config[key]:
            start(key, url)


if __name__ == '__main__':
    main()
