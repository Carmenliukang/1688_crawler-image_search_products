#!/usr/bin/env python
# -*- coding: utf-8 -*-


import time
import base64
from lib.func_txy import request_get
from lib.func_txy import request_post
from lib.func_txy import get_random_str


class Alibaba(object):
    """
    1688 PC 端接口获取相似商品的接口
    """

    def __init__(self):
        self.upload_url = 'https://cbusearch.oss-cn-shanghai.aliyuncs.com/'  # 上传图片
        self.sign_url = "https://open-s.1688.com/openservice/ossDataService"  # 获取 sign 加密

        self._headers()

    def _headers(self):
        headres = {
            'Origin': "https://www.1688.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "refer": "https://www.1688.com/"
        }
        self.headers = headres

    def get_key(self):
        '''
            cbuimgsearch/Z5Qja4fXPH1562293605000.jpg 生成规则是 cbuimgsearch/ + 随机10位 + 毫秒级别时间戳
            :return:
            '''
        key = "cbuimgsearch/" + "".join(get_random_str(10)) + str(int(time.time() * 1000))
        return key

    def get_dateset(self):
        '''
        获取加密时间
        :return:
        '''
        url = "https://open-s.1688.com/openservice/.htm?"  # 获取加密时间
        params = {
            "serviceIds": "cbu.searchweb.config.system.currenttime",
            "outfmt": "json",
        }

        status, data = request_get(url, params, self.headers)
        return status, data

    def get_sign(self, data_set):
        '''
        用于获取 sign 用于加密
        :return:
        '''
        url = 'https://open-s.1688.com/openservice/ossDataService'
        appkey = "{};{}".format('pc_tusou', str(data_set))

        params = {
            "appName": "pc_tusou",
            "appKey": base64.b64encode(appkey.encode("utf-8")),
            # 发生变化 pc_tusou;1562288848391 b64 编码 pc_tusou;毫秒级时间戳
        }

        status, data = request_get(url, params, self.headers)

        data = data.get('data', {})

        signature = data.get('signature', '')
        policy = data.get('policy', '')
        accessid = data.get('accessid', '')

        return status, signature, policy, accessid

    def upload_img(self, filename, signature, policy, accessid):
        """
        用于上传图片
        :return:
        """

        url = 'https://cbusearch.oss-cn-shanghai.aliyuncs.com/'
        key = "cbuimgsearch/" + get_random_str(10) + str(int(time.time() * 1000))
        name = get_random_str(5) + ".jpg"

        files = {
            "name": (None, name),
            "key": (None, key),
            "policy": (None, policy),
            "OSSAccessKeyId": (None, accessid),
            "success_action_status": (None, 200),
            "callback": (None, ""),
            "signature": (None, signature),
            "file": (name, open(filename, "rb").read())
        }

        status, res = request_post(url, files=files, headers=self.headers)

        return status, key

    def run(self, filename):
        status, data = self.get_dateset()

        # 这里 采用 str 匹配，因为相比较正则，str replace 更加快
        data_set = data.get('cbu.searchweb.config.system.currenttime', {}).get('dataSet', '')

        # 获取相关的 接口验证参数。同时 获取生成的 图片key
        status, signature, policy, accessid = self.get_sign(data_set)

        # uoload image file
        status, key = self.upload_img(filename, signature, policy, accessid)

        # 上传成功后，拼接生成的 查询 URL
        if status == "succ":
            url_res = 'https://s.1688.com/youyuan/index.htm?tab=imageSearch&imageType=oss&imageAddress={}'.format(key)
            return url_res
        else:
            return ""
