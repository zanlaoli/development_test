#!/usr/bin/env python
# ! -*- coding: utf-8 -*-
import http.client
import re
import urllib
import json


def check(pic_url, word):
    result = list()
    conn = http.client.HTTPSConnection("image.baidu.com", timeout=5)
    headers = {'User-Agent': "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}
    url = urllib.parse.urlencode({
        'queryImageUrl': pic_url
    })
    conn.request("GET", "/n/pc_search?%s" % url, headers=headers)
    try:
        res = conn.getresponse()
        data = res.read().decode("utf-8")
    except Exception:
        return False
    pattern = re.compile(r"\'guessWord\': \'(.*?)\'")
    guess_word = pattern.findall(data)
    if len(guess_word) > 0:
        return check_suggest(word, guess_word)  # 做语义联想分析
    else:
        return False


def check_suggest(word, guess_words):
    conn = http.client.HTTPConnection("api.bosonnlp.com")

    payload = '\"' + word + '\"'

    headers = {
        'accept': "application/json",
        'x-token': "D4kzWL2C.10867.LravVg7ReFAI"
    }

    conn.request("POST", "/suggest/analysis?top_k=10", payload.encode('utf-8'), headers)

    suggest = list()
    for item in json.loads(conn.getresponse().read().decode("utf-8")):
        suggest.append(item[1].replace('/n', ''))

    for guess_word in guess_words:
        if guess_word in suggest:
            return True
        else:
            return False
