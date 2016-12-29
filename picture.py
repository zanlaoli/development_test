#!/usr/bin/env python
# ! -*- coding: utf-8 -*-
import http.client
import re
import urllib

from check import check


def get_picture_url(word):
    conn = http.client.HTTPSConnection("image.baidu.com", timeout=5)
    headers = {'User-Agent': "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}
    url = urllib.parse.urlencode({
        'tn': "baiduimage",
        'ps': 1,
        'ct': 201326592,
        'lm': -1,
        'cl': 2,
        'ie': 'utf-8',
        'word': word
    })
    conn.request("GET",
                 "/search/index?%s" % url, headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")

    # print(data)
    pattern = re.compile(r'"objURL":"(.*?)"')
    imgSrcHtml = pattern.findall(data)
    return imgSrcHtml[0]  # 为提高速度 暂不做复查
    # index = 0
    # for item in imgSrcHtml:  # 对爬到的图片进行复查 采用经过识图后关键词与原关键词能联想上的图片 为了防止遇到太生僻的关键词太慢 只复查五次
    #     if check(item.replace('\'', ''), word):
    #         return imgSrcHtml[index]
    #     if index >= 5:
    #         return imgSrcHtml[0]
    #     index += 1
