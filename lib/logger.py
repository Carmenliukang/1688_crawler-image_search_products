# !/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-18 15:04
# @Author  : liukang.hero
# @FileName: logger.py

import os
import time
import logging.handlers
from lib.config import setting


class Log(object):
    def __init__(self, log_conf=setting.get('log', {})):
        self.log_file = log_conf.get('filename', '../log/run.log')
        self.lever = log_conf.get('lever', '20')
        self.logger_handers()

    def logger_handers(self):
        log_file = os.path.join(os.path.dirname(__file__), self.log_file)

        # logging 配置
        handler = logging.handlers.RotatingFileHandler(filename=log_file,
                                                       maxBytes=1024 * 1024,
                                                       backupCount=5,
                                                       encoding='utf-8')  # 实例化handler

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")  # 实例化formatter
        handler.setFormatter(formatter)  # 为handler添加formatter

        self.logger = logging.getLogger('run')  # 获取名为tst的logger
        self.logger.addHandler(handler)  # 为logger添加handler
        # logger.setLevel(logging.INFO)
        self.logger.setLevel(self.lever)


logger = Log().logger
