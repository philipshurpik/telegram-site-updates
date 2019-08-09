import logging
import os

import numpy as np
import requests
from bs4 import BeautifulSoup

from config import config as cfg
from resources import getters, tracked_fields
from utils.hash_utils import get_hash


class ResourceParser:
    def __init__(self, user_id, key, url, index):
        self.user_id = user_id
        self.key = key
        self.url = url
        self.index = index
        self.name = f"{self.user_id}_{key}_{index}"
        self.tracked_keys = tracked_fields[key]["keys"]
        self.tracked_values = tracked_fields[key]["values"]
        self.dict_path = os.path.join(cfg.data_folder, f"{user_id}_{key}_{get_hash(url)}.npy")
        self.state_dict = self.load_state()

    def check_updates(self):
        new_items, updated_items = [], []
        items = self.parse(self.key, self.url)
        # DEBUG code
        # if len(items) > 0 and 'text' in items[0]:
        #     items[4]['id'] = '0' + items[4]['id']
        if not self.state_dict:
            self.state_dict = self.init_state_dict(items)
            if len(items) > 0:
                self.save_state()
                print(f"ResourceParser {self.name}, initialized with: {len(items)} items")
        else:
            new_items, updated_items = self.update_state_dict(items)
            if len(new_items) > 0 or len(updated_items) > 0:
                self.save_state()
                print(f"ResourceParser {self.name}, new: {len(new_items)} items, updated: {len(updated_items)} items")
        return new_items, updated_items

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
                    updated_items.append({"data": item, "diff": diff})
                    self.state_dict[combined_key] = item
        return new_items, updated_items

    @staticmethod
    def parse(key, url):
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code != 200:
                logging.error("Error code: " + str(response.status_code))
                return []
        except Exception as e:
            logging.error(repr(e))
            return []

        soup = BeautifulSoup(response.text, 'lxml')
        items = getters[key](soup)
        return items
