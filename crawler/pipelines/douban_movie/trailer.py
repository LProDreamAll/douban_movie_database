# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.pipelines.base import BasePipeline


class TrailerDoubanPipeline(BasePipeline):
    """
    豆瓣电影预告片相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'TrailerMovieDouban': {
                'sql': 'replace into trailer_movie_douban values (%s,%s,%s)'
            }
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
