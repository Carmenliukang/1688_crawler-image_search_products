#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from urllib.parse import urlencode
from lib.func_txy import request_post
from lib.func_txy import get_random_str


class JD(object):
    def __init__(self):
        self._headers()

    def _headers(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0",
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
        }

    def upload_img(self, filename):
        url = "https://search.jd.com/image?op=upload"
        files = {
            "file": (get_random_str(5) + ".jpg", open(filename, "rb").read()),
        }

        status, data = request_post(url, files=files, headers=self.headers)
        return status, data

    def run(self, filename):
        status, data = self.upload_img(filename)
        url = ""
        if status == "succ" and "script" in data:
            path = re.findall("callback\(\"(.*?)\"\);", data)
            if path:
                url = "https://search.jd.com/image?{}".format(urlencode({"path": path[0], "op": "search"}))

        return url
