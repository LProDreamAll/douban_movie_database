# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
from crawler.pipelines.base import BasePipeline


class NeteasePipeline(BasePipeline):
    """
    网易云音乐相关

    """

    def __init__(self):
        super().__init__()
        # 待处理数据列表
        self.item_dict = {
            'MovieNetease': {
                'sql': 'insert ignore into movie_netease values (%s,%s,%s,%s)'
            },
            'SongNetease': {
                'sql': 'insert ignore into song_netease values (%s,%s)'
            },
            'PlaylistNetease': {
                'sql': 'insert ignore into playlist_netease values (%s,%s,%s,%s,%s,%s)'
            },
            'AlbumNetease': {
                'sql': 'insert ignore into album_netease values (%s,%s,%s,%s)'
            },
            'ArtistNetease': {
                'sql': 'insert ignore into artist_netease values (%s,%s,%s) '
                       'on duplicate key update '
                       'url_portrait=if(url_portrait="",values(url_portrait),url_portrait) '
            },
            'ArtistNeteaseToSongNetease': {
                'sql': 'insert ignore into artist_netease_to_song_netease values (%s,%s)'
            },
            'ArtistNeteaseToAlbumNetease': {
                'sql': 'insert ignore into artist_netease_to_album_netease values (%s,%s)'
            },
            'SongNeteaseToPlaylistNetease': {
                'sql': 'insert ignore into song_netease_to_playlist_netease values (%s,%s,%s)'
            },
            'SongNeteaseToAlbumNetease': {
                'sql': 'insert ignore into song_netease_to_album_netease values (%s,%s)'
            },
            'CommentNetease': {
                'sql': 'insert ignore into comment_netease values (%s,%s,%s,%s,%s,%s)'
            },
            'UserNetease': {
                'sql': 'insert ignore into user_netease values (%s,%s)'
            }
        }
        # 每个表添加data列表
        for table in self.item_dict.keys():
            self.item_dict[table]['data'] = []
