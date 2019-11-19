# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

"""
豆瓣影人相关

"""
import scrapy


class CelebrityDouban(scrapy.Item):
    id = scrapy.Field()
    id_celebrity_imdb = scrapy.Field()
    name_zh = scrapy.Field()
    name_origin = scrapy.Field()
    sex = scrapy.Field()
    birth_date = scrapy.Field()
    url_portrait = scrapy.Field()
    summary = scrapy.Field()
    is_updated = scrapy.Field()


class AliasCelebrityDouban(scrapy.Item):
    id_celebrity_douban = scrapy.Field()
    name_alias = scrapy.Field()
    is_nikename = scrapy.Field()


class ImageCelebrityDouban(scrapy.Item):
    id = scrapy.Field()
    id_celebrity_douban = scrapy.Field()
    sort = scrapy.Field()
    length = scrapy.Field()
    width = scrapy.Field()
