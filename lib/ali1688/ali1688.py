#!/usr/bin/env python
# -*- coding: utf-8 -*-


import base64
import json
import re
from typing import Dict

import requests
from requests.cookies import RequestsCookieJar

from lib.ali1688.sign import Sign
from lib.func_txy import now, request_get, request_post


class Ali1688(object):
    def __init__(self):
        self.t = now()
        self.app_key = "12574478"

    def headers(self):
        headres = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0",
        }
        return headres


class Token(Ali1688):
    def __init__(self, api: str, hostname: str):
        self.api = api
        self.hostname = hostname
        self.token_url = f"https://{self.hostname}/h5/{self.api.lower()}/1.0/"
        self.cookies: RequestsCookieJar
        super(Token, self).__init__()

    def get_token_params(self) -> Dict[str, str]:
        params = {
            "jsv": "2.7.0",
            "appKey": self.app_key,
            "t": str(self.t),
            "api": self.api,
            "v": "1.0",
            "type": "json",
            "dataType": "jsonp",
            "callback": "mtopjsonp1",
        }
        return params

    def request(self) -> requests.request:
        params = self.get_token_params()
        headers = self.headers()
        req = request_get(url=self.token_url, params=params, headers=headers)
        self.cookies: RequestsCookieJar = req.cookies
        return req

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


class Ali1688Upload(Token):
    def __init__(self, api: str = "mtop.1688.imageService.putImage", hostname="h5api.m.taobao.com"):
        super(Ali1688Upload, self).__init__(api=api, hostname=hostname)
        self.upload_url = f"https://{self.hostname}/h5/{self.api.lower()}/1.0"
        self.request()
        self._get_token()

    def get_params(self, data: str, t: int, jsv: str = "2.4.11") -> Dict[str, str]:
        sign_str = self.get_sign(data=data, t=t)
        params = {
            "jsv": jsv,
            "appKey": self.app_key,
            "t": str(t),
            "api": self.api,
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
            url=self.upload_url,
            params=params,
            headers=headers,
            data=data,
            cookies=self.cookies.get_dict(),
        )
        return req


class WorldTaobao(Ali1688Upload):
    def __init__(self, api: str = "mtop.tmall.hk.yx.worldhomepagepcapi.gethotwords", hostname="h5api.m.taobao.com"):
        super(WorldTaobao, self).__init__(api=api, hostname=hostname)
        self.upload_url = f"https://{self.hostname}/h5/mtop.relationrecommend.wirelessrecommend.recommend/2.0/"

    def get_data(self, filename: str) -> Dict[str, str]:
        # get file bytes
        with open(filename, "rb") as f:
            b64_bytes = base64.b64encode(f.read())
        strimg = str(b64_bytes).replace("b'", "").replace("'", "").replace("==", "")
        params = json.dumps(
            {
                "strimg": strimg,
                "pcGraphSearch": True,
                "sortOrder": 0,
                "tab": "all",
                "vm": "nv",
            },
            separators=(",", ":"),
        )

        data = json.dumps({"params": params, "appId": "34850"}, separators=(",", ":"), )

        return {"data": data}


class Ali1688ImageSearch(Ali1688):
    def __init__(self):
        self.url = "https://s.1688.com/youyuan/index.htm"
        super(Ali1688ImageSearch, self).__init__()

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
