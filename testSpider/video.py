# -*- coding: utf-8 -*-
import scrapy

class VideoSpider(scrapy.Spider):
    name = 'video'
    # 允许访问的域
    allowed_domains = ['movie.douban.com/review/best/']
    # 爬取的起始地址
    start_urls = [
        'https://movie.douban.com/review/best/?start=0']

    # start_urls = ['https://www.view.sdu.edu.cn']

    def parse(self, response):
        # 爬取当前网页
        print('start parse : ' + response.url)
        #if response.url.startswith("https://www.view.sdu.edu.cn/info/"):
        #print("BEGIN")
        #html_new = response.replace(r'<!--', '"').replace(r'-->', '"')
        #selectors = html_new.xpath('//*[@id="videolist_box"]/div[2]/ul/li')
        selectors = response.xpath('//*[@id="content"]/div/div[1]/div[1]/div')
        print(response.xpath('//*[@id="review_12768994_short"]/div/text()[1]').get())
        print(len(selectors))
        if selectors:
            for selector in selectors:
                #author = selector.xpath('.//header[@class="main-hd"]/a[@class="name"]/text()').get()
                author = selector.xpath('./div/header/span[@class="main-meta"]/text()').get()
                up_info = selector.xpath('.//a[@class="action-btn up"]/span/text()').get().strip()#extract()[0].strip()
                introduction = selector.xpath('./div/div/h2/a/text()').get()
                #review = selector.xpath('./div/div/div[1]/div/text()').get()
                review = selector.xpath('./div/div/div[1]/div/p/text()').get()
                if review:
                    review = selector.xpath('./div/div/div[1]/div/text()[1]').get().strip()
                    review = review.replace(u'\xa0', u' ')
                else:
                    review = selector.xpath('./div/div/div[1]/div/text()').get().strip()
                    review = review.replace(u'\xa0', u' ')
                #print(type(review))
                #if review == 'NULL':
                 #   review = selector.xpath('./div/div/div[1]/div//p/text()').get()
                #else:
                 #   review = review.strip()
                  #  review = review.replace(u'\xa0', u' ')
                #up_info = up_info.strip()
                print(author)
                print(up_info)
                print(introduction)
                print(review)
        #print("finish")

        #else:
         #   print("can not find")
