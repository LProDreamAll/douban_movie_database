# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy

"""
场景相关

"""

class Scene(scrapy.Item):
    """
    场景

    """
    id = scrapy.Field()
    id_movie_scene = scrapy.Field()
    id_place = scrapy.Field()
    name_zh = scrapy.Field()
    happen_time = scrapy.Field()


class SceneDetail(scrapy.Item):
    """
    场景详情

    """
    id = scrapy.Field()
    id_scene = scrapy.Field()
    id_movie_scene = scrapy.Field()
    id_place = scrapy.Field()
    happen_time = scrapy.Field()
    description = scrapy.Field()


class Place(scrapy.Item):
    """
    地点

    """
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
    description = scrapy.Field()


class Movie(scrapy.Item):
    """
    电影

    """
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
    start_year = scrapy.Field()
    description = scrapy.Field()


class Celebrity(scrapy.Item):
    """
    影人

    """
    id = scrapy.Field()
    id_scene = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
