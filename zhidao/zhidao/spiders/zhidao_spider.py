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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#import selenium.webdriver.support.ui as ui
from scrapy.http import TextResponse, HtmlResponse
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
    """
    start_urls = [
        #"http://www.baidu.com/p/%E7%BF%85%E8%86%80%E5%A4%A9%E6%B6%AF?from=zhidao",
        "http://www.baidu.com/p/cangxiongyou?from=zhidao",
        #"http://www.baidu.com/p/%E7%99%BD%E7%BE%8A%E5%A4%AA%E5%8F%94?from=zhidao",
    ]
    """
    def __init__(self):
        #CrawlSpider.__init__(self)
        self.start_urls = []
        tweets = []
        for line in open('data_utf8_1_result.json', 'r'):   
            tweets.append(json.loads(line))
        for tweet in tweets:
            #asker_link
            """
            url = tweet['people_link']
            if (url.startswith('http')):       
                    self.start_urls.extend([url])   #asker_link
            #print tweet['people_link']
            """
            # answerer_link
            for i in tweet['answers']:
                url = i['people_link']
                if (url.startswith('http')):       
                    self.start_urls.extend([url]) #answerer_link
                #print i['people_link']
            
        # use any browser you wish
        self.driver = webdriver.Chrome() 
        #self.driver = webdriver.PhantomJS(r'D:\phantomjs.exe')
        dispatcher.connect(self.spider_closed, signals.spider_closed)
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)
    
    def spider_closed(self, spider):
        #self.driver.close()
        self.driver.quit()
           
    def parse(self, response):
        #start browser
        self.driver.get(response.url)
        #loading time interval
        time.sleep(5)
        while True:
            try:
                next = WebDriverWait(self.driver, 5).until(
                    EC.visibility_of_element_located((By.LINK_TEXT, u'\u4e0b\u4e00\u9875')))  #Unicode 前加u''
            #try:
            #if (next):
                print "------------------find next-------------"
                next.click()
                time.sleep(3)
            except:
                break
        
  
        response = HtmlResponse(url=response.url, body=self.driver.page_source, encoding='utf-8')
        
        #from scrapy.shell import inspect_response  
        #inspect_response(response, self)  
        
        u_loader = ItemLoader(item = ZhiDaoU(), response = response)
        u_loader.add_value('url', response.url)
        #基本信息
        u_loader.add_xpath('name', '//h2[@class="yahei"]/text()')
        u_loader.add_value('uid', generate_uid(u_loader.get_output_value('name')))
        u_loader.add_xpath('the_best_answer_ratio', '//ul[@class="inline-list"]/li[1]/b/text()')
        u_loader.add_xpath('number_of_answers', '//ul[@class="inline-list"]/li[2]/b/text()')
        u_loader.add_xpath('number_of_excellent_answers', '//ul[@class="inline-list"]/li[3]/b/text()')
        u_loader.add_xpath('experience_points', '//ul[@class="inline-list"]/li[4]/b/text()')
        u_loader.add_xpath('weath_points', '//ul[@class="inline-list"]/li[5]/b/text()')
        u_loader.add_xpath('number_of_questions', '//ul[@class="inline-list"]/li[6]/b/text()')
        
        u_loader.add_xpath('skilled_in_fields', '//*/div[@class="zhidao-good clearfix p3 b2"]/ul/li/span/a/text()')
        u_loader.add_xpath('zhidao_gift', '//*/div[@class="zhidao-gift clearfix p3 b2"]/ul/li/a/@title')
        u_loader.add_xpath('zhidao_anwlist', '//*/div[@class ="zhidao-anwlist"]/table/tbody/tr/td/a/@href')
        
        yield u_loader.load_item()
        
        
