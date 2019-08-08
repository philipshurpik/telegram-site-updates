import logging
import time

import numpy as np

from processes.resource_parser import ResourceParser
from utils.process_utils import DaemonProcess


class UserProcess(DaemonProcess):
    def __init__(self, updates_queue, timeout, user_id, resources):
        super(UserProcess, self).__init__(name=f"UserProcess {user_id}")
        self.user_id = user_id
        self.updates_queue = updates_queue
        self.resources = resources
        self.timeout = timeout
        self.parsers = self.init_parsers()
        print(f"User Process loaded for {user_id}")

    def init_parsers(self):
        parsers = []
        for key in self.resources.keys():
            item = self.resources[key]
            for i, url in enumerate(item):
                parsers.append(ResourceParser(name=f"{self.user_id}_{key}_{i}", key=key, url=url))
        return parsers

    def target(self):
        while True:
            for parser in self.parsers:
                self.process_parser(parser)
            time.sleep(self.timeout * np.random.uniform(low=0.8, high=2))

    def process_parser(self, parser):
        try:
            new_items, updated_items = parser.check_updates()
            if len(new_items) > 0 or len(updated_items) > 0:
                self.updates_queue.put({
                    "user_id": self.user_id,
                    "key": parser.key,
                    "url": parser.url,
                    "time": time.time(),
                    "new_items": new_items,
                    "updated_items": updated_items
                })
        except:
            logging.error("Error while checking parser updates: ", exc_info=True)
