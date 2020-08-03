import scrapy

# //li//div[@class="l-item"]

# //div[@class="r"]/a                       网址链接和标题
# //div[@class="r"]/div[@class="up-info"]/a 作者信息和链接
# //div[@class ="r"]//div[1]                简介
# //span[@class="v-info-i"][1]              播放量
# //span[@class="v-info-i"][2]              评论量
# //*[@id="thread_list"]/li[@class=" j_thread_list clearfix"]

class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    # 允许访问的域
    allowed_domains = ['tieba.baidu.com']
    # 爬取的起始地址
    start_urls = ['https://tieba.baidu.com/f?kw=nba&ie=utf-8&pn=0']
    # start_urls = ['https://www.view.sdu.edu.cn']
# class="threadlist_title pull_left j_th_tit"
    def parse(self, response):
        # 爬取当前网页
        print('start parse : ' + response.url)
        print("开始了开始了")
        selectors = response.xpath('//*[@id="thread_list"]/li[@class=" j_thread_list clearfix"]')
        print(selectors)
        for selector in selectors:
            title = selector.xpath('//div[@class="threadlist_title pull_left j_th_tit"]')
            print(title)
        print("结束了")

# //*[@id="thread_list"]/li[@class=" j_thread_list clearfix"]//div[@class="threadlist_lz clearfix"]

