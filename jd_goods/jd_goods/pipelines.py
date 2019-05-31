# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import json
import os
import codecs
import scrapy
import pymongo
from jd_goods.settings import MONGO_DB, MONGO_PORT, MONGO_SHEETNAME, MONGO_URI


class JdGoodsPipeline(object):
    '''
    数据储存本地json文档
    '''
    def __init__(self):
        self.file = codecs.open('results.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + '\r\n'
        self.file.write(line)
        return item
    def spider_closed(self, spider):
        self.file.close()


class ImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        urls = item['img_url']
        for url in urls:
            file_name = url.split('/')[-1]
            path = '%s/%s/%s' % (item['describition'][0:20], item['color'], file_name)
            return path

    def get_media_requests(self, item, info):
        urls = item.get('img_url')
        for url in urls:
            yield scrapy.Request(url, meta={'item': item})


class MongoPipeline(object):

    def __init__(self):
        host = MONGO_URI
        port = MONGO_PORT
        dbname = MONGO_DB
        cname = MONGO_SHEETNAME
        client = pymongo.MongoClient(host=host, port=port)
        mydb = client[dbname]
        self.post = mydb[cname]

    def process_item(self, item, spider):
        data = dict(item)
        self.post.insert(data)
        return item