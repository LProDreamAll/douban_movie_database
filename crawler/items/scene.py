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
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
    name_other = scrapy.Field()
    alias = scrapy.Field()
    address_zh = scrapy.Field()
    address_en = scrapy.Field()
    description = scrapy.Field()
    phone = scrapy.Field()
    url_poster = scrapy.Field()
    url_earth = scrapy.Field()
    url_satellite = scrapy.Field()
    url_map = scrapy.Field()


class Movie(scrapy.Item):
    """
    电影

    """
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
    start_year = scrapy.Field()
    description = scrapy.Field()
    url_map = scrapy.Field()


class Celebrity(scrapy.Item):
    """
    影人

    """
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()


class SceneDetailToCelebrityScene(scrapy.Item):
    """
    影人-场景详情

    """
    id_scene_detail = scrapy.Field()
    id_celebrity_scene = scrapy.Field()


class ImagePlace(scrapy.Item):
    """
    地点实景图

    """
    id_place = scrapy.Field()
    url_image = scrapy.Field()
    description = scrapy.Field()


class ImageSceneDetail(scrapy.Item):
    """
    场景详情剧照图

    """
    id_scene_detail = scrapy.Field()
    url_image = scrapy.Field()
