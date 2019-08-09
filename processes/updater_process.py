from telegram.ext import Updater

from config import config as cfg
from resources import templates_new, templates_update
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
            key = item['key']
            if len(item["new_items"]) > 0:
                for new_item in item["new_items"]:
                    self.updater.bot.send_message(
                        chat_id=list(cfg.users.keys())[0],
                        text=templates_new[key](new_item),
                        parse_mode='HTML'
                    )
            if len(item["updated_items"]) > 0 and key in templates_update:
                for upd_item in item["updated_items"]:
                    data = upd_item["data"]
                    diff = upd_item["diff"]
                    self.updater.bot.send_message(
                        chat_id=list(cfg.users.keys())[0],
                        text=templates_update[key](data, diff),
                        parse_mode='HTML'
                    )
