# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

from crawler.pipelines.pipeline import Pipeline


class ScenePipeline(Pipeline):
    """
    场景相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'Scene': {
                'sql': 'insert ignore into scene values (%s,%s,%s,%s,%s)'
            },
            'SceneDetail': {
                'sql': 'insert ignore into scene_detail values (%s,%s,%s,%s,%s)'
            },
            'PlaceScene': {
                'sql': 'insert ignore into place_scene values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            },
            'MovieScene': {
                'sql': 'insert ignore into movie_scene(id,name_zh,name_en,start_year,description,url_map) values (%s,%s,%s,%s,%s,%s)'
            },
            'CelebrityScene': {
                'sql': 'insert ignore into celebrity_scene(id, name_zh, name_en) values (%s,%s,%s)'
            },
            'SceneDetailToCelebrityScene': {
                'sql': 'insert ignore into scene_detail_to_celebrity_scene values (%s,%s)'
            },
            'ImagePlaceScene': {
                'sql': 'insert ignore into image_place_scene(id_place_scene, url_image, description) values (%s,%s,%s)'
            },
            'ImageSceneDetail': {
                'sql': 'insert ignore into image_scene_detail(id_scene_detail, url_image) values (%s,%s)'
            },
            'ContinentScene': {
                'sql': 'insert ignore into continent_scene values (%s,%s,%s)'
            },
            'CountryScene': {
                'sql': 'insert ignore into country_scene values (%s,%s,%s)'
            },
            'StateScene': {
                'sql': 'insert ignore into  state_scene values (%s,%s,%s)'
            },
            'CityScene': {
                'sql': 'insert ignore into city_scene values (%s,%s,%s)'
            },
            'PlaceSceneToTypePlaceScene': {
                'sql': 'insert ignore into place_scene_to_type_place_scene values (%s,%s)'
            }
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
