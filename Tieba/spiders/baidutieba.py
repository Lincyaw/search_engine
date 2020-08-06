# -*- coding: utf-8 -*-
import scrapy
import pickle
from Tieba import items


class BaidutiebaSpider(scrapy.Spider):
    name = 'baidutieba'
    # 允许访问的域
    allowed_domains = ['tieba.baidu.com']
    # 爬取的起始地址
    start_urls = ['https://tieba.baidu.com/f?kw=nba&ie=utf-8&pn=0']
    # 将要爬取的地址列表
    destination_list = start_urls
    # 已爬取地址md5集合
    url_md5_seen = []
    # 断点续爬计数器
    counter = 0
    # 保存频率，每多少次爬取保存一次断点
    save_frequency = 50

    # # 重写init
    # def __init__(self):
    #     super
    #     # 读取已保存的断点
    #     import os
    #     if not os.path.exists('./pause/'):
    #         os.mkdir('./pause/')
    #     if not os.path.isfile('./pause/response.seen'):
    #         f = open('./pause/response.seen', 'wb')
    #         f.close()
    #     if not os.path.isfile('./pause/response.dest'):
    #         f = open('./pause/response.dest', 'wb')
    #         f.close()
    #
    #     f = open('./pause/response.seen', 'rb')
    #     if os.path.getsize('./pause/response.seen') > 0:
    #         self.url_md5_seen = pickle.load(f)
    #     f.close()
    #     f = open('./pause/response.dest', 'rb')
    #     if os.path.getsize('./pause/response.dest') > 0:
    #         self.start_urls = pickle.load(f)
    #         self.destination_list = self.start_urls
    #     f.close()
    #     self.counter += 1

    def parse(self, response):
        # 断点续爬功能之保存断点
        # self.counter_plus()

        root_url = "https://tieba.baidu.com/f?kw=nba&ie=utf-8&pn="
        count = 0

        # 爬取当前网页
        print('start parse : ' + response.url)
        print("开始了开始了")

        selectors = response.xpath('//*[@id="thread_list"]/li')
        print(selectors)
        if response.url.startswith("https://tieba.baidu.com/"):
            item = items.TiebaItem()
            for selector in selectors[2:]:
                count = count + 1
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
                url = selector.xpath(
                    './/div[@class="threadlist_title pull_left j_th_tit "]/a/@href').get()
                if url:  # 会员情况与非会员的xpath不一样, 判断一下非会员的是否读成功, 失败的话就表示是会员的, 要重新读一遍
                    url = "https://tieba.baidu.com" + url
                else:
                    url = selector.xpath(
                        './/div[@class="threadlist_title pull_left j_th_tit  member_thread_title_frs "]/a/@href').get()
                    url = "https://tieba.baidu.com" + url
                item['title'] = title
                item['introduction'] = introduction
                item['author'] = author
                item['reply'] = reply
                item['last_reply_time'] = last_reply_time
                item['url'] = url

                # 索引构建flag
                item['indexed'] = 'False'

                # yield it
                yield item
                # print("title: " + title, count)
                # print("introduction: " + introduction)
                # print("author: ", author)
                # print("reply number: " + reply)
                # print("last reply time = " + last_reply_time)
                # print("url = ", url)
                # print(" \n")

        for PAGE_NUMBER in range(2, 300):
            url = root_url + str(PAGE_NUMBER)
            self.destination_list.append(url)
            print('已爬取网址数：' + (str)(len(self.destination_list)))
            yield scrapy.Request(url, callback=self.parse, errback=self.errback_httpbin)
            # print(url)

        print("结束了")

    # scrapy.request请求失败后的处理
    def errback_httpbin(self, failure):
        # self.destination_list.remove(failure.request._url)
        print('Error 404 url deleted: ' + failure.request._url)
        # self.counter_plus()

    # counter++，并在合适的时候保存断点
    def counter_plus(self):
        print('待爬取网址数：' + (str)(len(self.destination_list)))
        # 断点续爬功能之保存断点
        if self.counter % self.save_frequency == 0:  # 爬虫经过save_frequency次爬取后
            print('Rayiooo：正在保存爬虫断点....')

            f = open('./pause/response.seen', 'wb')
            pickle.dump(self.url_md5_seen, f)
            f.close()

            f = open('./pause/response.dest', 'wb')
            pickle.dump(self.destination_list, f)
            f.close()

            self.counter = self.save_frequency

        self.counter += 1  # 计数器+1


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