# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.tools.database_pool import database_pool
from crawler.configs import default as config


class MovieDoubanPipeline(object):
    """
    豆瓣电影相关

    """

    def __init__(self):
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()
        self.spider_name = 'movie_douban'

    def process_item(self, item, spider):
        if spider.name == self.spider_name:
            pass

    def close_spider(self, spider):
        if spider.name == self.spider_name:
            pass
