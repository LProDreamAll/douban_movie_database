# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import time

from crawler.tools.database_pool import database_pool
from scrapy_redis.spiders import RedisSpider


class BaseSpider(RedisSpider):
    """
    xxxSpider类的公共父类


    """

    def __init__(self, type=None, **kwargs):
        super().__init__(**kwargs)
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()
        self.type = type
        # 当期日期
        self.today = int(time.time())

    def start_requests(self):
        pass

    def prepare(self, offset, limit):
        pass

    def parse(self, response):
        pass
