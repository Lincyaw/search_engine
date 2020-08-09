# -*- coding: utf-8 -*-
import scrapy
import pickle
from Tieba import items


def md5(val):
    import hashlib
    ha = hashlib.md5()
    ha.update(bytes(val, encoding='utf-8'))
    key = ha.hexdigest()
    return key


class BaidutiebaSpider(scrapy.Spider):
    name = 'baidutieba'
    # 允许访问的域
    allowed_domains = ['tieba.baidu.com']
    # 爬取的起始地址
    start_urls = [f'https://tieba.baidu.com/f?kw=nba&ie=utf-8&pn={page*50}' for page in range(0, 2000)]
    # 将要爬取的地址列表
    destination_list = start_urls
    # 已爬取地址md5集合
    url_md5_seen = []
    # 断点续爬计数器
    counter = 0
    # 保存频率，每多少次爬取保存一次断点
    save_frequency = 50


    def parse(self, response):
        # 断点续爬功能之保存断点
        # self.counter_plus()

        root_url = "https://tieba.baidu.com/f?kw=nba&ie=utf-8&pn="

        # 爬取当前网页
        print('start parse : ' + response.url)
        print("开始了开始了")

        selectors = response.xpath('//*[@id="thread_list"]/li')
        print(selectors)
        if response.url.startswith("https://tieba.baidu.com/"):
            item = items.TiebaItem()
            for selector in selectors[2:]:
                url = selector.xpath(
                    './/div[@class="threadlist_title pull_left j_th_tit "]/a/@href').get()
                if url:  # 会员情况与非会员的xpath不一样, 判断一下非会员的是否读成功, 失败的话就表示是会员的, 要重新读一遍
                    url = "https://tieba.baidu.com" + url
                else:
                    url = selector.xpath(
                        './/div[@class="threadlist_title pull_left j_th_tit  member_thread_title_frs "]/a/@href').get()
                    url = "https://tieba.baidu.com" + url
                md5url = md5(url)
                if self.binary_md5_url_search(md5url) > -1:  # 存在当前MD5
                    print("有重复!!!!!!!!!!!!!!!")
                    pass
                else:
                    title = selector.xpath(
                        './/div[@class="threadlist_title pull_left j_th_tit  member_thread_title_frs "]/a/text()').get()
                    if not title:
                        title = selector.xpath('.//div[@class="threadlist_title pull_left j_th_tit "]/a/text()').get()
                    introduction = selector.xpath(
                        './/div[@class="threadlist_abs threadlist_abs_onlyline "]/text()').get()
                    introduction = introduction.strip()
                    author = selector.xpath(
                        './/span[@class="tb_icon_author "]//a[@rel="noreferrer"]/text()').get()
                    reply = selector.xpath(
                        './/span[@class ="threadlist_rep_num center_text"]/text()').get()
                    last_reply_time = selector.xpath(
                        './/span[@class ="threadlist_reply_date pull_right j_reply_data"]/text()').get()
                    last_reply_time = last_reply_time.strip()
                    item['title'] = title
                    item['introduction'] = introduction
                    item['author'] = author
                    item['reply'] = reply
                    item['last_reply_time'] = last_reply_time
                    item['url'] = url
                    item['urlmd5'] = md5(url)
                    # 索引构建flag
                    item['indexed'] = 'False'
                    self.binary_md5_url_insert(md5url)
                    self.destination_list.append(url)
                    print('已爬取网址数：' + (str)(len(self.destination_list)))
                    # yield it
                    yield item

                # print("title: " + title, count)
                # print("introduction: " + introduction)
                # print("author: ", author)
                # print("reply number: " + reply)
                # print("last reply time = " + last_reply_time)
                # print("url = ", url)
                # print(" \n")

        # for PAGE_NUMBER in range(100, 50000, 50):
        #     next_url = root_url + str(PAGE_NUMBER)
        #     #md5url = md5(url)
        #     #if self.binary_md5_url_search(md5url) > -1:    # 存在当前MD5
        #     #    pass
        #     #else:
        #     #    self.binary_md5_url_insert(md5url)
        #     # print(next_url)
        #     yield scrapy.Request(next_url, callback=self.parse, errback=self.errback_httpbin, dont_filter=True)
        #     # print(next_url)

        print("结束了")

    # scrapy.request请求失败后的处理
    def errback_httpbin(self, failure):
        print('Error 404 url deleted: ' + failure.request._url)


    # 二分法md5集合排序插入self.url_md5_set--16进制md5字符串集
    def binary_md5_url_insert(self, md5_item):
        low = 0
        high = len(self.url_md5_seen)
        while (low < high):
            mid = (int)(low + (high - low) / 2)
            if self.url_md5_seen[mid] < md5_item:
                low = mid + 1
            elif self.url_md5_seen[mid] >= md5_item:
                high = mid
        self.url_md5_seen.insert(low, md5_item)

    # 二分法查找url_md5存在于self.url_md5_set的位置，不存在返回-1
    def binary_md5_url_search(self, md5_item):
        low = 0
        high = len(self.url_md5_seen)
        if high == 0:
            return -1
        while (low < high):
            mid = (int)(low + (high - low) / 2)
            if self.url_md5_seen[mid] < md5_item:
                low = mid + 1
            elif self.url_md5_seen[mid] > md5_item:
                high = mid
            elif self.url_md5_seen[mid] == md5_item:
                return mid
        if low >= self.url_md5_seen.__len__():
            return -1
        if self.url_md5_seen[low] == md5_item:
            return low
        else:
            return -1
