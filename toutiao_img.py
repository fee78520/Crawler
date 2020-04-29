# -*- coding: utf-8 -*-
# @Time    : 2020/4/29 19:23
# @Author  : LiPengfei
# @File    : toutiao_img.py

import requests
from urllib.parse import urlencode
import re
import os
from hashlib import md5
import json


headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.106 Safari/537.36',
    'cookie': 'tt_webid=6689770852458677768; WEATHER_CITY=%E5%8C%97%E4%BA%AC; UM_distinctid=16aa738630e890-02daeed22a3bba-f353163-1fa400-16aa738630f86c; tt_webid=6689770852458677768; csrftoken=85f646aac651995d0f0d477d9e1000b1; s_v_web_id=a9c80360734866fb880cd48244e4d2e3; CNZZDATA1259612802=1806456525-1557579889-https%253A%252F%252Fwww.baidu.com%252F%7C1557585289; __tasessionId=b9cl244be1557590374034; passport_auth_status=be3918f20b2cefdeae2de53331bb068a; sso_uid_tt=9364aef949fb1422b0d8445d87b9adb1; toutiao_sso_user=08d9d869618fc319637f6e2e11d3981e; login_flag=a7eae77d77aac773723e3468446bfa02; sessionid=7bf2d480f660db06fd489845e59608a1; uid_tt=555598b2d1b7b155f07da91a6fd45192; sid_tt=7bf2d480f660db06fd489845e59608a1; sid_guard="7bf2d480f660db06fd489845e59608a1|1557590405|15552000|Thu\054 07-Nov-2019 16:00:05 GMT'
}

def get_data(offset, keyword):#获取主页面

    params = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'from': 'search_tab',
        'pd': 'synthesis',
        'timestamp': 1588144413451,
    }
    url = "https://www.toutiao.com/api/search/content/?" + urlencode(params)
    try:
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            res = r.json()
            return res
    except:
        print('访问错误')
        return None

def parse_page(data):
    """
    获取详情页面的url
    :param data:
    :return:
    """
    if data and 'data' in data:
        for item in data.get('data'):
            article_url = item.get('article_url')
            if article_url and 'toutiao' in article_url:
                yield article_url

def get_detail_page(detail_url):
    try:
        headers = {
            'cookie': 'tt_webid=6813916869096883719; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6813916869096883719; csrftoken=8b531c6788e3416b8e59d2048a440b64; __tasessionId=5ad20pc991588150876450; s_v_web_id=verify_k9jirdyu_v9i5R5cz_EvTp_4YpZ_8UFB_fcmEfKpHBW84',
            'user-agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36""".replace(
            ' ', '')}

        response = requests.get(detail_url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except:
        return None


def get_img_urls(html):
    image_pattern = re.compile('gallery: JSON.parse\("(.*)"\)', re.S)
    result = re.search(image_pattern, html)
    if result:
        data = json.loads(result.group(1).replace('\\', ''))
        img_urls = [i.get('url') for i in data.get('sub_images')]
        img_urls = [i.replace('u002F', '/') for i in img_urls]
        return img_urls
    else:
        print('图片链接获取失败')
        return None


def download_image(image):
    try:
        headers = {
            'cookie': 'tt_webid=6813916869096883719; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6813916869096883719; csrftoken=8b531c6788e3416b8e59d2048a440b64; __tasessionId=5ad20pc991588150876450; s_v_web_id=verify_k9jirdyu_v9i5R5cz_EvTp_4YpZ_8UFB_fcmEfKpHBW84',
            'user-agent': """Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36""".replace(
            ' ', '')}
        response = requests.get(image, headers=headers)
        if response.status_code == 200:
            data = response.content
            return data
        return None
    except:
        print('请求图片失败')

def save_image(url):
    data = download_image(url)
    path = '../data/'
    if not os.path.exists(path):
        os.makedirs(path)
    file_path = '%s%s.jpg' %(path, md5(data).hexdigest())
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(data)
            f.close()
            print('保存成功')


if __name__ == '__main__':
    data = get_data(0, '街拍')
    urls = parse_page(data)
    for url in urls:
        html = get_detail_page(url)
        img_urls = get_img_urls(html)
        if img_urls:
            for img_url in img_urls:
                save_image(img_url)
        # else:
        #     print(html)


