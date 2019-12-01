#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.jd_lib import JD
from lib.taobao_lib import TaoBao
from lib.alibaba_lib import Alibaba

if __name__ == '__main__':
    filename = 'data/测试图片.jpg'

    url = Alibaba().run(filename)
    print(url)

    url = TaoBao().run(filename)
    print(url)

    url = JD().run(filename)
    print(url)
