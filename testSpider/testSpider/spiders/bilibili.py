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

    def parse(self, response):
        root_url = "https://tieba.baidu.com/f?kw=nba&ie=utf-8&pn="
        count = 0
        # 爬取当前网页
        print('start parse : ' + response.url)
        print("开始了开始了")
        selectors = response.xpath('//*[@id="thread_list"]/li')
        print(selectors)
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
            if url:   # 会员情况与非会员的xpath不一样, 判断一下非会员的是否读成功, 失败的话就表示是会员的, 要重新读一遍
                url = "https://tieba.baidu.com/"+url
            else:
                url = selector.xpath(
                    './/div[@class="threadlist_title pull_left j_th_tit  member_thread_title_frs "]/a/@href').get()
                url = "https://tieba.baidu.com/" + url
            print("title: "+title, count)
            print("introduction: "+introduction)
            print("author: ", author)
            print("reply number: "+reply)
            print("last reply time = "+last_reply_time)
            print("url = ", url)
            print(" \n")
            for PAGE_NUMBER in range(50):
                url = root_url + str(PAGE_NUMBER)
                print(url)

        print("结束了")





