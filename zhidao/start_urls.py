# -*- coding: utf-8 -*-
import json

tweets = []
for line in open('data_utf8_1_result.json', 'r'):   # 进行中的task
    tweets.append(json.loads(line))
    
    
count = 0
for tweet in tweets:
    print tweet['people_link']
    count += 1
    """
    for i in tweet['answers']:
        print i['people_link']
        count+=1
    """
    
print count
print tweet['people_link'][5]