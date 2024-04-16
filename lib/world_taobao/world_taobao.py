import json
import requests
from typing import Dict
from lib.ali1688.token import Token
from config.setting import (
    world_taobao_api,
    ali1688_host,
    world_taobao_api_id,
    ali1688_jsv,
    world_taobao_api_v,
    ali1688_api_key,
)
from lib.func_txy import fileb64_encode, now, request_post


class WorldTaobao(Token):
    def __init__(self):
        super(WorldTaobao, self).__init__()
        self.upload_url = f"https://{ali1688_host}/h5/{world_taobao_api.lower()}/2.0/"

    def get_data(self, filename: str) -> Dict[str, str]:
        # get file bytes
        strimg = fileb64_encode(filename)
        params = json.dumps(
            {
                "strimg": strimg,
                "pcGraphSearch": True,
                "sortOrder": "0",
                "region": "",
                "tab": "all",
                "vm": "nv",
                "sversion": "15.8",
                "ttid": "600000@taobao_android_10.16.10",
            },
            separators=(",", ":"),
        )
        data = json.dumps(
            {"params": params, "appId": world_taobao_api_id}, separators=(",", ":")
        )

        return {"data": data}

    @property
    def upload_headers(self):
        headres = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:85.0) Gecko/20100101 Firefox/85.0",
            "referer": "https://world.taobao.com/",
        }
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
            "api": world_taobao_api,
            "v": world_taobao_api_v,
            "type": "originaljson",
            "dataType": "jsonp",
            "sign": sign_str,
        }
        return params

    def upload(self, filename: str) -> requests.request:
        # upload image
        data = self.get_data(filename=filename)
        headers = self.upload_headers
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["origin"] = "https://world.taobao.com"
        headers["cookie"] = ""
        for k, v in self.cookies.items():
            headers["cookie"] += f"{k}={v}; "
        params = self.get_params(data=data, t=now())
        req = request_post(
            url=self.upload_url,
            params=params,
            headers=headers,
            data=data,
            # cookies=self.cookies.get_dict()
        )
        return req
