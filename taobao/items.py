# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    comment_count=scrapy.Field()#评论数
    price =scrapy.Field()
    goods_url = scrapy.Field()
    shops_id = scrapy.Field()
    sales = scrapy.Field()
    is_tmall = scrapy.Field()
    shops_name = scrapy.Field()
    shops_loc = scrapy.Field()
    goods_id = scrapy.Field()
