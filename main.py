import os
import time
from multiprocessing import Queue

from config import config as cfg
from parser import Parser
from utils.process_utils import start_process, check_processes


def main():
    os.makedirs(cfg.data_folder, exist_ok=True)
    processes = []
    updates_queue = Queue()

    for key in cfg.resources.keys():
        item = cfg.resources[key]
        for i, url in enumerate(item):
            starter = lambda: Parser(name=f"{key}_{i}", updates_queue=updates_queue, key=key, url=url, timeout=cfg.poll_timeout)
            processes += [start_process(starter)]

    while True:
        time.sleep(cfg.error_timeout)
        processes = check_processes(processes)


if __name__ == '__main__':
    main()
