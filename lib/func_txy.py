#!/usr/bin/env python
# encoding: utf-8

import random
import string
import requests
import contextlib

import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def get_random_str(k):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k))


def request_get(url, params=None, headers={}, allow_redirects=True):
    try:
        with contextlib.closing(
                requests.get(url, params=params, headers=headers, timeout=30, allow_redirects=allow_redirects)) as req:
            data = req.json()
        return "succ", data
    except Exception as e:
        print(e)
        return "fail", {}


def request_post(url, data=None, files=None, headers={}):
    try:
        with contextlib.closing(requests.post(url, data=data, files=files, headers=headers, timeout=30)) as req:
            data = req.text
        return "succ", data
    except Exception as e:
        print(e)
        return "fail", {}
