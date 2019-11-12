# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

from crawler.configs import default as config
from crawler.tools.database_pool import database_pool


class ScenePipeline(object):
    """
    场景相关

    """

    def __init__(self):
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()
        self.spider_name = 'scene'
        # 待处理数据列表
        self.item_list = {
            'Movie': [],
            'Celebrity': [],
            'Place': [],
            'Scene': [],
            'SceneDetail': []
        }

    def process_item(self, item, spider):
        if spider.name == self.spider_name:
            table = item.__class__.__name__
            self.item_list[table].append(list(item.values()))
            # 批量处理待处理数据列表
            if len(self.item_list[table]) > config.BATCH_NUM:
                self.dispose(table)

    def close_spider(self, spider):
        if spider.name == self.spider_name:
            # 批量处理待处理数据列表的剩余部分
            for table in self.item_list:
                self.dispose(table)
            self.conn.close()

    def dispose(self, table):
        """
        数据表分类,数据库sql语句

        :param table: item_list中的表名
        :return:
        """
        # 电影
        if table == 'Movie':
            self.execute(table=table,
                         sql='insert into movie_scene(id,name_zh,name_en,start_year,description) values (%s,%s,%s,%s,%s)')
        elif table == 'Celebrity':
            pass
        elif table == 'Place':
            pass
        elif table == 'Scene':
            pass
        elif table == 'SceneDetail':
            pass

    def execute(self, table, sql):
        """
        数据库sql执行

        :param table: item_list中的表名
        :param sql
        :return:
        """
        self.cursor.executemany(sql, self.item_list[table])
        self.item_list[table].clear()
        self.conn.commit()
