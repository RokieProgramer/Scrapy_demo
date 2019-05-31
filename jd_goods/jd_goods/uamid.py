#!/usr/bin/env python 
# -*- coding: utf-8 -*-
"""
@project = jd_goods
@file = 
@author = Administrator
@create_time = 2019/6/1 0001 3:28
"""

import random
from .settings import UAPOOL
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware


class Uamid(UserAgentMiddleware):

    def __init__(self, usragent=''):
        self.user_agent = usragent

    def process_request(self, request, spider):
        thisua = random.choice(UAPOOL)
        print('当前UA,\n{}'.format(thisua))
        print('+++'*20)
        # request.headers.setdefalut('User-Agent', thisua)
        request.meta['User-Agent'] = thisua




