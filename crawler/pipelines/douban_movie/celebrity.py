# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.pipelines.base import BasePipeline


class CelebrityDoubanPipeline(BasePipeline):
    """
    豆瓣影人相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'CelebrityDouban': {
                'sql': 'replace into celebrity_douban values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            },
            'AliasCelebrityDouban': {
                'sql': 'insert ignore into alias_celebrity_douban values (%s,%s,%s)'
            },
            'AwardMovie': {
                'sql': 'insert ignore into award_movie values (%s,%s)'
            },
            'MovieDoubanToAwardMovie': {
                'sql': 'insert ignore into movie_douban_to_award_movie values (%s,%s,%s,%s,%s,%s)'
            }
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
