# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 11:03
# @Author  : LiPengfei
# @File    : weibo_ajax.py

from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq


"""
微博要用ajax去请求
# ajax请求完整链接：
# https://m.weibo.cn/api/container/getIndex?uid=5051755960&luicode=10000011&lfid=1076035051755960&type=uid&value=5051755960&containerid=1076035051755960
第二页开始有since_id参数
每一页得since_id存在上一页得请求结果当中
"""

def get_data(since_id=''):

    headers = {
        'user-agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36""".replace(
            ' ', '')
    }

    params = {
        'uid': '5051755960',
        'luicode': '10000011',
        'lfid': '1076035051755960',
        'type': 'uid',
        'value': '5051755960',
        'containerid':'1076035051755960',
    }

    if since_id:
        params['since_id'] = since_id

    base_url = 'https://m.weibo.cn/api/container/getIndex?'

    url = base_url + urlencode(params)
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        return r.json()
    else:
        return None

def get_since_id(data):
    return data.get('data').get('cardlistInfo').get('since_id')


def parse_data(data):
    if data:
        for item in data.get('data').get('cards'):
            if 'mblog' in item:
                mblog = item.get('mblog')
                yield {
                    'id': mblog.get('id'),
                    'text': pq(mblog.get('text')).text(),
                    'attitudes': item.get('attitudes_count'),
                    'comments': item.get('comments_count'),
                    'reposts': item.get('reposts_count'),
                }


if __name__ == '__main__':
    since_id = ''
    pages = 3
    for page in range(pages):
        data = get_data(since_id=since_id)
        since_id = get_since_id(data)
        for val in parse_data(data):
            print(val)




