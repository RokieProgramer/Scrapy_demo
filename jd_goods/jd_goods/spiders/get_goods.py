# -*- coding: utf-8 -*-
import scrapy
from jd_goods.items import JdGoodsItem
from urllib.parse import urlencode
import re
import json


class GetGoodsSpider(scrapy.Spider):
    name = 'get_goods'
    # allowed_domains = ['jd.com']
    # https://search.jd.com/Search?keyword=huwwei_p30pro

    def start_requests(self):
        # keyword = input("请输入想要查询的物品：")
        # max_page = int(input('请输入想要爬取的最大页面数：'))
        keyword = 'iphone X'
        max_page = 1
        url = 'https://search.jd.com/Search?'
        for page in range(1, max_page+1):
            url += urlencode({'keyword':keyword, 'enc': 'utf-8', 'page': page})
            yield scrapy.Request(url)

    def parse(self, response):
        node_list = response.xpath('//div[@id="J_goodsList"]//div[@class="p-name p-name-type-2"]')
        # print('***'*20)
        # print(len(node_list))
        # print('***' * 20)
        for index, node in enumerate(node_list):
            # 产品详情页面
            goods_url = 'https:' + node.xpath('./a/@href').extract_first()
            goods_url = response.urljoin(goods_url)
            yield scrapy.Request(url=goods_url,callback=self.parse_goods_page)
    #
    def parse_goods_page(self, response):
        '''
        解析产品详情页面,解析颜色，获取当前一个颜色的所有机型的页面
        :param response:
        :return:
        '''
        item = JdGoodsItem()
        describition = response.xpath(
            '//div[@class="sku-name"]/text()').extract()
        describition = ''.join(describition)
        item['describition'] = describition.strip()
        item = JdGoodsItem()
        describition = response.xpath(
            '//div[@class="sku-name"]/text()').extract()
        describition = ''.join(describition)
        item['describition'] = describition.strip()
        node_list = response.xpath('//div[@id="choose-attr-1"]/div/div')
        for node in node_list:
            item['color'] = node.xpath('./a/i/text()').extract_first().strip()
            # 颜色对应的页面链接
            data_sku = node.xpath('./@data-sku').extract_first()
            next_url = 'https://item.jd.com/{data_sku}.html'.format(data_sku=data_sku)
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url,
                                 meta={'item': item},
                                 callback=self.parse_goods_page_1)

    def parse_goods_page_1(self, response):
        '''
        当前颜色对应的内存+rom版本对应机型页面
        :param response:
        :return:
        '''
        item = response.meta['item']
        node_list = response.xpath('//div[@id="choose-attr-2"]/div/div')
        for node in node_list:
            item['memories'] = node.xpath('./a/text()').extract_first().strip()
            # 内存+ROM对应的页面链接
            data_sku = node.xpath('./@data-sku').extract_first()
            next_url = 'https://item.jd.com/{data_sku}.html'.format(
                data_sku=data_sku)
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url,
                                 meta={'item': item},
                                 callback=self.parse_goods_page_2)

    def parse_goods_page_2(self, response):
        '''
        机型颜色，内存，ROM固定，获取套餐版本页面链接
        :param response:
        :return:
        '''
        item = response.meta['item']
        node_list = response.xpath('//div[@id="choose-attr-3"]/div/div')
        for node in node_list:
            item['version'] = node.xpath('./a/text()').extract_first().strip()
            # 套餐版本对应的页面链接
            data_sku = node.xpath('./@data-sku').extract_first()
            item['id'] = data_sku
            next_url = 'https://item.jd.com/{data_sku}.html'.format(
                data_sku=data_sku)
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url,
                                 meta={'item': item},
                                 callback=self.parse_goods_page_3)

    def parse_goods_page_3(self, response):
        '''
        颜色，内存+ROM，套餐版本都以确定，获取产品图片链接
        :param response:
        :return:
        '''
        item = response.meta['item']
        # 产品价格
        price= response.xpath('//span[@class="p-price"]/span/text()').extract()
        # 包含所有当前颜色对应的产品图片
        img_node_list = response.xpath('//ul[@class="lh"]/li')
        img_list = []
        for node in img_node_list:
            img_source = node.xpath('./img/@src').extract_first()
            img_url = re.sub('\d{1}\/\w{1}\d{2,3}\w{1}\d{2,3}\w{1}', '0/', img_source)
            img_url = 'http:' + img_url
            img_list.append(img_url)
        item['img_url'] = img_list
        url = "https://p.3.cn/prices/mgets?callback=&skuIds=J_" + item['id']
        url = response.urljoin(url)
        yield scrapy.Request(url, meta={'item': item}, callback=self.parse_price)

    def parse_price(self, response):
        '''
        获取价格
        :param response:
        :return:
        '''
        item = response.meta['item']
        price_str = response.body
        price_str = price_str.decode('utf-8')
        pattern = re.compile('"p":"(.*)"}')
        result = re.findall(pattern, price_str)
        print('价格是：', result[0])
        item['price'] = '￥' + result[0]
        yield item
