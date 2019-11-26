# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.pipelines.base import BasePipeline


class ResourcePipeline(BasePipeline):
    """
    电影资源相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'ResourceMovie': {
                'sql': 'insert ignore into resource_movie(id_movie_douban,id_movie_imdb ,id_website_resource, id_type_resource, name_zh,create_year,name_origin,url_resource) '
                       ' values (%s,%s,%s,%s,%s,%s,%s,%s)'
            },
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
