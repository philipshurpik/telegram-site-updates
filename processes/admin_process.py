import time

from config import config as cfg
from utils.process_utils import DaemonProcess


class AdminProcess(DaemonProcess):
    def __init__(self, admin_queue):
        super(AdminProcess, self).__init__(name="AdminProcess")
        self.admin_queue = admin_queue

    def target(self):
        while True:
            time.sleep(cfg.error_timeout)
