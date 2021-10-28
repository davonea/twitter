# -*- coding:utf-8 -*-
import logging
import os
import os.path
import time
import sys

from framework.modules.bases.service_config import GET_CONF_EX, GET_CONF
from framework.modules.bases.singleton import singleton

initialized = False
formatter = logging.Formatter('%(asctime)s %(levelname)s %(process)d [%(filename)s:%(lineno)d %(funcName)s]: %(message)s')

@singleton
class Configer():
    def __init__(self):
        self.__log_path = ""
        self.__file_handler = None
        self.__console_handler = None
        self.__pure_path = "" 
        self.__time_format = "%Y%m%d%H%M"
        self.__time_format = "%Y%m%d"

    def set_file_handler(self):
        date_str = time.strftime(self.__time_format)
        self.__log_path = self.__pure_path + '.' + date_str

        fh = logging.FileHandler(self.__log_path)
        fh.setFormatter(formatter)
        self.__file_handler = fh
        logging.getLogger('').addHandler(fh)

    def set_console_handler(self):
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG)
        console.setFormatter(formatter)
        self.__console_handler = console
        logging.getLogger('').addHandler(console)
        logging.getLogger('').setLevel(logging.INFO)

    def del_console_handler(self):
        logging.getLogger('').removeHandler(self.__console_handler)
        del self.__console_handler
        self.__console_handler = None

    def del_file_handler(self):
        logging.getLogger('').removeHandler(self.__file_handler)
        del self.__file_handler
        self.__file_handler = None

    def rotate(self):
        date_str = time.strftime(self.__time_format)
        path = self.__pure_path + '.' + date_str

        if path == self.__log_path:
            return
        sys.stdout.flush()
        sys.stderr.flush()
        self.del_file_handler()
        self.set_file_handler()

    def init(self, level, path="./log.txt", quiet=False):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        self.__pure_path = path
        if quiet:
            self.del_console_handler()

        if not quiet and not self.__console_handler:
            self.set_console_handler()
        self.set_file_handler()


        cmd = str("logging.getLogger("").setLevel(logging.%s)" % (level.upper()))
        exec(cmd)


class Logger():
    def __init__(self):
        self.info = logging.info
        self.debug = logging.debug
        self.warning = logging.warning
        self.error = logging.error
        self.critical = logging.critical
        Configer().set_console_handler()


def log_init(level, path=GET_CONF_EX("log", "log_dir_common", "log_dir_common"), quiet=True):
    Configer().del_file_handler()
    Configer().init(level, path, quiet)


g_logger = Logger()


def logger():
    Configer().rotate()
    return g_logger

def log(log_name):
    def decorator(func):
        def wrapper(*args, **kw):
            quiet = False
            if log_name == 'pachong':
                quiet = True
            if log_name == 'fanyi':
                quiet = True
            log_init(GET_CONF('log', 'log_level'), GET_CONF_EX('log', 'log_dir_' + log_name, os.path.join(GET_CONF('log', 'log_dir_'), log_name)),
                     quiet = quiet)
            return func(*args, **kw)
        return wrapper
    return decorator

if __name__ == '__main__':
    log_init('info', quiet=False)

    while True:
        l = logger()
        l.info('abc')
        time.sleep(1)
