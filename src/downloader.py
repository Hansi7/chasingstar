#!/usr/bin/env python
# -*-coding:utf-8-*-

import requests
import url_manager


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.,2',
    'Accept-Encoding': 'gzip, deflate'
}


def get_html(url, Referer_url=None):
    '''get_html(url),download and return html'''
    if Referer_url:
        headers['Referer'] = Referer_url
    try:
        req = requests.get(url, headers=headers)
        return req.text
    except:
        print('Error Connection')
        url_manager.show()
        exit(0)


def get_image(url, Referer_url=None):
    if Referer_url:
        headers['Referer'] = Referer_url
    req = requests.get(url, headers=headers)
    return req.content


def save_image(url, filename, Referer_url=None):
    b_image = get_image(url, Referer_url)
    f = open(filename, 'wb')
    f.write(b_image)
    f.close()
