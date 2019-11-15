# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy


class MovieDouban(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()


class CelebrityDouban(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()


class MovieScene(scrapy.Item):
    id = scrapy.Field()
    id_movie_douban = scrapy.Field()


class CelebrityScene(scrapy.Item):
    id = scrapy.Field()
    id_celebrity_douban = scrapy.Field()
