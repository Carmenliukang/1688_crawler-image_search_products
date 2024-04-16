#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lib import alibaba, yiwugo
from lib.ali1688 import ali1688
from lib.world_taobao.world_taobao import WorldTaobao

if __name__ == "__main__":
    path = "data/down.jpeg"

    upload = ali1688.Ali1688Upload()
    res = upload.upload(filename=path)
    print(res.json())

    image_id = res.json().get("data", {}).get("imageId", "")
    if not image_id:
        raise Exception("not image id")
    print(upload.image_search_url(image_id=image_id))

    taobao_upload = WorldTaobao()
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

    # # yiwugo
    yiwugo = yiwugo.YiWuGo()
    res = yiwugo.upload(path)
    assert "起购" in res.text, "yiwugo search error"
