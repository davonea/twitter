#!/usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from framework.modules.bases.singleton import *
import os
import time
import sys

conf_file = ""


@singleton
class __ServiceManager():
    def __init__(self):
        self.conf_file = conf_file
        self.load()

    def load(self):
        self.cf = configparser.ConfigParser()
        self.cf.read(self.conf_file)
        self.mtime = os.path.getmtime(self.conf_file)
        sys.stderr.write('load conf file at [%s]\n' % time.ctime(time.time()))

    def reload(self):
        if self.mtime != os.path.getmtime(self.conf_file):
            self.load()

    def get_ex(self, name, key, dft_val):
        self.reload()
        try:
            return self.cf.get(name, key)
        except Exception as e:
            return dft_val

    def get(self, name, key):
        self.reload()
        return self.cf.get(name, key)

    def has(self, name, key):
        return self.cf.has_option(name, key)

    def get_sections(self):
        return self.cf.sections()

    def get_options(self, section):
        return self.cf.options(section)


def GET_SECTIONS():
    manager = __ServiceManager()
    return manager.get_sections()

def GET_OPTIONS(section):
    manager = __ServiceManager()
    return manager.get_options(section)

def GET_CONF_EX(name, key, dft_val):
    manager = __ServiceManager()
    return manager.get_ex(name, key, dft_val)


def GET_CONF(name, key):
    manager = __ServiceManager()
    return manager.get(name, key)


def HAS_CONF(name, key):
    manager = __ServiceManager()
    return manager.has(name, key)


def main():
    pass


if __name__ == '__main__':
    main()
