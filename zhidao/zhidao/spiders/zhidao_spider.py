from scrapy import log # This module is useful for printing out debug information
from scrapy.spider import Spider
from zhidao.items import ZhiDaoU
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request
import exceptions
import json
import re

def generate_uid(user_name):
    return hash(user_name)

def get_all_qurl_list():
    q = []
    q_path = './zhihu_q.dat'
    q_file = open(q_path, 'r')
    for line in q_file.xreadlines():
        q.append(line.strip())
    return q

class ZhidaoSpider(Spider):
    name = "zhidao"
    allowed_domins = ["www.baidu.com"]
    start_urls = [
        "http://www.baidu.com/p/%E7%BF%85%E8%86%80%E5%A4%A9%E6%B6%AF?from=zhidao",
    ]
    def parse(self, response):
        u_loader = ItemLoader(item = ZhiDaoU(), response = response)
        u_loader.add_value('url', response.url)
        u_loader.add_xpath('the_best_answer_ratio', '//ul[@class="inline-list"]/li[1]/b/text()')
        #u_loader.add_css('name', '#\31 000000 > div.info-right > div.user-name.clearfix > h2')
        #print u_loader.load_item()

        yield u_loader.load_item()
        
        
