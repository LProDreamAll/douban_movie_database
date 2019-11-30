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
from crawler.items.netease import SongNeteaseToAlbumNetease
from crawler.items.netease import ArtistNetease
from crawler.items.netease import ArtistNeteaseToSongNetease


class AlbumNeteaseSpider(BaseSpider):
    """
    网易云音乐专辑相关

    """
    name = 'album_netease'
    # start_url存放容器改为redis list
    redis_key = 'album_netease:start_urls'
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
        self.cursor.execute("select album_netease.id from album_netease "
                            "left join song_netease_to_album_netease "
                            "on album_netease.id=song_netease_to_album_netease.id_album_netease "
                            "where song_netease_to_album_netease.id_album_netease is null "
                            'limit {}'.format(default.SELECT_LIMIT))
        for id, in self.cursor.fetchall():
            first_param = "{}"
            fd = self.form_data.get_form_data(first_param=first_param, api_type=config.TYPE_WEAPI)
            yield scrapy.FormRequest(url='{}{}'.format(config.URL_ALBUM, id), formdata=fd,
                                     meta={'id': id}, callback=self.parse)

    def parse(self, response):
        album_id = response.meta['id']
        content = json.loads(response.text)
        if 'songs' in content:
            for song in content['songs']:
                item_song_to_album = SongNeteaseToAlbumNetease()
                item_song_to_album['id_song_netease'] = song['id']
                item_song_to_album['id_album_netease'] = album_id
                yield item_song_to_album
                item_song = SongNetease()
                item_song['id'] = song['id']
                item_song['name_zh'] = song['name']
                yield item_song
                print('---------')
                print(item_song)
                for artist in song['ar']:
                    item_artist = ArtistNetease()
                    item_artist['id'] = artist['id']
                    item_artist['name_zh'] = artist['name']
                    item_artist['url_portrait'] = ''
                    yield item_artist
                    item_artist_to_song = ArtistNeteaseToSongNetease()
                    item_artist_to_song['id_artist_netease'] = artist['id']
                    item_artist_to_song['id_song_netease'] = song['id']
                    yield item_artist_to_song
            self.logger.info('get netease album\'s songs success,album_id:{}'.format(album_id))
        else:
            self.logger.warning('get netease album\'s songs failed,album_id:{}'.format(album_id))
