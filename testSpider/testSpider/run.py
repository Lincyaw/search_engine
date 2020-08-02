from scrapy import cmdline

cmdline.execute("scrapy crawl bilibili".split())
# cmdline.execute("scrapy crawl SduViewSpider -s JOBDIR=crawls/somespider-1".split())