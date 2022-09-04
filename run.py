#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib.alibaba import Token, Upload, ImageSearch

if __name__ == '__main__':

    # get cookie and token
    token = Token()
    req = token.request()
    cookies = req.cookies

    # upload image and get image id
    upload = Upload(cookies=cookies)
    res = upload.upload(filename="data/下载.jpeg")
    image_id = res.json().get("data", {}).get("imageId", "")
    if not image_id:
        raise Exception("not image id")

    # search goods by image id
    image_search = ImageSearch()
    req = image_search.request(image_id=image_id)
