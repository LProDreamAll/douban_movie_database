# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# 场景相关 start ------------------------------------------------------------------

class SceneItem(scrapy.Item):
    """
    场景

    """
    id = scrapy.Field()
    id_movie_scene = scrapy.Field()
    id_place = scrapy.Field()
    name_zh = scrapy.Field()
    happen_time = scrapy.Field()


class SceneDetailItem(scrapy.Item):
    """
    场景详情

    """
    id = scrapy.Field()
    id_scene = scrapy.Field()
    id_movie_scene = scrapy.Field()
    id_place = scrapy.Field()
    happen_time = scrapy.Field()
    description = scrapy.Field()


class PlaceItem(scrapy.Item):
    """
    地点

    """
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
    description = scrapy.Field()


class MovieItem(scrapy.Item):
    """
    电影

    """
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
    start_year = scrapy.Field()
    description = scrapy.Field()


class CelebrityItem(scrapy.Item):
    """
    影人

    """
    id = scrapy.Field()
    id_scene = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()


# 场景相关 end ------------------------------------------------------------------
