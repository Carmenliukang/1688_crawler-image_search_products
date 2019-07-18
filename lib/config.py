# !/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019-04-02 16:07
# @Author  : liukang.hero
# @FileName: config.py

import os
import configparser


class config(object):
    def __init__(self, filename='../conf/config.conf'):
        self.config = configparser.ConfigParser()
        fp = open(os.path.join(os.path.dirname(__file__), filename))
        self.config.read_file(fp)
        fp.close()

    def setting(self):
        self.setting = {}
        for item in self.config.sections():
            self.setting[item] = self.get_conf(item)
        return self.setting

    def get_conf(self, section):
        setting = {}
        for k, v in self.config.items(section):
            setting[k] = v
        return setting


setting = config().setting()
