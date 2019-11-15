# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

from crawler.pipelines.pipeline import Pipeline


class SearchPipeline(Pipeline):
    """
    电影搜索相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'MovieDouban': {
                'sql': 'insert ignore into movie_douban(id,name_zh) values (%s,%s)'
            },
            'CelebrityDouban': {
                'sql': 'insert ignore into celebrity_douban(id,name_zh) values (%s,%s)'
            },
            'MovieScene': {
                'sql': 'update movie_scene set id_movie_douban=%s where id=%s'
            },
            'CelebrityScene': {
                'sql': 'update celebrity_scene set id_celebrity_douban=%s where id=%s'
            },
            'MovieResource': {
                'sql': ''
            }
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
