import sys
import time

import requests
from bs4 import BeautifulSoup

from resources import getters
from utils.process_utils import DaemonProcess


class Parser(DaemonProcess):
    def __init__(self, name, updates_queue, key, url, timeout):
        super(Parser, self).__init__(name=name)
        self.name = name
        self.updates_queue = updates_queue
        self.key = key
        self.url = url
        self.timeout = timeout

    def target(self):
        while True:
            items = self.parse(self.key, self.url)
            print(f"Parser {self.name}, initialized with: {len(items)} items")
            time.sleep(self.timeout)

    @staticmethod
    def parse(key, url):
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        except Exception as e:
            print(repr(e))
            sys.exit(1)

        if response.status_code != 200:
            print("Error code: " + str(response.status_code))
            sys.exit(1)

        soup = BeautifulSoup(response.text, 'lxml')
        items = getters[key](soup)
        return items
