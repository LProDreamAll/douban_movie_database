# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy


# 用于更新resource
class ResourceMovie(scrapy.Item):
    id = scrapy.Field()
    id_movie_douban = scrapy.Field()
    id_movie_imdb = scrapy.Field()


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
