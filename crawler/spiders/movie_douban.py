# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy
from crawler.tools.database_pool import database_pool



class MovieDoubanSpider(scrapy.Spider):
    """
    豆瓣电影相关

    """
    name = 'movie_douban'
    allowed_domains = ['movie.douban.com']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()



    def start_requests(self):
        self.cursor.execute('select id from movie_douban')

    def parse(self, response):
        pass
