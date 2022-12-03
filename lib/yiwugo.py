#!/usr/bin/env python
# -*- coding: utf-8 -*-


import base64
import re
import time
from urllib.parse import urlencode

from lib.func_txy import request_get, request_post


class YiWuGo(object):
    def __init__(self):
        self.origin_url = "https://www.yiwugo.com/"
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

    def get_token(self):
        res = request_get(url=self.origin_url, headers=self.headers)
        token = re.findall('hm.baidu.com/hm.js\?(.*?)";', res.text)
        self.token = token[0] if len(token) == 1 else ""

    def upload(self, path):
        with open(path, "rb") as f:
            b64_string = base64.b64encode(f.read()).decode("utf-8")
        data = urlencode({"code": b64_string})
        now = str(int(time.time()))
        if not self.token:
            self.get_token()
        assert self.token, "yiwug get token error"
        cookies = {
            f"Hm_lvt_{self.token}": now,
            f"Hm_lpvt_{self.token}": now,
        }
        res = request_post(
            url=self.upload_url, data=data, headers=self.headers, cookies=cookies
        )
        return res
