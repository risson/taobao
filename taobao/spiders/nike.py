# -*- coding: utf-8 -*-
import scrapy
import re
import json

from taobao.items import TaobaoItem

class TbSpider(scrapy.Spider):
    name = "nike"
    allowed_domains = ["www.taobao.com"]
    start_urls = ['http://www.taobao.com/']


    search_url = 'https://s.taobao.com/search?q={key}&cat={cat}&p4ppushleft=1%2C48&bcoffset=3&ntoffset=3&s={index}'

    def start_requests(self):
        key = 'nike'
        cats = [50470026,50470025,50468018,50484019,50484020] #部分鞋子类别
        for cat in cats:

            for num in range(0,4400,44):
                yield scrapy.Request(url=self.search_url.format(key=key,cat=cat,index=num),callback=self.parse,dont_filter = True)


    def parse(self, response):
        html = response.text
        content = re.findall(r'g_page_config = (.*?) g_srp_loadCss',html,re.S)[0].strip()[:-1]
        #格式化
        content = json.loads(content)

        item = TaobaoItem()

        #获取信息列表
        data_list = content['mods']['itemlist']['data']['auctions']

        #提取数据
        for data in data_list:
            try:
                item['title'] = data['raw_title']
                item['price'] = float(data['view_price'])
                pattern = re.compile(r'\d+')
                item['sales'] = int(pattern.findall(data['view_sales'])[0])
                item['is_tmall'] = '是' if data['shopcard']['isTmall'] else '否'
                item['shops_loc'] = data['item_loc']
                item['shops_name'] = data['nick']
                item['shops_id'] = data['user_id']
                item['goods_url'] = 'http'+data['detail_url']
                item['comment_count'] = int(data['comment_count'])
                item['goods_id'] = data['nid']

                yield item
            except Exception as e:
                pass
