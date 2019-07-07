# !/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-05 10:29
# @Author  : liukang.hero
# @FileName: test.py


import json
import time
import base64
import random
import requests
import contextlib

# 用于生成随机数
chioce_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z',
               'a', 'b', 'c', 'd', 'e', 'f', 'h', 'i', 'j', 'k', 'm', 'n', 'p', 'r', 's', 't', 'w', 'x', 'y', 'z', '2',
               '3', '4', '5', '6', '7', '8']


# 上传文件
def request_post_files(url, data, headers):
    with contextlib.closing(requests.post(url=url, files=data, headers=headers)) as req:
        data = req.text
        return "succ", data


# post 请求
def request_post(url, data, headers):
    with contextlib.closing(requests.post(url=url, data=data, headers=headers)) as req:
        data = req.text
        return "succ", data


# get 请求
def request_get(url, params, headers):
    with contextlib.closing(requests.get(url=url, params=params, headers=headers)) as req:
        data = req.text
        return "succ", data


def get_time_stamp():
    return str(int(time.time() * 1000))


# 用于生成图片的 key
def get_key():
    '''
    cbuimgsearch/Z5Qja4fXPH1562293605000.jpg
    规则 是 cbuimgsearch/ 10位随机 + 毫秒级别时间戳
    :return:
    '''
    key = "cbuimgsearch/" + "".join(random.sample(chioce_list, 10)) + get_time_stamp()
    return key


def get_policy(filename):
    with open(filename, "rb") as f:
        data = f.read()
    return base64.b64encode(data)


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

    data = {
        "name": (None, filename),
        "key": (None, key),
        "policy": (None, policy),
        # 这个接口可以调用通过
        "OSSAccessKeyId": (None, OSSAccessKeyId),  # 这个接口可以调用通过
        "success_action_status": (None, "200"),
        "callback": (None, ""),
        "signature": (None, signature),  # 这个可以调用通过
        "file": open(filename, 'rb').read(),

    }
    return data, key


def get_dataset():
    url = 'https://open-s.1688.com/openservice/.htm?'

    params = {
        "callback": "jQuery18303374729635985685_" + str(int(time.time() * 1000)),
        "serviceIds": "cbu.searchweb.config.system.currenttime",
        "outfmt": "jsonp",
        "_": get_time_stamp()
    }

    headers = {
        "Host": 'open-s.1688.com',
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }

    status, data = request_get(url, params, headers)
    return status, data


def get_signature(data_set):
    url = 'https://open-s.1688.com/openservice/ossDataService'
    appkey = "{};{}".format('pc_tusou', str(data_set))

    params = {
        "appName": "pc_tusou",
        "appKey": base64.b64encode(appkey.encode("utf-8")),
        # 发生变化 pc_tusou;1562288848391 b64 编码 pc_tusou;毫秒级时间戳
        "callback": "jQuery18303536909897611926_{}".format(str(int(time.time() * 1000))),  # 需要判断
        "_": get_time_stamp(),  # 时间戳
        "": ""
    }

    headers = {
        "Host": 'open-s.1688.com',
        "Cache-Control": "no-cache",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }

    status, data = request_get(url, params, headers)
    data = data.split("(")[1].replace(');', '')

    result = json.loads(data)
    signature = result.get('data', {}).get('signature', '')
    policy = result.get('data', {}).get('policy', '')
    OSSAccessKeyId = result.get('data', {}).get('accessid', '')
    return status, signature, policy, OSSAccessKeyId


def upload_1688_image(filename, signature, policy, OSSAccessKeyId):
    url = 'https://cbusearch.oss-cn-shanghai.aliyuncs.com/'
    headers = get_headers()
    params, key = get_params(filename, signature, policy, OSSAccessKeyId)
    status, res = request_post_files(url, params, headers)
    return status, key


def get_1688_url(filename):
    '''
    1. 获取 需要 b64 编码的时间戳
    2. 获取 必须传输的参数 signature policy 同时将生成的 图片 key 返回
    3. 上传图片
    4. 拼接山骨干的徒留
    :param filename:
    :return:
    '''
    status, data = get_dataset()
    # todo 这里是一个优化的点，暂时没有找到 jQuery 返回结果的解析包
    data = data.split("(")[1].replace(');', '')
    data_set = json.loads(data).get('cbu.searchweb.config.system.currenttime', {}).get('dataSet', '')

    # 获取相关的 接口验证参数。同时 获取生成的 图片key
    status, signature, policy, OSSAccessKeyId = get_signature(data_set)

    # 上传图片
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
