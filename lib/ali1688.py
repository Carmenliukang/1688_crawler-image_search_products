#!/usr/bin/env python
# -*- coding: utf-8 -*-


import base64
import json
import re
from typing import Dict

import requests
from requests.cookies import RequestsCookieJar

from lib.func_txy import now, request_get, request_post
from lib.sign import Sign


class Ali1688(object):
    def __init__(self):
        self.t = now()
        self.app_key = "12574478"

    def headers(self):
        headres = {
            "Origin": "https://s.1688.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0",
            "referer": "https://s.1688.com",
        }
        return headres


class Token(Ali1688):
    def __init__(self):
        self.url = "https://h5api.m.1688.com/h5/mtop.taobao.widgetservice.getjsoncomponent/1.0/?jsv=2.7.0&appKey=12574478&t=1662222785423&api=mtop.taobao.widgetService.getJsonComponent&v=1.0&type=json&dataType=jsonp&callback=mtopjsonp1"
        super(Token, self).__init__()

    def get_params(self) -> Dict[str, str]:
        params = {
            "jsv": "2.7.0",
            "appKey": self.app_key,
            "t": str(self.t),
            "api": "mtop.taobao.widgetService.getJsonComponent",
            "v": "1.0",
            "type": "json",
            "dataType": "jsonp",
            "callback": "mtopjsonp1",
        }
        return params

    def request(self) -> requests.request:
        params = self.get_params()
        headers = self.headers()
        req = request_get(url=self.url, params=params, headers=headers)
        return req


class Upload(Ali1688):
    def __init__(self, cookies: RequestsCookieJar):
        self.cookies: RequestsCookieJar = cookies
        self.url = "https://h5api.m.1688.com/h5/mtop.1688.imageservice.putimage/1.0"
        self._get_token()
        super(Upload, self).__init__()

    def _get_token(self):
        if not self.cookies or not self.cookies.get("_m_h5_tk", ""):
            raise Exception("cookie not found _m_h5_tk")

        cookie_list = self.cookies.get("_m_h5_tk", "").split("_")
        if len(cookie_list) < 2:
            raise Exception("cookie _m_h5_tk not found '_' ")

        self.token: str = cookie_list[0]

    def get_sign(self, data: str, t: int) -> str:
        text = f"{self.token}&{t}&{self.app_key}&{data}"
        sign = Sign()
        sign_str = sign.sign(text)
        return sign_str

    def get_params(self, data: str, t: int) -> Dict[str, str]:
        sign_str = self.get_sign(data=data, t=t)
        params = {
            "jsv": "2.4.11",
            "appKey": self.app_key,
            "t": str(t),
            "api": "mtop.1688.imageService.putImage",
            "ecode": "0",
            "v": "1.0",
            "type": "originaljson",
            "dataType": "jsonp",
            "sign": sign_str,
        }
        return params

    def get_data(self, filename: str) -> Dict[str, str]:
        # get file bytes
        with open(filename, "rb") as f:
            b64_bytes = base64.b64encode(f.read())
        data = json.dumps(
            {
                "imageBase64": str(b64_bytes).replace("b'", "").replace("'", ""),
                "appName": "searchImageUpload",
                "appKey": "pvvljh1grxcmaay2vgpe9nb68gg9ueg2",
            },
            separators=(",", ":"),
        )
        return {"data": data}

    def upload(self, filename: str) -> requests.request:
        # upload image
        t = now()
        data = self.get_data(filename=filename)
        params = self.get_params(data=data.get("data", ""), t=t)
        headers = self.headers()
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        req = request_post(
            url=self.url,
            params=params,
            headers=headers,
            data=data,
            cookies=self.cookies.get_dict(),
        )
        return req


class ImageSearch(Ali1688):
    def __init__(self):
        self.url = "https://s.1688.com/youyuan/index.htm"
        super(ImageSearch, self).__init__()

    def get_params(self, image_id: str) -> Dict[str, str]:
        params = {"tab": "imageSearch", "imageId": image_id, "imageIdList": image_id}
        return params

    def request(self, image_id: str) -> requests.request:
        params = self.get_params(image_id=image_id)
        headers = self.headers()
        req = request_get(url=self.url, params=params, headers=headers)
        return req

    def check_goods(self, html: str):
        # todo
        re.findall("window.data.offerresultData = successDataCheck\(.*?\)", html)
