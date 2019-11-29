# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy

"""
search
均用于更新,或添加ID

"""


class ResourceMovie(scrapy.Item):
    id = scrapy.Field()
    id_movie_douban = scrapy.Field()


class MovieDouban(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()
    start_year = scrapy.Field()


class CelebrityDouban(scrapy.Item):
    id = scrapy.Field()
    name_en = scrapy.Field()


class MovieScene(scrapy.Item):
    id = scrapy.Field()
    id_movie_douban = scrapy.Field()


class CelebrityScene(scrapy.Item):
    id = scrapy.Field()
    id_celebrity_douban = scrapy.Field()


class MovieImdb(scrapy.Item):
    id = scrapy.Field()
    is_douban_updated = scrapy.Field()


class CelebrityImdb(scrapy.Item):
    id = scrapy.Field()
    is_douban_updated = scrapy.Field()
