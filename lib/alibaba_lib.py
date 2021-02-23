#!/usr/bin/env python
# -*- coding: utf-8 -*-
import io
import os
import re
import json
import requests
from lib.func_txy import request_post
from lib.func_txy import request_get_content
from lib.func_txy import get_random_str
from urllib.parse import urlparse


class Alibaba(object):
    """
    1688 PC 端接口获取相似商品的接口
    """

    def __init__(self, cookie):
        self.upload_url = "https://stream-upload.taobao.com/api/upload.api?appkey=1688search&folderId=0&_input_charset=utf-8&useGtrSessionFilter=false"  # 上传图片
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

    def upload_img(self, filename):
        """
        用于上传图片
        :return:
        """
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
            # "ua": (None, ""),
            "file": (name, bytestream)
        }

        status, res = request_post(self.upload_url, data=None, files=files, headers=self.headers)
        key = ""
        if status == "succ":
            data = json.loads(res)
            url = data["object"]["url"]
            key = url.split("/")[-1]
        return status, key

    def img_search(self, url):
        """
        用于上传图片并搜索商品列表
        从1688官网图搜页面扒出来的jsonp接口
        :return: dict o None
        """
        status_desc, data = request_get_content(url, headers=self.headers)
        if status_desc == "succ":
            return 'succ', data
        else:
            return 'fail', None

    def check_goods(self, html):
        """
        todo 这里需要匹配
        :param html:
        :return:
        """
        re.findall("window.data.offerresultData = successDataCheck\(.*?\)", html)

    def run(self, filename, need_products=False):
        # uoload image file
        status, key = self.upload_img(filename)

        # 上传成功后，拼接生成的 查询 URL
        if status == "succ":
            url_res = f"https://s.1688.com/youyuan/index.htm?tab=imageSearch&imageAddress={key}&spm="
            if need_products == False:
                return url_res
            else:
                status_desc, data = self.img_search(url_res)
                if status_desc == 'succ':
                    return data
                return None
        else:
            return ""
