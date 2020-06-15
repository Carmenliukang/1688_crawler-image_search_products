# !/usr/bin/python
# -*- coding: utf-8 -*-


import random
import string
import requests
import contextlib


def request_post(url, data=None, files={}, headers={}, timeout=10):
    try:
        with contextlib.closing(
                requests.post(url=url, data=data, files=files, headers=headers, timeout=timeout)) as req:
            res = req.text
            return "succ", res
    except Exception as e:
        print(e)
        return "fail", {}


def request_get(url, params, headers, timeout=10):
    try:
        with contextlib.closing(requests.get(url=url, params=params, headers=headers, timeout=timeout)) as req:
            data = req.json()
            return "succ", data
    except Exception as e:
        print(e)
        return "fail", {}


def request_get_content(url, params=None, headers={}, timeout=10):
    try:
        with contextlib.closing(requests.get(url=url, params=params, headers=headers, timeout=timeout)) as req:
            data = req.text
            return "succ", data
    except Exception as e:
        print(e)
        return "fail", {}


def get_random_str(k):
    return ''.join(random.choices(string.ascii_letters, k=k))


def get_random_digits(k):
    return ''.join(random.choices(string.digits, k=k))
