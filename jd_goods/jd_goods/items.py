# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class JdGoodsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 产品id
    id = scrapy.Field()
    # 产品的文字描述
    describition = scrapy.Field()
    # 价格
    price = scrapy.Field()
    # 颜色
    color = scrapy.Field()
    # 内存+ROM
    memories = scrapy.Field()
    # 套餐版本
    version = scrapy.Field()
    # 产品图片
    img_url = scrapy.Field()
