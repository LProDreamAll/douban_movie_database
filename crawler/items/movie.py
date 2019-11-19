# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

"""
公共电影相关

"""
import scrapy


class TagMovie(scrapy.Item):
    id_movie_douban = scrapy.Field()
    name_zh = scrapy.Field()


class AwardMovie(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()