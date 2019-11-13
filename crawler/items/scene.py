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
    id_place_scene = scrapy.Field()
    name_zh = scrapy.Field()
    happen_time = scrapy.Field()


class SceneDetail(scrapy.Item):
    """
    场景详情

    """
    id = scrapy.Field()
    id_scene = scrapy.Field()
    id_movie_scene = scrapy.Field()
    happen_time = scrapy.Field()
    description = scrapy.Field()


class PlaceScene(scrapy.Item):
    """
    场景地点

    """
    id = scrapy.Field()
    id_continent_scene = scrapy.Field()
    id_country_scene = scrapy.Field()
    id_state_scene = scrapy.Field()
    id_city_scene = scrapy.Field()
    longitude = scrapy.Field()
    latitude = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
    name_other = scrapy.Field()
    alias = scrapy.Field()
    address_zh = scrapy.Field()
    address_en = scrapy.Field()
    description = scrapy.Field()
    area_zh = scrapy.Field()
    area_en = scrapy.Field()
    phone = scrapy.Field()
    url_poster = scrapy.Field()
    url_earth = scrapy.Field()
    url_satellite = scrapy.Field()
    url_map = scrapy.Field()


class MovieScene(scrapy.Item):
    """
    场景电影

    """
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
    start_year = scrapy.Field()
    description = scrapy.Field()
    url_map = scrapy.Field()


class CelebrityScene(scrapy.Item):
    """
    场景影人

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


class ImagePlaceScene(scrapy.Item):
    """
    场景地点实景图

    """
    id_place_scene = scrapy.Field()
    url_image = scrapy.Field()
    description = scrapy.Field()


class ImageSceneDetail(scrapy.Item):
    """
    场景详情剧照图

    """
    id_scene_detail = scrapy.Field()
    url_image = scrapy.Field()


class ContinentScene(scrapy.Item):
    """
    洲

    """
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()


class CountryScene(scrapy.Item):
    """
    国家

    """
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()


class StateScene(scrapy.Item):
    """
    州/省

    """
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()


class CityScene(scrapy.Item):
    """
    城市

    """
    id = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()


class PlaceSceneToTypePlaceScene(scrapy.Item):
    """
    场景地点-场景地点类型

    """
    id_place_scene = scrapy.Field()
    id_type_place_scene = scrapy.Field()
