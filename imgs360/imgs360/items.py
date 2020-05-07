# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class Imgs360Item(Item):
    table = 'images'
    # collection = table = 'images'
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    url = Field()
    title = Field()
    thumb = Field()






