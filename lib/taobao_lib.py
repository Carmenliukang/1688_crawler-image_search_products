#!/usr/bin/env python
# -*- coding: utf-8 -*-


import json
from lib.func_txy import request_post
from lib.func_txy import get_random_str


class TaoBao(object):
    def __init__(self, cookie=None):
        self.cookie = cookie
        self._headers()

    def _headers(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Referer": "https://www.taobao.com/",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "origin": "https://www.taobao.com",
        }
        if self.cookie:
            self.headers["cookie"] = self.cookie

    def upload_img(self, filename):
        url = "https://s.taobao.com/image"
        files = {
            "cross": (None, "taobao"),
            "type": (None, "iframe"),
            "imgfile": (get_random_str(5) + ".jpg", open(filename, "rb").read(), "image/jpeg"),
        }

        status, data = request_post(url, files=files, headers=self.headers)
        return status, data

    def run(self, filename):
        status, data = self.upload_img(filename)
        url = ""
        if status == "succ" and "script" in data:
            res = data.replace('<script>document.domain="taobao.com";</script>', '')
            msg = json.loads(res)
            url = "https://s.taobao.com/search?tfsid={}&app=imgsearch".format(msg.get('name', ''))

        return url
