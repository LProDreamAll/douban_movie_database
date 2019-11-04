# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SceneItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class MovieSceneItem(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
    cover_src = scrapy.Field()
    static_map_src = scrapy.Field()
    start_year = scrapy.Field()
