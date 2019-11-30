# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

from crawler.pipelines.base import BasePipeline


class SearchDoubanPipeline(BasePipeline):
    """
    豆瓣电影搜索相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'MovieDouban': {
                'sql': 'insert ignore into movie_douban(id,id_movie_imdb,name_zh,start_year) values (%s,%s,%s,%s)'
            },
            'CelebrityDouban': {
                'sql': 'insert ignore into celebrity_douban(id,id_celebrity_imdb,name_origin) values (%s,%s,%s)'
            },
            'ResourceMovie': {
                'sql': 'insert into resource_movie(id,id_movie_douban) '
                       'values (%s,%s) '
                       'on duplicate key update '
                       'id_movie_douban=values(id_movie_douban) '
            },
            'MovieScene': {
                'sql': 'insert into movie_scene(id,id_movie_douban) values(%s,%s) '
                       'on duplicate key update '
                       'id_movie_douban=values(id_movie_douban) '
            },
            'CelebrityScene': {
                'sql': 'insert into celebrity_scene(id,id_celebrity_douban) values (%s,%s) '
                       'on duplicate key update '
                       'id_celebrity_douban=values(id_celebrity_douban) '
            },
            'MovieImdb': {
                'sql': 'insert into movie_imdb(id,is_douban_updated) values (%s,%s) '
                       'on duplicate key update '
                       'is_douban_updated=values(is_douban_updated) '
            },
            'CelebrityImdb': {
                'sql': 'insert into celebrity_imdb(id,is_douban_updated) values (%s,%s) '
                       'on duplicate key update '
                       'is_douban_updated=values(is_douban_updated) '
            },
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
