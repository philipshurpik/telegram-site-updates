from telegram.ext import Updater

from config import config as cfg
from resources import templates_new
from utils.process_utils import DaemonProcess


class UpdaterProcess(DaemonProcess):
    def __init__(self, updates_queue):
        super(UpdaterProcess, self).__init__(name="UpdaterProcess")
        self.updates_queue = updates_queue
        self.updater = None

    def target(self):
        print("updater started")
        self.updater = Updater(cfg.telegram_token, use_context=True)

        while True:
            item = self.updates_queue.get()
            if len(item["new_items"]) > 0:
                key = item['key']
                for new_item in item["new_items"]:
                    self.updater.bot.send_message(chat_id=list(cfg.users.keys())[0], text=templates_new[key](new_item))
            if len(item["updated_items"]) > 0:
                print("Updated items: ", item["url"], item["key"], item["time"], item["updated_items"])
