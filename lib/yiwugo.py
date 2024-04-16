#!/usr/bin/env python
# -*- coding: utf-8 -*-

from urllib.parse import urlencode

from lib.func_txy import request_post, fileb64_encode


class YiWuGo(object):
    def __init__(self):
        self.upload_url = (
            "https://img.yiwugo.com/search.html?cpage=1&imageRetrievalMethod=original"
        )
        self.token = ""
        self._headers()

    def _headers(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:107.0) Gecko/20100101 Firefox/107.0",
            "Origin": "https://www.yiwugo.com/",
            "Referer": "https://www.yiwugo.com/",
            "Content-Type": "application/x-www-form-urlencoded",
        }

    def upload(self, path):
        b64_string = fileb64_encode(path)
        data = urlencode({"code": b64_string})
        res = request_post(url=self.upload_url, data=data, headers=self.headers)
        return res
