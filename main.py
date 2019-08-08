import logging
import multiprocessing
import os
import time

from config import config as cfg
from processes import UserProcess, UpdaterProcess
from utils.process_utils import start_process, check_processes


def main():
    os.makedirs(cfg.data_folder, exist_ok=True)
    processes = []
    updates_queue = multiprocessing.Queue()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    updater_process = lambda: UpdaterProcess(updates_queue=updates_queue)
    processes += [start_process(updater_process)]

    for key in cfg.users.keys():
        resources = cfg.users[key]
        starter = lambda: UserProcess(user_id=key, resources=resources, updates_queue=updates_queue, timeout=cfg.poll_timeout)
        processes += [start_process(starter)]

    while True:
        time.sleep(cfg.error_timeout)
        processes = check_processes(processes)


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    main()
