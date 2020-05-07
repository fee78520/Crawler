# -*- coding: utf-8 -*-
import json
from scrapy import Spider, Request
from urllib.parse import urlencode

from imgs360.items import Imgs360Item


class ImagesSpider(Spider):
    name = 'images'
    allowed_domains = ['image.so.com']
    start_urls = ['http://image.so.com/']

    def start_requests(self):
        data = {'ch': 'photography', 'listtype': 'new'}
        base_url = 'https://image.so.com/zj?'
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page * 30
            params = urlencode(data)
            url = base_url + params
            yield Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for img in result.get('list'):
            item = Imgs360Item()
            item['id'] = img.get('id')
            item['url'] = img.get('qhimg_url')
            item['title'] = img.get('group_title')
            item['thumb'] = img.get('qhimg_thumb_url')
            yield item

