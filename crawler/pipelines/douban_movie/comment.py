# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.pipelines.base import BasePipeline


class CommentDoubanPipeline(BasePipeline):
    """
    豆瓣电影短评相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'CommentMovieDouban': {
                'sql': 'insert ignore into comment_movie_douban values (%s,%s,%s,%s,%s)'
            },
            'UserDouban': {
                'sql': 'insert ignore into user_douban values (%s,%s)'
            }
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
