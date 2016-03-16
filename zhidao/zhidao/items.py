# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, Join, TakeFirst, Compose
#from scrapy.utils.makeup import remove_entities


class ZhidaoItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
# Zhidao User
class ZhiDaoU(Item):
    uid = Field(
        output_processor = TakeFirst()
        )  # hash(name)
    name = Field(
        output_processor = TakeFirst()
        )  
    url = Field(
        output_processor = TakeFirst()
        )
    the_best_answer_ratio = Field(
        output_processor = TakeFirst()
        ) #采纳率
    number_of_answers = Field(
        output_processor = TakeFirst()
        ) #回答数
    number_of_excellent_answers = Field(
        output_processor = TakeFirst()
        ) #回答被赞同数
    experience_points = Field(
        output_processor = TakeFirst()
        ) #经验值
    weath_points = Field(
        output_processor = TakeFirst()
        ) #财富值
    number_of_questions = Field(
        output_processor = TakeFirst()
        ) #提问数
    skilled_in_fields = Field(
        input_processor = MapCompose(unicode.strip),
        output_processor = Join() 
        ) #擅长领域
    zhidao_gift = Field(
        input_processor = MapCompose(unicode.strip),
        output_processor = Join() 
        ) #勋章
    zhidao_anwlist = Field(
        input_processor = MapCompose(unicode.strip),
        output_processor = Join() 
        ) #回答记录

class ZhiDaoQ(Item):
    qid = Field()  # 问题id
    class_info = Field()  # 问题分类
    ask_title = Field()
    content = Field()
    ask_time = Field()  # 提问时间
    ask_tags = Field()  # 问题tags标签，暂以 "," 分隔
    people_link = Field()  # 提问人链接
    answers = Field()

class ZhiDaoA(Item):
    mode = Field()  # 回答被分类型： 提问者采纳， 专业回答， 网友采纳， 普通回答
    pos_time = Field()  # 回答时间
    content = Field()
    people_link = Field()  # 回答人链接 
