#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from typing import Dict

import requests
from urllib.parse import urlencode

from lib.func_txy import (
    now,
    request_post,
    get_headers,
    fileb64_encode,
)
from lib.ali1688.token import Token
from config.setting import (
    ali1688_upload_api,
    ali1688_host,
    ali1688_api_key,
    ali1688_jsv,
    ali1688_upload_app_name,
    ali1688_upload_app_key,
    ali1688_v,
)


class Ali1688Upload(Token):
    def __init__(self):
        super(Ali1688Upload, self).__init__()

    @property
    def upload_url(self):
        return f"https://{ali1688_host}/h5/{ali1688_upload_api.lower()}/{ali1688_v}"

    @property
    def upload_headers(self):
        headres = get_headers()
        headres["referer"] = "https://www.1688.com/"
        headres["Content-Type"] = "application/x-www-form-urlencoded"
        return headres

    def get_params(
        self,
        data: str,
        t: int,
        jsv: str = ali1688_jsv,
    ) -> Dict[str, str]:
        sign_str = self.get_sign(data=data, t=t, token=self.token)
        params = {
            "jsv": jsv,
            "appKey": ali1688_api_key,
            "t": t,
            "api": ali1688_upload_api,
            "ecode": "0",
            "v": ali1688_v,
            "type": "originaljson",
            "dataType": "jsonp",
            "sign": sign_str,
        }
        return params

    def get_data(self, filename: str) -> Dict[str, str]:
        b64_str = fileb64_encode(filename)
        data = json.dumps(
            {
                "imageBase64": b64_str,
                "appName": ali1688_upload_app_name,
                "appKey": ali1688_upload_app_key,
            },
            separators=(",", ":"),
        )
        return {"data": data}

    def upload(self, filename: str) -> requests.request:
        # upload image
        t = now()
        data = self.get_data(filename=filename)
        params = self.get_params(data=data.get("data", ""), t=t)
        headers = self.upload_headers
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        req = request_post(
            url=self.upload_url,
            params=params,
            headers=headers,
            data=data,
            cookies=self.cookies.get_dict(),
        )
        return req

    def image_search_url(self, image_id: str):
        url = "https://s.1688.com/youyuan/index.htm"
        params = {"tab": "imageSearch", "imageId": image_id, "imageIdList": image_id}
        return "{}?{}".format(url, urlencode(params))
