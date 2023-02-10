#!/usr/bin/env python
# -*- coding: utf-8 -*-


from lib import alibaba, yiwugo
from lib.ali1688 import ali1688

if __name__ == "__main__":
    path = "data/down.jpeg"

    # 1688 example
    # get cookie and token
    # # upload image and get image id
    upload = ali1688.Ali1688Upload()
    res = upload.upload(filename=path)
    image_id = res.json().get("data", {}).get("imageId", "")
    if not image_id:
        raise Exception("not image id")
    print(image_id)

    # search goods by i®mage id
    image_search = ali1688.Ali1688ImageSearch()
    req = image_search.request(image_id=image_id)
    print(req.url)

    taobao_upload = ali1688.WorldTaobao()
    res = taobao_upload.upload(filename=path)
    if res.json().get("data"):
        print("taobao_upload success")

    # alibaba example
    upload = alibaba.Upload()
    image_key = upload.upload(filename=path)
    print(f"{image_key}")

    image_searh = alibaba.ImageSearch()
    req = image_searh.search(image_key=image_key)
    print(req.url)

    # yiwugo
    yiwugo = yiwugo.YiWuGo()
    res = yiwugo.upload(path)
    print(res.status_code)
    assert "起购" in res.text, "yiwugo search error"
