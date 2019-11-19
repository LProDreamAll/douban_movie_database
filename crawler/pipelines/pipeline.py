# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

from crawler.configs import default as config
from crawler.tools.database_pool import database_pool
import warnings


class Pipeline(object):
    """
    pipeline类的公共父类，用于批量处理不同表的sql语句

    PS: 每一个子类需要初始化init方法中的item_dict中不同表对应的sql语句及其data列表

    """

    def __init__(self):
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()
        # 待处理数据列表
        self.item_dict = {
        }

    def process_item(self, item, spider):
        table = item.__class__.__name__
        self.item_dict[table]['data'].append(list(item.values()))
        # 批量处理待处理数据列表
        if len(self.item_dict[table]['data']) > config.BATCH_NUM:
            self.execute(table)

    def close_spider(self, spider):
        # 批量处理待处理数据列表的剩余部分
        for table in self.item_dict:
            if self.item_dict[table]['data']:
                self.execute(table)
        self.conn.close()

    def execute(self, table):
        """
        批量执行sql语句

        :param table: item_dict中的表名
        :return:
        """
        warnings.filterwarnings("ignore")
        self.cursor.executemany(self.item_dict[table]['sql'], self.item_dict[table]['data'])
        self.conn.commit()
        self.item_dict[table]['data'].clear()
