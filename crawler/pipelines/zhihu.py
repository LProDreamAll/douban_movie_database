# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.pipelines.base import BasePipeline


class ZhihuPipeline(BasePipeline):
    """
    知乎相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'MovieZhihu': {
                'sql': 'insert ignore into movie_zhihu values (%s,%s,%s,%s,%s,%s) '
            },
            'QuestionZhihu': {
                'sql': 'insert ignore into question_zhihu values (%s,%s,%s,%s) '
            },
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
