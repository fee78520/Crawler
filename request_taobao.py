# -*- coding: utf-8 -*-
# @Time    : 2020/5/12 10:14
# @Author  : LiPengfei
# @File    : request_taobao.py


import requests
import re

def getHTMLText(url):
    try:
        headers = {
            'authority': 's.taobao.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://s.taobao.com/search?q=ipad&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20200512&ie=utf8',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 't=49526c1bf84cc8b915043a2efd2288f8; cna=vD+rFuh92GYCAXWEwrAyMiOD; lgc=%5Cu670B%5Cu98DE%5Cu670B; tracknick=%5Cu670B%5Cu98DE%5Cu670B; enc=fajo8rXVmhfJU%2FLcDHIM2tk7OktjgQTpMFkOo6VvrHSN6eltWHo9NQEatfruEp4Ox9Zpl%2BEsnexLZ1tQ9Dl7ig%3D%3D; miid=921962071301117531; thw=cn; hng=CN%7Czh-CN%7CCNY%7C156; sgcookie=EIwUvJ4ax%2Bcanir3RZBa%2F; uc3=nk2=pmT%2BbvMD&id2=UU6gaQnHJV2l3w%3D%3D&vt3=F8dBxGR%2BNS52XUWEcGA%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; uc4=nk4=0%40pKtAZA6XN2KMima8%2B8S9%2By8%3D&id4=0%40U2xt8aP7QFTblSU0kyZ4VoiiaT64; _cc_=Vq8l%2BKCLiw%3D%3D; tfstk=cm_OBJt1fJ2MuE1w4ZEHlQfPvMPlZWyvdf9mkSZOJaMYVC3AiS_lygtufIM9JWC..; _m_h5_tk=0de9a4d9058ffb7e09ff10912c6c0077_1588858525414; _m_h5_tk_enc=170b6e585e92c381f12a16bae5d98d4c; mt=ci=-1_0; v=0; cookie2=1709e4d0fff1dcb4ea6635ca85612d0d; _tb_token_=e36af0be7fe87; _samesite_flag_=true; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=4EB498141448C9D66AF6C71AA56D5134; uc1=cookie14=UoTUM2LLX687yg%3D%3D; isg=BJ2dqnzEn4ZB6nuyHugq4GnfrHmXutEM8WKGZl9iGPQjFr9IJw_v3CPEQAoQ1unE; l=eBj-Xiq7Q-pGy4HsBO5aFurza77OrIRbzsPzaNbMiInGa6sltFGaeNQc7ZL6SdtjgtCXLetzEdARfRUXrMzdg2HvCbKrCyCuCxJO.',
        }

        r = requests.get(url, headers=headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""


def parsePage(ilt, html):
    try:
        plt = re.findall(r'\"view_price\":\"[\d+\.]*\"', html)
        tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)
        for i in range(len(plt)):
            price = eval(plt[i].split(':')[1])
            title = eval(tlt[i].split(':')[1])
            ilt.append([price, title])
    except:
        print("F")


def printGoodsList(ilt):
    tplt = "{:4}\t{:8}\t{:16}"
    print(tplt.format("序号", "价格", "商品名称"))
    count = 0
    for g in ilt:
        count = count + 1
        print(tplt.format(count, g[0], g[1]))


def main():
    goods = 'ipad'
    depth = 2
    start_url = "https://s.taobao.com/search?q=" + goods
    infoList = []
    for i in range(depth):
        try:
            url = start_url + '&s=' + str(44 * i)
            html = getHTMLText(url)
            parsePage(infoList, html)
        except:
            continue
    printGoodsList(infoList)

if __name__ == '__main__':
    main()



