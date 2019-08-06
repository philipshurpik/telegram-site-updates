from utils.process_utils import DaemonProcess


class Updater(DaemonProcess):
    def __init__(self, updates_queue):
        super(Updater, self).__init__(name="updater")
        self.updates_queue = updates_queue

    def target(self):
        while True:
            item = self.updates_queue.get()
            if len(item["new_items"]) > 0:
                print("New items: ", item["url"], item["key"], item["time"], item["new_items"])
            if len(item["updated_items"]) > 0:
                print("Updated items: ", item["url"], item["key"], item["time"], item["updated_items"])
