# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduItem(scrapy.Item):
    '''
    img 表示贴吧头像
    name 表示贴吧名称
    user_num 表示关注人数
    topic_num 表示发帖数量
    tag 表示贴吧标签
    description 表示贴吧的描述
    url 表示贴吧链接
    '''
    title = scrapy.Field()
    tag = scrapy.Field()
    name = scrapy.Field()
    img = scrapy.Field()
    user_num = scrapy.Field()
    topic_num = scrapy.Field()
    description = scrapy.Field()
    url = scrapy.Field()

