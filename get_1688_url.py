# !/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-05 10:29
# @Author  : liukang.hero
# @FileName: get_1688_url.py

import json
import time
import base64
import random
import requests
import contextlib
from requests_toolbelt import MultipartEncoder

chioce_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z',
               'a', 'b', 'c', 'd', 'e', 'f', 'h', 'i', 'j', 'k', 'm', 'n', 'p', 'r', 's', 't', 'w', 'x', 'y', 'z', '2',
               '3', '4', '5', '6', '7', '8']


def request_post_files(url, data, headers):
    try:
        with contextlib.closing(requests.post(url=url, data=data, headers=headers)) as req:
            data = req.text
            return "succ", data
    except Exception as e:
        print(e)
        return "fail", {}


def request_post(url, data, headers):
    try:
        with contextlib.closing(requests.post(url=url, data=data, headers=headers)) as req:
            data = req.text
            return "succ", data
    except Exception as e:
        print(e)
        return "fail", {}


def request_get(url, params, headers):
    try:
        with contextlib.closing(requests.get(url=url, params=params, headers=headers)) as req:
            data = req.text
            return "succ", data
    except Exception as e:
        print(e)
        return "fail", {}


def get_key():
    '''
    cbuimgsearch/Z5Qja4fXPH1562293605000.jpg 生活规则是 cbuimgsearch/ + 随机10位 + 毫秒级别时间戳
    :return:
    '''
    key = "cbuimgsearch/" + "".join(random.sample(chioce_list, 10)) + str(int(time.time() * 1000))
    return key


def get_headers():
    headers = {
        'Origin': "https://www.1688.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
    }
    return headers


def get_params(filename, signature, policy, OSSAccessKeyId):
    key = get_key()
    file_payload = {
        "name": filename,
        "key": key,
        "policy": policy,
        "OSSAccessKeyId": OSSAccessKeyId,
        "success_action_status": "200",
        "callback": "",
        "signature": signature,
        "file": open(filename, 'rb').read()
    }

    m = MultipartEncoder(file_payload)

    headers = get_headers()
    headers['Content-Type'] = m.content_type
    return m, headers, key


def get_dataset():
    '''
    获取 dataSet 时间戳，用于 加密
    callback 用于 str replace
    :return:
    '''
    url = 'https://open-s.1688.com/openservice/.htm?'
    callback = "jQuery18303374729635985685_" + str(int(time.time() * 1000))
    params = {
        "callback": callback,
        "serviceIds": "cbu.searchweb.config.system.currenttime",
        "outfmt": "jsonp",
        "_": str(int(time.time() * 1000))
    }

    headers = {
        "Host": 'open-s.1688.com',
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }

    status, data = request_get(url, params, headers)
    return status, data, callback


def get_signature(data_set):
    '''
    获取上传文件必须的参数
    :param data_set: 加密的时间戳
    :return:
    '''
    url = 'https://open-s.1688.com/openservice/ossDataService'
    appkey = "{};{}".format('pc_tusou', str(data_set))

    callback = "jQuery18303536909897611926_{}".format(str(int(time.time() * 1000)))

    params = {
        "appName": "pc_tusou",
        "appKey": base64.b64encode(appkey.encode("utf-8")),
        # 发生变化 pc_tusou;1562288848391 b64 编码 pc_tusou;毫秒级时间戳
        "callback": callback,
        "_": str(int(time.time() * 1000)),  # 时间戳
        "": ""
    }

    headers = {
        "Host": 'open-s.1688.com',
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }

    status, data = request_get(url, params, headers)

    # 返回结果处理
    json_str = data.replace("{}(".format(callback), "").replace(");", '')
    result = json.loads(json_str)
    signature = result.get('data', {}).get('signature', '')
    policy = result.get('data', {}).get('policy', '')
    OSSAccessKeyId = result.get('data', {}).get('accessid', '')

    return status, signature, policy, OSSAccessKeyId


def upload_1688_image(filename, signature, policy, OSSAccessKeyId):
    '''
    上传文件。这里使用的是 MultipartEncoder 包，更加便捷生成 multipart/form-data 类型的body
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundarybsKUYKw7Wu6nNEAG
    :param filename: 上传文件名称
    :param signature:必须参数，通过 调用 https://open-s.1688.com/openservice/ossDataService 获取。
    :param policy:必须参数，通过 调用 https://open-s.1688.com/openservice/ossDataService 获取。
    :param OSSAccessKeyId:必须参数，通过 调用 https://open-s.1688.com/openservice/ossDataService 获取。
    :return: status fail|succ key图片唯一ID
    '''
    url = 'https://cbusearch.oss-cn-shanghai.aliyuncs.com/'

    m, headers, key = get_params(filename, signature, policy, OSSAccessKeyId)

    status, res = request_post_files(url, m, headers)
    return status, key


def get_1688_url(filename):
    '''
    1. 获取 需要 b64 编码的时间戳
    2. 获取 必须传输的参数 signature policy 同时将生成的 图片 key 返回
    3. 上传图片
    4. 拼接查询的结果
    :param filename:
    :return:
    '''
    status, data, callback = get_dataset()

    # 这里 采用 str 匹配，因为相比较正则，str replace 更加快
    json_str = data.replace("{}(".format(callback), "").replace(");", '')
    data_set = json.loads(json_str).get('cbu.searchweb.config.system.currenttime', {}).get('dataSet', '')

    # 获取相关的 接口验证参数。同时 获取生成的 图片key
    status, signature, policy, OSSAccessKeyId = get_signature(data_set)

    # uoload image
    status, key = upload_1688_image(filename, signature, policy, OSSAccessKeyId)

    # 上传成功后，拼接生成的 查询 URL
    if status == "succ":
        url_res = 'https://s.1688.com/youyuan/index.htm?' \
                  'tab=imageSearch&imageType=oss&imageAddress={}&spm=a260k.635.3262836.d1088'.format(key)
        return url_res
    else:
        return ""


if __name__ == '__main__':
    filename = "image/666.jpg"
    t0 = time.time()
    url_res = get_1688_url(filename)
    print(url_res)

    t1 = time.time()
    print(t1 - t0)
