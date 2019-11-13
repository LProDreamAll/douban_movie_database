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
            'Scene': [],
            'SceneDetail': [],
            'PlaceScene': [],
            'MovieScene': [],
            'CelebrityScene': [],
            'SceneDetailToCelebrityScene': [],
            'ImagePlaceScene': [],
            'ImageSceneDetail': [],
            'ContinentScene': [],
            'CountryScene': [],
            'StateScene': [],
            'CityScene': [],
            'PlaceSceneToTypePlaceScene': []
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
        if table == 'Scene':
            self.execute(table=table, sql='insert ignore into scene values (%s,%s,%s,%s,%s)')
        elif table == 'SceneDetail':
            self.execute(table=table, sql='insert ignore into scene_detail values (%s,%s,%s,%s,%s)')
        elif table == 'PlaceScene':
            self.execute(table=table,
                         sql='insert ignore into place_scene values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)')
        elif table == 'MovieScene':
            self.execute(table=table,
                         sql='insert ignore into movie_scene(id,name_zh,name_en,start_year,description,url_map) values (%s,%s,%s,%s,%s,%s)')
        elif table == 'CelebrityScene':
            self.execute(table=table,
                         sql='insert ignore into celebrity_scene(id, name_zh, name_en) values (%s,%s,%s)')
        elif table == 'SceneDetailToCelebrityScene':
            self.execute(table=table, sql='insert ignore into scene_detail_to_celebrity_scene values (%s,%s)')
        elif table == 'ImagePlaceScene':
            self.execute(table=table,
                         sql='insert ignore into image_place_scene(id_place_scene, url_image, description) values (%s,%s,%s)')
        elif table == 'ImageSceneDetail':
            self.execute(table=table,
                         sql='insert ignore into image_scene_detail(id_scene_detail, url_image) values (%s,%s)')
        elif table == 'ContinentScene':
            self.execute(table=table, sql='insert ignore into continent_scene values (%s,%s,%s)')
        elif table == 'CountryScene':
            self.execute(table=table, sql='insert ignore into country_scene values (%s,%s,%s)')
        elif table == 'StateScene':
            self.execute(table=table, sql='insert ignore into  state_scene values (%s,%s,%s)')
        elif table == 'CityScene':
            self.execute(table=table, sql='insert ignore into city_scene values (%s,%s,%s)')
        elif table == 'PlaceSceneToTypePlaceScene':
            self.execute(table=table, sql='insert ignore into place_scene_to_type_place_scene values (%s,%s)')

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
