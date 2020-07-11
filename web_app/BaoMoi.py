import scrapy
import json
import os
import csv

class BaoMoi(scrapy.Spider):
    name = "baomoi"
    allowed_domains = ['baomoi.com']
    
    # start_id = 35565971
    # end_id = 35565959

    def __init__(self, start_id, end_id, *args, **kwargs):
        super(BaoMoi, self).__init__(*args, **kwargs)
        if (start_id > end_id):
            self.start_id = int(start_id)
            self.end_id = int(end_id)
        else:
            self.start_id = int(end_id)
            self.end_id = int(start_id)
        
        if os.path.exists("crawl.csv"):
            os.remove("crawl.csv")

    def start_requests(self):
        while self.start_id >= self.end_id:
            url = 'https://baomoi.com/c/' + str(self.start_id) + '.epi'
            yield scrapy.Request(url=url, callback=self.parse, meta = {'dont_redirect': True, 'handle_httpstatus_list': [302]})

    def parse(self, response):
        if (str(response.body) != "b''"):
            item = BaomoiItem()
            item['title'] = response.xpath("//h1[@class='article__header']/text()")[0].extract().strip()
            item['summary'] = response.xpath("////div[@class='article']/div[@class='article__sapo']/text()")[0].extract().strip() 
            item['content'] = ' '.join(str(s).strip() for s in response.xpath("//div[@class='article__body']/p[@class='body-text']/text()").extract())
            item['writtenTime'] = response.xpath("//time[@class='time']/text()")[0].extract().strip()
            item['url'] = response.url
            item['category'] = response.xpath("//a[@class='cate'][1]/text()")[0].extract().strip()
            item['tag'] = ' '.join(str(x).strip().replace('"','\\"') for x in response.xpath("//div[@class='article__tag']/p/a[@class='keyword']/text()").extract())
            item['source'] = response.xpath("//div[@class='article']/div[@class='article__meta']/a[@class='source']/text()")[1].extract().strip()
            yield item
        self.start_id = self.start_id - 1   
    
class BaomoiItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    summary = scrapy.Field()
    content = scrapy.Field()
    writtenTime = scrapy.Field()
    url = scrapy.Field()
    category = scrapy.Field()
    tag = scrapy.Field()
    source = scrapy.Field()
    pass