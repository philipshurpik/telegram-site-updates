import os
import sys
import time

import numpy as np
import requests
from bs4 import BeautifulSoup

from config import config as cfg
from resources import getters, tracked_fields
from utils.hash_utils import get_hash
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
        self.tracked_values = tracked_fields[key]["values"]
        self.dict_path = os.path.join(cfg.data_folder, f"{key}_{get_hash(url)}.dat")
        self.state_dict = self.load_state()

    def load_state(self):
        return np.load(self.dict_path, allow_pickle=True).item() if os.path.exists(self.dict_path) else {}

    def target(self):
        while True:
            items = self.parse(self.key, self.url)
            if not self.state_dict:
                self.state_dict = self.init_state_dict(items)
            else:
                dict_diff = self.check_item_updates(items)
                if dict_diff:
                    self.updates_queue.put({"name": self.name, "key": self.key, "url": self.url,
                                            "time": time.time(), "update": dict_diff})

            print(f"Parser {self.name}, initialized with: {len(items)} items")
            time.sleep(self.timeout)

    def init_state_dict(self, items):
        state_dict = {}
        for item in items:
            combined_key = "_".join([item[key] for key in self.tracked_keys])
            state_dict[combined_key] = item
        return state_dict

    def check_item_updates(self, items):

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
