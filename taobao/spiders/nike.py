# -*- coding: utf-8 -*-
import scrapy
import re

from taobao.items import TaobaoItem

class JdSpider(scrapy.Spider):
    name = "nike"
    allowed_domains = ["www.taobao.com"]
    start_urls = ['http://www.taobao.com/']


    search_url = 'https://s.taobao.com/search?q={key}&cat={cat}&p4ppushleft=1%2C48&bcoffset=3&ntoffset=3&s={index}'

    def start_requests(self):
        key = 'nike'
        cats = [50470026] #部分鞋子类别
        for cat in cats:

            for num in range(0,4400,44):
                yield scrapy.Request(url=self.search_url.format(key=key,cat=cat,page=num),callback=self.parse,dont_filter = True)


    def parse(self, response):
        all_goods = response.xpath('//div[@id="J_goodsList"]/ul/li')
        for one_good in all_goods:
            item = TaobaoItem()

            try:
                data = one_good.xpath('div/div/a/em')
                item['title'] = data.xpath('string(.)').extract()[0]#提取出该标签所有文字内容
                item['comment_count'] = one_good.xpath('div/div[@class="p-commit"]/strong/a/text()').extract()[0]#评论数
                item['goods_url'] = 'http:'+one_good.xpath('div/div[4]/a/@href').extract()[0]#商品链接
                item['shop_url'] = 'http:'+one_good.xpath('div/div[7]/span/a/@href').extract()[0]#店铺链接
                item['shops_id']=self.find_shop_id(item['shop_url'])#店铺ID
                goods_id=one_good.xpath('div/div[2]/div/ul/li[1]/a/img/@data-sku').extract()[0]
                if goods_id:
                    item['goods_id'] =goods_id
                price=one_good.xpath('div/div[3]/strong/i/text()').extract()#价格
                if price:#有写商品评论数是0，价格也不再源代码里面，应该是暂时上首页的促销商品，每页有三四件，我们忽略掉
                    item['price'] =float(price[0])


                yield item
            except Exception as e:
                pass
