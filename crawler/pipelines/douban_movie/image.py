# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

from crawler.pipelines.base import BasePipeline


class ImageDoubanPipeline(BasePipeline):
    """
    图片相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'ImageMovieDouban': {
                'sql': 'insert ignore into image_movie_douban values (%s,%s,%s,%s,%s)'
            },
            'ImageCelebrityDouban': {
                'sql': 'insert ignore into image_celebrity_douban values (%s,%s,%s,%s,%s)'
            }
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
