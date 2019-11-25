# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy


class ResourceMovie(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_movie_imdb = scrapy.Field()
    id_website_resource = scrapy.Field()
    id_type_resource = scrapy.Field()
    name_zh = scrapy.Field()
    create_year = scrapy.Field()
    name_origin = scrapy.Field()
    url_resource = scrapy.Field()
