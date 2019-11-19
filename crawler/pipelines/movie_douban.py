# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.pipelines.pipeline import Pipeline


class MovieDoubanPipeline(Pipeline):
    """
    豆瓣电影相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'MovieDouban': {
                'sql': 'replace into movie_douban values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            },
            'AliasMovieDouban': {
                'sql': 'insert ignore into alias_movie_douban values (%s,%s)'
            },
            'MovieDoubanToCelebrityDouban': {
                'sql': 'insert ignore into movie_douban_to_celebrity_douban values (%s,%s,%s,%s)'
            },
            'MovieDoubanToTypeMovie': {
                'sql': 'insert ignore into movie_douban_to_type_movie values (%s,%s)'
            },
            'RateMovieDouban': {
                'sql': 'insert ignore into rate_movie_douban values (%s,%s,%s,%s,%s,%s,%s,%s)'
            },
            'TagMovie': {
                'sql': 'insert ignore into tag_movie values (%s,%s)'
            },
            'AwardMovie': {
                'sql': 'insert ignore into award_movie values (%s,%s)'
            },
            'MovieDoubanToAwardMovie': {
                'sql': 'insert ignore into movie_douban_to_award_movie values (%s,%s,%s,%s,%s,%s)'
            },
            'ImageMovieDouban': {
                'sql': 'insert ignore into image_movie_douban values (%s,%s,%s,%s,%s)'
            },
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
