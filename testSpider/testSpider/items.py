# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TestspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    newsTitle = scrapy.Field()
    newsUrl = scrapy.Field()
    newsUrlMd5 = scrapy.Field()
    newsClick = scrapy.Field()
    newsPublishTime = scrapy.Field()
    newsContent = scrapy.Field()
    indexed = scrapy.Field()    # 索引构建过了没有的flag
