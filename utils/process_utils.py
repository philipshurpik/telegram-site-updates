import logging
import multiprocessing


class DaemonProcess(multiprocessing.Process):
    def __init__(self, name, *args, **kwargs):
        multiprocessing.Process.__init__(self, *args, **kwargs)
        self.daemon = True
        self.name = name

    def target(self):
        raise Exception("need to be implemented in child process")

    def run(self):
        try:
            self.target()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            logging.error(f"Error in process: {e}", exc_info=True, stack_info=True)


def start_process(starter):
    p = starter()
    p.start()
    return p, starter


def check_processes(processes):
    return [_check_process(*proc) for proc in processes]


def _check_process(process, starter):
    if process.is_alive():
        return process, starter
    else:
        logging.error(f"Something wrong with process {process.name}, restarting")
        return start_process(starter)
