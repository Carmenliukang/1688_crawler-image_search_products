# !/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2019-07-18 11:58
# @Author  : liukang.hero
# @FileName: func_txy.py

import os
import io
import json
import time
import base64
import random
import requests
import contextlib
from lib.logger import logger
from requests_toolbelt import MultipartEncoder

chioce_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'W', 'X', 'Y', 'Z',
               'a', 'b', 'c', 'd', 'e', 'f', 'h', 'i', 'j', 'k', 'm', 'n', 'p', 'r', 's', 't', 'w', 'x', 'y', 'z', '2',
               '3', '4', '5', '6', '7', '8']


def request_post(url, data, headers):
    try:
        with contextlib.closing(requests.post(url=url, data=data, headers=headers)) as req:
            res = req.text
            logger.info("requests post:\n\turl:{}\n\tdata:{}\n\tresult:{}".format(url, data, res))
            return "succ", res
    except Exception as e:
        print(e)
        logger.info("requests post err:\n\turl:{}\n\tdata:{}\n\terr:{}".format(url, data, e))
        return "fail", {}


def request_get(url, params, headers):
    try:
        with contextlib.closing(requests.get(url=url, params=params, headers=headers)) as req:
            data = req.text
            logger.info("requests get:\n\turl:{}\n\tparams:{}\n\tresult:{}".format(url, params, data))
            return "succ", data
    except Exception as e:
        print(e)
        logger.info("requests get err:\n\turl:{}\n\tdata:{}\n\terr:{}".format(url, params, e))
        return "fail", {}


def get_reuqest_data(url):
    headers = {
        'user-agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }
    try:
        with contextlib.closing(requests.get(url=url, headers=headers, stream=True)) as req:
            content = req.content
            content = io.BytesIO(content).read()
        return content
    except Exception as e:
        print(e)
        return ""


def get_headers():
    headers = {
        'Origin': "https://www.1688.com",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
    }
    return headers


def get_file_data(filename):
    with open(filename, 'rb') as f:
        data = f.read()
        return data


def get_key():
    '''
    cbuimgsearch/Z5Qja4fXPH1562293605000.jpg 生活规则是 cbuimgsearch/ + 随机10位 + 毫秒级别时间戳
    :return:
    '''
    key = "cbuimgsearch/" + "".join(random.sample(chioce_list, 10)) + str(int(time.time() * 1000))
    return key


def get_params_by_filename(filename, signature, policy, OSSAccessKeyId):
    key = get_key()
    name = "".join(random.sample(chioce_list, 5)) + ".jpg"
    file_payload = {
        "name": name,
        "key": key,
        "policy": policy,
        "OSSAccessKeyId": OSSAccessKeyId,
        "success_action_status": "200",
        "callback": "",
        "signature": signature,
        "file": get_file_data(filename),
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

    status, data = request_get(url, params, get_headers())
    return status, data, callback


def get_signature_result_manage(data, callback):
    json_str = data.replace("{}(".format(callback), "").replace(");", '')
    result = json.loads(json_str)
    signature = result.get('data', {}).get('signature', '')
    policy = result.get('data', {}).get('policy', '')
    OSSAccessKeyId = result.get('data', {}).get('accessid', '')
    return signature, policy, OSSAccessKeyId


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

    status, data = request_get(url, params, get_headers())

    signature, policy, OSSAccessKeyId = get_signature_result_manage(data, callback)

    return status, signature, policy, OSSAccessKeyId


def get_params_by_url(image_url, signature, policy, OSSAccessKeyId):
    key = get_key()
    name = "".join(random.sample(chioce_list, 5)) + ".jpg"
    file_payload = {
        "name": name,
        "key": key,
        "policy": policy,
        "OSSAccessKeyId": OSSAccessKeyId,
        "success_action_status": "200",
        "callback": "",
        "signature": signature,
        "file": get_reuqest_data(image_url)
    }

    m = MultipartEncoder(file_payload)

    headers = get_headers()
    headers['Content-Type'] = m.content_type
    return m, headers, key


def upload_1688_image_by_url(image_url, signature, policy, OSSAccessKeyId):
    '''
    上传文件。这里使用的是 MultipartEncoder 包，更加便捷生成 multipart/form-data 类型的body
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundarybsKUYKw7Wu6nNEAG
    :param image_url: 图片的URL链接
    :param signature:必须参数，通过 调用 https://open-s.1688.com/openservice/ossDataService 获取。
    :param policy:必须参数，通过 调用 https://open-s.1688.com/openservice/ossDataService 获取。
    :param OSSAccessKeyId:必须参数，通过 调用 https://open-s.1688.com/openservice/ossDataService 获取。
    :return: status fail|succ key图片唯一ID
    '''
    url = 'https://cbusearch.oss-cn-shanghai.aliyuncs.com/'

    m, headers, key = get_params_by_url(image_url, signature, policy, OSSAccessKeyId)

    status, res = request_post(url, m, headers)

    return status, key


def upload_1688_image_by_filename(filename, signature, policy, OSSAccessKeyId):
    '''
    上传文件。这里使用的是 MultipartEncoder 包，更加便捷生成 multipart/form-data 类型的body
    Content-Type: multipart/form-data; boundary=----WebKitFormBoundarybsKUYKw7Wu6nNEAG
    :param image_url: 图片的URL链接
    :param signature:必须参数，通过 调用 https://open-s.1688.com/openservice/ossDataService 获取。
    :param policy:必须参数，通过 调用 https://open-s.1688.com/openservice/ossDataService 获取。
    :param OSSAccessKeyId:必须参数，通过 调用 https://open-s.1688.com/openservice/ossDataService 获取。
    :return: status fail|succ key图片唯一ID
    '''
    url = 'https://cbusearch.oss-cn-shanghai.aliyuncs.com/'

    m, headers, key = get_params_by_filename(filename, signature, policy, OSSAccessKeyId)

    status, res = request_post(url, m, headers)

    return status, key


def get_image_file_name(image_dir_path):
    '''
    # 获取image 文件
    :param image_dir_path: 文件路径
    :return:
    '''
    image_files_list = []
    for file in os.listdir(image_dir_path):
        file_path = os.path.join(image_dir_path, file)

        if not os.path.isdir(file_path) and os.path.splitext(file_path)[1] in ['.jpg', '.jpeg', ".png"]:
            image_files_list.append(file_path)

    return image_files_list
