# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.pipelines.base import BasePipeline


class SearchNeteasePipeline(BasePipeline):
    """
    网易云音乐搜索相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'SongNetease': {
                'sql': 'insert ignore into song_netease values (%s,%s,%s)'
            },
            'PlaylistNetease': {
                'sql': 'insert ignore into playlist_netease values (%s,%s,%s,%s,%s,%s,%s)'
            },
            'AlbumNetease': {
                'sql': 'insert ignore into album_netease values (%s,%s,%s,%s)'
            },
            'MovieDoubanToNetease': {
                'sql': 'insert ignore into movie_douban_to_netease values (%s,%s,%s)'
            }
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
