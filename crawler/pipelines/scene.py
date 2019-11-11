# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

from crawler.database_pool import database_pool

"""
场景相关

"""


class MoviePipeline(object):
    """
    电影

    """

    def __init__(self):
        self.conn = database_pool.connection()
        self.spider_name = 'scene'
        self.item_list = []

    def process_item(self, item, spider):
        if spider.name == self.spider_name:
            self.item_list.append(list(item.values()))
            # 每满100条数据进行批量插入
            if len(self.item_list) == 10:
                self.insert_movie(self.item_list)
                self.item_list.clear()

    def close_spider(self, spider):
        if spider.name == self.spider_name:
            # 剩下不满100条数据批量插入
            self.insert_movie(self.item_list)
            self.item_list.clear()
            self.conn.close()

    def insert_movie(self, item_list):
        """
        批量插入电影数据

        :param item_list:
        :return:
        """
        self.conn.cursor().executemany(
            'insert into movie_scene(id,name_zh,name_en,start_year,description) values (%s,%s,%s,%s,%s)', item_list)
        self.conn.commit()
        # try:
        #     self.conn.cursor().executemany(
        #         'insert into movie_scene(id,name_zh,name_en,start_year,description) values (%s,%s,%s,%s,%s)', item_list)
        #     self.conn.commit()
        # except Exception as e:
        #     pass
