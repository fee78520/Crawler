# -*- coding: utf-8 -*-
# @Time    : 2020/4/27 19:04
# @Author  : LiPengfei
# @File    : my_top100.py


import requests
import re
import json


def get_one_page(url):
    headers = {
        'User-Agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) 
                         Chrome/80.0.3987.149 Safari/537.36""".replace(' ', '').replace('\n', '')
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        return None


def parse_html(html):
    i_re_s = '<dd>.*?board-index.*?>(.*?)</i>'
    img_re_s = '.*?data-src="(.*?)"'
    t_re_s = '.*?name.*?a.*?>(.*?)<'
    zy_re_s = '.*?star">(.*?)<'
    time_re_s = '.*?releasetime.*?>(.*?)<'
    int_re_s = '.*?integer.*?>(.*?)<'
    fra_re_s = '.*?fraction.*?>(.*?)<'

    all_re_s = i_re_s + img_re_s + t_re_s + zy_re_s + time_re_s + int_re_s + fra_re_s

    all_pattern = re.compile(all_re_s, re.S)
    all_items = re.findall(all_pattern, html)
    print(all_items)

    for item in all_items:
        yield {
            'index': item[0],
            'image': item[1],
            'title': item[2].strip(),
            'actor': item[3][3:].strip() if len(item[3])>3 else '',
            'time': item[4],
            'score': item[5] + item[6],
        }


def write_file(data, file):
    with open(file, 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')


def main(offset):
    url = 'http://maoyan.com/board/4?offset=%s' %offset
    html = get_one_page(url)
    for item in parse_html(html):
        print(item)
        write_file(item, 'my_top100.txt')


if __name__ == '__main__':
    for n in range(10):
        main(n*10)


