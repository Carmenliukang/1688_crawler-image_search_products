#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path
import pathlib
import time

from lib.func_txy import get_random_str, request_get, request_post


class Alibaba(object):
    def __init__(self):
        self.app_key = "a5m1ismomeptugvfmkkjnwwqnwyrhpb1"
        self.app_name = "magellan"
        self.url = "https://www.alibaba.com/"
        self._headers()

    def _headers(self):
        headres = {
            "Origin": "https://www.alibaba.com",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
            "Accept": "*/*",
            "Referer": "https://www.alibaba.com",
        }
        self.headers = headres


class Sign(Alibaba):
    def __init__(self):
        super(Sign, self).__init__()
        self.sign_url = f"https://open-s.alibaba.com/openservice/ossUploadSecretKeyDataService?appKey={self.app_key}&appName={self.app_name}"

    def sign(self):
        req = request_get(url=self.sign_url, headers=self.headers)
        return req


class Upload(Sign):
    """
    1688 PC 端接口获取相似商品的接口
    """

    def __init__(self):
        super(Upload, self).__init__()

    def get_image_key(self, image_path: str, file_extension: str):
        """
        cbuimgsearch/Z5Qja4fXPH1562293605000.jpg role cbuimgsearch/ + random 10 + time.time
        :return:
        """
        image_key = (
            f"{image_path}/"
            + "".join(get_random_str(10))
            + str(int(time.time() * 1000))
        )
        return image_key

    def get_requst_params(self, filename: str):
        sign_req = self.sign()
        sign_req = sign_req.json()
        if not sign_req.get("data", ""):
            raise Exception("get sign error")
        data = sign_req.get("data", "")

        url = data.get("host", "")
        assert url
        signature = data.get("signature", "")
        assert signature
        policy = data.get("policy", "")
        assert policy
        accessid = data.get("accessid", "")
        assert accessid
        image_path = data.get("imagePath", "")
        assert image_path

        file_extension = pathlib.Path(filename).suffix
        image_key = self.get_image_key(
            image_path=image_path, file_extension=file_extension
        )
        name = get_random_str(5) + file_extension

        if os.path.exists(filename):
            bytestream = open(filename, "rb").read()
        else:
            raise Exception(f"not found {filename}")

        files = {
            "name": (None, name),
            "key": (None, image_key),
            "policy": (None, policy),
            "OSSAccessKeyId": (None, accessid),
            "success_action_status": (None, 200),
            "callback": (None, ""),
            "signature": (None, signature),
            "file": (name, bytestream),
        }
        return files, url, image_key

    def upload(self, filename: str):
        files, url, image_key = self.get_requst_params(filename=filename)
        req = request_post(url, files=files, headers=self.headers)
        if not req.text:
            return image_key
        else:
            raise Exception("upload image failed")


class ImageSearch(Alibaba):
    def __init__(self):
        super(ImageSearch, self).__init__()
        self.search_url = "https://www.alibaba.com/picture/search.htm"

    def params(self, image_key: str):
        params = {
            "imageType": "oss",
            "escapeQp": True,
            "imageAddress": f"/{image_key}",
            "sourceFrom": "imageupload",
        }
        return params

    def search(self, image_key: str):
        params = self.params(image_key=image_key)
        req = request_get(url=self.search_url, params=params, headers=self.headers)
        return req
