import time
from typing import Dict, Optional
from requests.cookies import RequestsCookieJar
from lib.func_txy import get_headers, request_get, calculate_md5_hash

from config.setting import (
    ali1688_api_key,
    ali1688_v,
    ali1688_jsv,
    ali1688_token_api,
    ali1688_host,
)


class Token(object):
    def __init__(self):
        self.cookies: Optional[RequestsCookieJar] = None
        self.token_request()

    @property
    def token_url(self):
        return f"https://{ali1688_host}/h5/{ali1688_token_api.lower()}/{ali1688_v}/"

    @property
    def t(self):
        return int(time.time())

    def get_sign(self, data: str, t: int, token: str) -> str:
        text = f"{token}&{t}&{ali1688_api_key}&{data}"
        sign_str = calculate_md5_hash(text)
        return sign_str

    def get_token_params(self) -> Dict[str, str]:
        params = {
            "jsv": ali1688_jsv,
            "appKey": ali1688_api_key,
            "t": self.t,
            "api": ali1688_token_api,
            "v": ali1688_v,
            "type": "json",
            "dataType": "jsonp",
            "callback": "mtopjsonp1",
            "preventFallback": True,
            "data": {},
        }
        return params

    def token_headers(self):
        headers = get_headers()
        headers["authority"] = "h5api.m.1688.com"
        headers["Referer"] = "https://www.1688.com/"
        return headers

    def token_request(self):
        params = self.get_token_params()
        req = request_get(
            url=self.token_url, params=params, headers=self.token_headers()
        )
        self.cookies = req.cookies

    @property
    def token(self):
        if not self.cookies or not self.cookies.get("_m_h5_tk", ""):
            raise Exception("cookie not found _m_h5_tk")

        cookie_list = self.cookies.get("_m_h5_tk", "").split("_")
        if len(cookie_list) < 2:
            raise Exception("cookie _m_h5_tk not found '_' ")

        token: str = cookie_list[0]
        return token
