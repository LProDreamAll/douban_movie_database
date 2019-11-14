# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy


class MovieDoubanSpider(scrapy.Spider):
    """
    豆瓣电影相关

    """
    name = 'movie_douban'
    allowed_domains = ['movie.douban.com']

    def start_requests(self):
        pass

    def parse(self, response):
        pass
