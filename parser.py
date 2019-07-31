import hashlib
import os
import sys
import time

import numpy as np
import requests
from bs4 import BeautifulSoup

from config import config as cfg
from resources import getters, tracked_fields
from utils.process_utils import DaemonProcess


class Parser(DaemonProcess):
    def __init__(self, name, updates_queue, key, url, timeout):
        super(Parser, self).__init__(name=name)
        self.name = name
        self.updates_queue = updates_queue
        self.key = key
        self.url = url
        self.timeout = timeout
        self.tracked_keys = tracked_fields[key]["keys"]
        self.combined_key = "_".join(self.tracked_keys)
        self.tracked_value = tracked_fields[key]["value"]
        self.dict_path = os.path.join(cfg.data_folder, f"{key}_{hashlib.md5(url.encode()).hexdigest()}.dat")
        self.state_dict = self.load_state()

    def load_state(self):
        return np.load(self.dict_path, allow_pickle=True).item() if os.path.exists(self.dict_path) else {}

    def target(self):
        while True:
            items = self.parse(self.key, self.url)
            if not self.state_dict:
                self.state_dict = self.init_state_dict(items)

            print(f"Parser {self.name}, initialized with: {len(items)} items")
            time.sleep(self.timeout)

    def init_state_dict(self, items):

        return {}

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
