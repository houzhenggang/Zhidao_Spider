# -*- coding: utf-8 -*-

from scrapy import log # This module is useful for printing out debug information
from scrapy.spiders import Spider
from zhidao.items import ZhiDaoU
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
import exceptions
import json
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import selenium.webdriver.support.ui as ui
from scrapy.http import TextResponse 
import time

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
    
    def __init__(self):
        #CrawlSpider.__init__(self)
        # use any browser you wish
        self.driver = webdriver.Chrome() 
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    
    def spider_closed(self, spider):
        self.driver.close()
    
    #def __del__(self):
    #    self.browser.close()
    
    
    def parse(self, response):
        #start browser
        self.driver.get(response.url)
        #loading time interval
        time.sleep(5)
        while True:
            #next = self.driver.find_element_by_link_text("\u4e0b\u4e00\u9875")
            #next = WebDriverWait(self.driver, 10).until(
            #    EC.visibility_of_element_located((By.LINK_TEXT, "\u4e0b\u4e00\u9875")))
            next = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.LINK_TEXT, "5")))
            try:
                next.click()
            except:
                break
  
        response = TextResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        
        u_loader = ItemLoader(item = ZhiDaoU(), response = response)
        u_loader.add_value('url', response.url)
        #基本信息
        u_loader.add_xpath('the_best_answer_ratio', '//ul[@class="inline-list"]/li[1]/b/text()')
        u_loader.add_xpath('number_of_answers', '//ul[@class="inline-list"]/li[2]/b/text()')
        u_loader.add_xpath('number_of_excellent_answers', '//ul[@class="inline-list"]/li[3]/b/text()')
        u_loader.add_xpath('experience_points', '//ul[@class="inline-list"]/li[4]/b/text()')
        u_loader.add_xpath('weath_points', '//ul[@class="inline-list"]/li[5]/b/text()')
        u_loader.add_xpath('number_of_questions', '//ul[@class="inline-list"]/li[6]/b/text()')
        
        u_loader.add_xpath('skilled_in_fields', '//*/div[@class="zhidao-good clearfix p3 b2"]/ul/li/span/a/text()')
        u_loader.add_xpath('zhidao_gift', '//*/div[@class="zhidao-gift clearfix p3 b2"]/ul/li/a/@title')
        u_loader.add_xpath('zhidao_anwlist', '//*/div[@class ="zhidao-anwlist"]/table/tbody/tr/td/a/@href')
        
        #u_loader.add_xpath('name', "")
        #u_loader.add_css('name', '#\31 000000 > div.info-right > div.user-name.clearfix > h2')
        #print u_loader.load_item()

        yield u_loader.load_item()
        
        
