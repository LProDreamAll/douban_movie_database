# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import re
import scrapy
from crawler.tools.netease_encrypt import form_data
from crawler.configs import default
from crawler.configs import netease as config
from crawler.spiders.base import BaseSpider

from crawler.items.netease import MovieNetease
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
                            "left join movie_netease "
                            "on movie_douban.id=movie_netease.id_movie_douban "
                            "where movie_netease.id_movie_douban is null "
                            'limit {}'.format(default.SELECT_LIMIT))
        for id, keyword in self.cursor.fetchall():
            # webAPI 混合歌曲,专辑,歌单
            # first_param = """{{s:"{}",type:"web"}}""".format(keyword)
            for netease_type in [1, 10, 1000]:
                # 安卓API type=1:歌曲 10:专辑 1000:歌单
                first_param_dict = config.EAPI_PARAMS
                first_param_dict['s'] = keyword
                first_param_dict['type'] = netease_type
                first_param = json.dumps(first_param_dict, separators=(',', ':'))
                fd = self.form_data.get_form_data(first_param=first_param, api_type=config.TYPE_EAPI,
                                                  eapi_url=config.URL_SEARCH_TIPS_EAPI_NEED)
                yield scrapy.FormRequest(url=config.URL_EAPI_SEARCH_TIPS, formdata=fd,
                                         meta={'id': id, 'netease_type': netease_type, 'keyword': keyword},
                                         callback=self.parse)

    def parse(self, response):
        movie_id = response.meta['id']
        keyword = response.meta['keyword']
        netease_type = response.meta['netease_type']
        content = json.loads(response.text)
        # 获取结果正常
        if 'result' in content:
            # 获取到内容且不为空
            if content['result']:
                result = content['result']
                # 歌曲
                if netease_type == 1 and 'songs' in result:
                    for index, song in enumerate(result['songs']):
                        item_song = SongNetease()
                        item_song['id'] = song['id']
                        item_song['name_zh'] = song['name']
                        yield item_song
                        print('song ---------------')
                        print(item_song)
                        for artist in song['artists']:
                            item_artist = ArtistNetease()
                            item_artist['id'] = artist['id']
                            item_artist['name_zh'] = artist['name']
                            url_cover = re.search('net/(.*)', artist['picUrl']) if artist['picUrl'] is not None else ''
                            item_artist['url_portrait'] = url_cover.group(1) if url_cover != '' else ''
                            yield item_artist
                            item_artist_to_song = ArtistNeteaseToSongNetease()
                            item_artist_to_song['id_artist_netease'] = artist['id']
                            item_artist_to_song['id_song_netease'] = song['id']
                            yield item_artist_to_song
                        item_movie = MovieNetease()
                        item_movie['id_movie_douban'] = movie_id
                        item_movie['id_netease'] = song['id']
                        item_movie['netease_type'] = 1
                        item_movie['sort'] = index + 1
                        yield item_movie
                # 歌单
                elif netease_type == 1000 and 'playlists' in result:
                    for index, playlist in enumerate(result['playlists']):
                        item_playlist = PlaylistNetease()
                        item_playlist['id'] = playlist['id']
                        item_playlist['name_zh'] = playlist['name']
                        item_playlist['total'] = playlist['trackCount']
                        item_playlist['play_count'] = playlist['playCount']
                        item_playlist['url_cover'] = playlist['coverImgUrl']
                        item_playlist['description'] = playlist['description']
                        yield item_playlist
                        print('playlist ---------------')
                        print(item_playlist)
                        item_movie = MovieNetease()
                        item_movie['id_movie_douban'] = movie_id
                        item_movie['id_netease'] = playlist['id']
                        item_movie['netease_type'] = 2
                        item_movie['sort'] = index + 1
                        yield item_movie
                # 专辑
                elif netease_type == 10 and 'albums' in result:
                    for index, album in enumerate(result['albums']):
                        item_album = AlbumNetease()
                        item_album['id'] = album['id']
                        item_album['name_zh'] = album['name']
                        item_album['total'] = album['size']
                        url_cover = re.search('net/(.*)', album['picUrl']) if album['picUrl'] is not None else ''
                        item_album['url_cover'] = url_cover.group(1) if url_cover != '' else ''
                        yield item_album
                        print('album ----------------')
                        print(item_album)
                        item_artist = ArtistNetease()
                        item_artist['id'] = album['artist']['id']
                        item_artist['name_zh'] = album['artist']['name']
                        url_portrait = re.search(
                            'net/(.*)', album['artist']['picUrl']) if album['artist']['picUrl'] is not None else ''
                        item_artist['url_portrait'] = url_portrait.group(1) if url_portrait != '' else ''
                        yield item_artist
                        item_artist_to_album = ArtistNeteaseToAlbumNetease()
                        item_artist_to_album['id_artist_netease'] = album['artist']['id']
                        item_artist_to_album['id_album_netease'] = album['id']
                        yield item_artist_to_album
                        item_movie = MovieNetease()
                        item_movie['id_movie_douban'] = movie_id
                        item_movie['id_netease'] = album['id']
                        item_movie['netease_type'] = 3
                        item_movie['sort'] = index + 1
                        yield item_movie
                self.logger.info('get netease search success,movie_id:{},keyword:{},netease_type:{}'
                                 .format(movie_id, keyword, netease_type))
            # 获取到结果但为空,标记为已搜索
            else:
                item_movie = MovieNetease()
                item_movie['id_movie_douban'] = movie_id
                item_movie['id_netease'] = 0
                item_movie['netease_type'] = 0
                item_movie['sort'] = 0
                yield item_movie
                self.logger.info('get netease search None,movie_id:{},keyword:{},netease_type:{}'
                                 .format(movie_id, keyword, netease_type))
        # 获取结果失败
        else:
            self.logger.warning('get netease search failed,movie_id:{},keyword:{},netease_type:{}'
                                .format(movie_id, keyword, netease_type))
