from telegram.ext import Updater

from config import config as cfg
from utils.process_utils import DaemonProcess


class UpdaterProcess(DaemonProcess):
    def __init__(self, updates_queue):
        super(UpdaterProcess, self).__init__(name="updater_process")
        self.updates_queue = updates_queue
        self.updater = Updater(cfg.telegram_token, use_context=True)

    def target(self):
        while True:
            item = self.updates_queue.get()
            if len(item["new_items"]) > 0:
                print("New items: ", item["url"], item["key"], item["time"], item["new_items"])
            if len(item["updated_items"]) > 0:
                print("Updated items: ", item["url"], item["key"], item["time"], item["updated_items"])
