# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

"""
公共电影相关

"""
import scrapy


class TypeVideo(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()


class AwardMovie(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()


class TypeAward(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()


class TypeMovie(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()


class TagMovie(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()

class Profession(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()