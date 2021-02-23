#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import base64
import json
from lib.func_txy import request_get
from lib.func_txy import request_post
from lib.func_txy import request_get_content
from lib.func_txy import get_random_str
from lib.func_txy import get_random_digits
import os.path
from urllib.parse import urlparse
import requests
import io


class Alibaba(object):
    """
    1688 PC 端接口获取相似商品的接口
    """

    def __init__(self, cookie):
        self.upload_url = 'https://cbusearch.oss-cn-shanghai.aliyuncs.com/'  # 上传图片
        self.sign_url = "https://open-s.1688.com/openservice/ossDataService"  # 获取 sign 加密
        self.imageSearch_service_url = "https://open-s.1688.com/openservice/imageSearchOfferResultViewService"
        self._headers(cookie=cookie)
        self.search_page_size = 40

    def setSearchPageSize(self, pageSize):
        self.search_page_size = pageSize

    def _headers(self, cookie):
        headres = {
            'Origin': "https://www.1688.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0",
            "Accept": "*/*",
            "Cache-Control": "no-cache",
            "refer": "https://www.1688.com/",
            "cookie": cookie
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
        url = "https://open-s.1688.com/openservice/.htm"  # 获取加密时间
        params = {
            "serviceIds": "cbu.searchweb.config.system.currenttime",
            "outfmt": "json",
        }
        print(params)

        # status, data = request_get_content(url, params, self.headers)
        status, data = request_get(url, params, self.headers)
        return status, data

    def get_sign(self, data_set):
        '''
        用于获取 sign 用于加密
        :return:
        '''
        url = 'https://open-s.1688.com/openservice/ossDataService'
        key = str(base64.b64decode("cGNfdHVzb3U=".encode("utf-8")), encoding="utf-8")
        appkey = "{};{}".format(key, str(data_set))

        params = {
            "appName": key,
            "appKey": base64.b64encode(appkey.encode("utf-8")),
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
        key = "cbuimgsearch/" + get_random_str(10) + str(int(time.time()) * 1000) + ".jepg"
        name = get_random_str(5) + ".jpeg"

        if os.path.exists(filename):
            bytestream = open(filename, "rb").read()
        else:
            us = urlparse(filename)
            if not us:
                return 'fail', None
            r = requests.get(filename)
            bytestream = io.BytesIO(r.content)

        files = {
            "name": (None, name),
            "key": (None, key),
            "policy": (None, policy),
            "OSSAccessKeyId": (None, accessid),
            "success_action_status": (None, 200),
            "callback": (None, ""),
            "signature": (None, signature),
            "file": (name, bytestream)
        }

        status, res = request_post(url, data=None, files=files, headers=self.headers)
        return status, key

    def img_search(self, img_key, dataSet, beginPage=1):
        """
        用于上传图片并搜索商品列表
        从1688官网图搜页面扒出来的jsonp接口
        :return: dict o None
        """
        app_name = "pc_tusou"

        app_key = base64.b64encode(f'{app_name};{dataSet}'.encode("utf-8"))

        appKey = str(app_key, encoding="utf8")

        request_params = {
            "imageAddress": img_key,
            "imageType": "oss",
            "pageSize": self.search_page_size,
            "beginPage": beginPage,
            "categoryId": "null",
            "appName": app_name,
            "appKey": appKey,
            "callback": ""
        }
        status_desc, data = request_get(self.imageSearch_service_url, request_params, headers=self.headers)
        if status_desc == "succ":
            return 'succ', data
        else:
            return 'fail', None

    def run(self, filename, need_products=False):
        status, data = self.get_dateset()
        print(status, data)

        # json 直接解析
        data_set = data.get('cbu.searchweb.config.system.currenttime', {}).get('dataSet', '')

        # 获取相关的 接口验证参数。同时 获取生成的 图片key
        status, signature, policy, accessid = self.get_sign(data_set)
        print(status, signature, policy, accessid)

        # uoload image file
        status, key = self.upload_img(filename, signature, policy, accessid)
        # 上传成功后，拼接生成的 查询 URL
        if status == "succ":
            url_res = 'https://s.1688.com/youyuan/index.htm?tab=imageSearch&imageType=oss&imageAddress={}'.format(
                key.split(".")[0])
            if need_products == False:
                return url_res
            else:
                status_desc, data = self.img_search(key, data_set)
                if status_desc == 'succ':
                    return data
                return None
        else:
            return ""
