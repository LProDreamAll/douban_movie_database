# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.pipelines.base import BasePipeline


class DoubanPipeline(BasePipeline):
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
            'TrailerMovieDouban': {
                'sql': 'insert ignore into trailer_movie_douban values (%s,%s,%s)'
            },
            'ResourceMovie': {
                'sql': 'insert into resource_movie(id_movie_douban,id_movie_imdb ,id_website_resource, id_type_resource, name_zh,create_year,name_origin,url_resource) '
                       ' values (%s,%s,%s,%s,%s,%s,%s,%s)'
            },
            'ImageCelebrityDouban': {
                'sql': 'insert ignore into image_celebrity_douban values (%s,%s,%s,%s,%s)'
            },
            'CommentMovieDouban': {
                'sql': 'insert ignore into comment_movie_douban values (%s,%s,%s,%s,%s)'
            },
            'UserDouban': {
                'sql': 'insert ignore into user_douban values (%s,%s)'
            },
            'CelebrityDouban': {
                'sql': 'replace into celebrity_douban values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            },
            'AliasCelebrityDouban': {
                'sql': 'insert ignore into alias_celebrity_douban values (%s,%s,%s)'
            }
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
