from scrapy import log
from proxy import PROXIES
from agents import AGENTS

import random
import base64


class ProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass            
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

class ProxyMiddleware2(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = "http://127.0.0.1:8087"

      

class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent
