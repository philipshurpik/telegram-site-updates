from telegram.ext import Updater

from config import config as cfg
from utils.process_utils import DaemonProcess


class UpdaterProcess(DaemonProcess):
    def __init__(self, updates_queue):
        super(UpdaterProcess, self).__init__(name="updater_process")
        self.updates_queue = updates_queue
        self.updater = None

    def target(self):
        self.updater = Updater(cfg.telegram_token, use_context=True)
        self.updater.bot.send_message(chat_id=list(cfg.users.keys())[0], text="Hello world")

        while True:
            item = self.updates_queue.get()
            if len(item["new_items"]) > 0:
                print("New items: ", item["url"], item["key"], item["time"], item["new_items"])
            if len(item["updated_items"]) > 0:
                print("Updated items: ", item["url"], item["key"], item["time"], item["updated_items"])
