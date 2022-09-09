#!/usr/bin/env python
# -*- coding: utf-8 -*-


from lib import ali1688, alibaba

if __name__ == "__main__":

    # 1688 example
    # get cookie and token
    token = ali1688.Token()
    req = token.request()
    cookies = req.cookies

    # upload image and get image id
    upload = ali1688.Upload(cookies=cookies)
    res = upload.upload(filename="data/down.jpeg")
    image_id = res.json().get("data", {}).get("imageId", "")
    if not image_id:
        raise Exception("not image id")
    print(image_id)

    # search goods by image id
    image_search = ali1688.ImageSearch()
    req = image_search.request(image_id=image_id)
    print(req.url)

    # alibaba example
    upload = alibaba.Upload()
    image_key = upload.upload(filename="data/down.jpeg")
    print(f"{image_key=}")

    image_searh = alibaba.ImageSearch()
    req = image_searh.search(image_key=image_key)
    print(req.url)
