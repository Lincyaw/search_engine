# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TiebaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    author = scrapy.Field()
    reply = scrapy.Field()
    last_reply_time = scrapy.Field()
    introduction = scrapy.Field()
    indexed = scrapy.Field()  # 索引构建过了没有的flag
    urlmd5 = scrapy.Field()
