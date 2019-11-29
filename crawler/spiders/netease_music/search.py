# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import scrapy
from crawler.tools.netease_encrypt import form_data
from crawler.configs import default
from crawler.configs import netease as config
from crawler.spiders.base import BaseSpider

from crawler.items.netease import SongNetease
from crawler.items.netease import PlaylistNetease
from crawler.items.netease import AlbumNetease
from crawler.items.netease import ArtistNetease
from crawler.items.netease import ArtistNeteaseToSongNetease
from crawler.items.netease import ArtistNeteaseToAlbumNetease


class SearchNeteaseSpider(BaseSpider):
    """
    网易云音乐搜索相关

    """
    name = 'search_netease'
    # start_url存放容器改为redis list
    redis_key = 'search_netease:start_urls'
    allowed_domains = ['music.163.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.netease.NeteasePipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.form_data = form_data()

    def start_requests(self):
        self.cursor.execute("select movie_douban.id,movie_douban.name_zh from movie_douban "
                            "left join song_netease "
                            "on movie_douban.id=song_netease.id_movie_douban "
                            "left join playlist_netease "
                            "on movie_douban.id=playlist_netease.id_movie_douban "
                            "left join album_netease "
                            "on movie_douban.id=album_netease.id_movie_douban "
                            "where song_netease.id_movie_douban is null "
                            "and playlist_netease.id_movie_douban is null "
                            "and album_netease.id_movie_douban is null "
                            'limit {}'.format(default.SELECT_LIMIT))
        for id, keyword in self.cursor.fetchall():
            first_param = """{{s:"{}",type:"web"}}""".format(keyword)
            # 安卓API type=1:歌曲 10:专辑 1000:歌单
            # first_param_dict = config.EAPI_PARAMS
            # first_param_dict['s'] = keyword
            # first_param_dict['type'] = 1000
            # first_param = json.dumps(first_param_dict, separators=(',', ':'))
            fd = self.form_data.get_form_data(first_param=first_param, api_type=config.TYPE_WEAPI, eapi_url=None)
            yield scrapy.FormRequest(url=config.URL_SEARCH_TIPS, formdata=fd,
                                     meta={'id': id, 'keyword': keyword}, callback=self.parse)

    def parse(self, response):
        movie_id = response.meta['id']
        keyword = response.meta['keyword']
        content = json.loads(response.text)
        if 'result' in content and (
                'songs' in content['result'] or 'playlists' in content['result'] or 'albums' in content['result']):
            result = content['result']
            # 歌曲
            if 'songs' in result:
                for song in result['songs']:
                    item_song = SongNetease()
                    item_song['id'] = song['id']
                    item_song['id_movie_douban'] = movie_id
                    item_song['name_zh'] = song['name']
                    yield item_song
                    print('song ---------------')
                    print(item_song)
                    for artist in song['artists']:
                        item_artist = ArtistNetease()
                        item_artist['id'] = artist['id']
                        item_artist['name_zh'] = artist['name']
                        yield item_artist
                        item_artist_to_song = ArtistNeteaseToSongNetease()
                        item_artist_to_song['id_artist_netease'] = artist['id']
                        item_artist_to_song['id_song_netease'] = song['id']
                        yield item_artist_to_song
            # 歌单
            if 'playlists' in result:
                for playlist in result['playlists']:
                    item_playlist = PlaylistNetease()
                    item_playlist['id'] = playlist['id']
                    item_playlist['id_movie_douban'] = movie_id
                    item_playlist['name_zh'] = playlist['name']
                    item_playlist['total'] = playlist['trackCount']
                    item_playlist['play_count'] = playlist['playCount']
                    item_playlist['url_cover'] = playlist['coverImgUrl']
                    item_playlist['description'] = playlist['description']
                    yield item_playlist
                    print('playlist ---------------')
                    print(item_playlist)
            # 专辑
            if 'albums' in result:
                for album in result['albums']:
                    item_album = AlbumNetease()
                    item_album['id'] = album['id']
                    item_album['id_movie_douban'] = movie_id
                    item_album['name_zh'] = album['name']
                    item_album['total'] = album['size']
                    yield item_album
                    print('album ----------------')
                    print(item_album)
                    item_artist = ArtistNetease()
                    item_artist['id'] = album['artist']['id']
                    item_artist['name_zh'] = album['artist']['name']
                    yield item_artist
                    item_artist_to_album = ArtistNeteaseToAlbumNetease()
                    item_artist_to_album['id_artist_netease'] = album['artist']['id']
                    item_artist_to_album['id_album_netease'] = album['id']
                    yield item_artist_to_album
            self.logger.info('get netease search success,movie_id:{},keyword:{}'.format(movie_id, keyword))
        else:
            self.logger.warning('get netease search failed,movie_id:{},keyword:{}'.format(movie_id, keyword))

