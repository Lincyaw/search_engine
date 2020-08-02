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
    start_urls = ['https://www.bilibili.com/v/game/stand_alone/#/all/default/0/1/']

    def parse(self, response):
        # 爬取当前网页
        print('start parse : ' + response.url)
        # self.destination_list.remove(response.url)
        if response.url.startswith("https://www.bilibili.com/v/game/"):
            for box in response.xpath('//li//div[@class="l-item"]'):
                title = box.xpath('//div[@class="r"]/a/text()').extract_first()
                up_info = box.xpath('//div[@class="r"]/div[@class="up-info"]/a/text()').extract_first()
                introduction = box.xpath('//div[@class ="r"]//div[1]/text()').extract_first()
                print(title, up_info, introduction)
