# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.tools.database_pool import database_pool
from crawler.configs import default
from scrapy_redis.spiders import RedisSpider


class BaseSpider(RedisSpider):
    """
    xxxSpider类的公共父类

    需要重写 prepare 和 parse 两个方法

    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()
        # 计数器
        self.count = 0
        # 当前请求列表数量限制
        self.limit = default.REQUEST_NOW

    def start_requests(self):
        return self.prepare(self.count, self.limit)

    def prepare(self, offset, limit):
        """
        获取请求列表

        :param offset:
        :param limit:
        :return:
        """
        pass

    def parse(self, response):
        pass
