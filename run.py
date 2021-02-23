#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.alibaba_lib import Alibaba

if __name__ == '__main__':
    filename = 'data/下载.jpeg'
    cookie = """请填写登入成功的cookie"""
    url = Alibaba(cookie).run(filename)
    print(url)
