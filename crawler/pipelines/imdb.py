# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.pipelines.base import BasePipeline


class ImdbPipeline(BasePipeline):
    """
    IMDB相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'MovieImdb': {
                'sql': 'insert into movie_imdb(id,url_poster,summary) values (%s,%s,%s) '
                       'on duplicate key update '
                       'url_poster=values(url_poster), '
                       'summary=values(summary)'
            },
            'RateImdb': {
                'sql': 'insert into rate_imdb values(%s,%s,%s,%s,%s) '
                       'on duplicate key update '
                       'tomato_score=values(tomato_score), '
                       'mtc_score=values(mtc_score) '
            }
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
