# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

import scrapy

"""
IMDB相关

"""


class MovieImdb(scrapy.Item):
    id = scrapy.Field()
    url_poster = scrapy.Field()
    summary = scrapy.Field()


class RateImdb(scrapy.Item):
    id = scrapy.Field()
    imdb_score = scrapy.Field()
    imdb_vote = scrapy.Field()
    tomato_score = scrapy.Field()
    mtc_score = scrapy.Field()
