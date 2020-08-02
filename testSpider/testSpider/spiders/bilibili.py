import scrapy

# //li//div[@class="l-item"]

# //div[@class="r"]/a                       网址链接和标题
# //div[@class="r"]/div[@class="up-info"]/a 作者信息和链接
# //div[@class ="r"]//div[1]                简介
# //span[@class="v-info-i"][1]              播放量
# //span[@class="v-info-i"][2]              评论量


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    # 允许访问的域
    allowed_domains = ['bilibili.com/v/game/stand_alone/#/']
    # 爬取的起始地址
    start_urls = ['https://www.bilibili.com/v/game/stand_alone/?rt=V%2FymTlOu4ow%2Fy4xxNWPUZ3XqQ%2BU%2B%2FNnablrXdXaL%2Brk%3D']
    # start_urls = ['https://www.view.sdu.edu.cn']

    def parse(self, response):
        # 爬取当前网页
        print('start parse : ' + response.url)
        print("开始了开始了")
        selectors = response.xpath('//*[@id="videolist_box"]/div[2]/ul')
        print(selectors)
        for selector in selectors:
            title = selector.xpath('.//li/div[@class="l-item"]//div[@class="r"]/a/text()')
            up_info = selector.xpath('.//li/div[@class="l-item"]//div[@class="r"]/div[@class="up-info"]/a/text()')
            introduction = selector.xpath('.//li/div[@class="l-item"]//div[@class="r"]/div[1]/text()')
            print(title, up_info, introduction)
        print("结束了")



