# !/usr/bin/python
# -*- coding: utf-8 -*-

import contextlib
import random
import string
import time
import requests
import hashlib
import base64


def calculate_md5_hash(text: str):
    return hashlib.md5(text.encode("utf-8")).hexdigest()


def request_post(
    url, params=None, data=None, files=None, headers=None, timeout=10, cookies=None
):
    with contextlib.closing(
        requests.post(
            url=url,
            params=params,
            data=data,
            files=files,
            headers=headers,
            cookies=cookies,
            timeout=timeout,
        )
    ) as req:
        return req


def request_get(url, params=None, headers=None, timeout=10, cookies=None):
    with contextlib.closing(
        requests.get(
            url=url, params=params, headers=headers, cookies=cookies, timeout=timeout
        )
    ) as req:
        return req


def get_random_str(k):
    return "".join(random.choices(string.ascii_letters, k=k))


def get_random_digits(k):
    return "".join(random.choices(string.digits, k=k))


def now():
    return int(time.time() * 1000)


def get_headers():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    return headers


def fileb64_encode(path):
    with open(path, "rb") as f:
        b64_str = base64.b64encode(f.read()).decode("ascii")
        return b64_str
