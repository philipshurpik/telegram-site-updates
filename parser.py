import logging
import os
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
        self.dict_path = os.path.join(cfg.data_folder, f"{key}_{get_hash(url)}.npy")
        self.state_dict = self.load_state()

    def target(self):
        while True:
            items = self.parse(self.key, self.url)
            if not self.state_dict:
                self.state_dict = self.init_state_dict(items)
                self.save_state()
                print(f"Parser {self.name}, initialized with: {len(items)} items")
            else:
                new_items, updated_items = self.update_state_dict(items)
                if len(new_items) > 0 or len(updated_items) > 0:
                    self.save_state()
                    self.updates_queue.put({"name": self.name, "key": self.key, "url": self.url,
                                            "time": time.time(), "new_items": new_items, "updated_items": updated_items})
                    print(f"Parser {self.name}, new: {len(new_items)} items, updated: {len(updated_items)} items")
            time.sleep(self.timeout)

    def load_state(self):
        state_dict = np.load(self.dict_path, allow_pickle=True).item() if os.path.exists(self.dict_path) else {}
        print(f"State dict loaded for parser {self.name}, state items count: {len(state_dict)}") \
            if state_dict else print(f"State dict empty for parser {self.name}")
        return state_dict

    def save_state(self):
        np.save(self.dict_path, self.state_dict, allow_pickle=True)

    def init_state_dict(self, items):
        state_dict = {}
        for item in items:
            combined_key = "_".join([item[key] for key in self.tracked_keys])
            state_dict[combined_key] = item
        return state_dict

    def update_state_dict(self, items):
        new_items = []
        updated_items = []

        for item in items:
            combined_key = "_".join([item[key] for key in self.tracked_keys])
            if combined_key not in self.state_dict:
                self.state_dict[combined_key] = item
                new_items.append(item)
            elif self.tracked_values is not None and len(self.tracked_values) > 0:
                state_item = self.state_dict[combined_key]
                diff = []
                for tracked_value in self.tracked_values:
                    if item[tracked_value] != state_item[tracked_value]:
                        diff.append({"field": tracked_value, "before": state_item[tracked_value], "after": item[tracked_value]})
                if len(diff) > 0:
                    updated_items.append({"item": item, "diff": diff})
                    self.state_dict[combined_key] = item
        return new_items, updated_items

    @staticmethod
    def parse(key, url):
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code != 200:
                logging.error("Error code: " + str(response.status_code))
                time.sleep(cfg.error_timeout)
                return []
        except Exception as e:
            logging.error(repr(e))
            time.sleep(cfg.error_timeout)
            return []

        soup = BeautifulSoup(response.text, 'lxml')
        items = getters[key](soup)
        return items
