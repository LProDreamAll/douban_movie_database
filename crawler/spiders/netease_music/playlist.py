# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import scrapy
from crawler.tools.database_pool import database_pool
from crawler.tools.netease_encrypt import form_data
from crawler.configs import netease as config
from scrapy_redis.spiders import RedisSpider

from crawler.items.netease import SongNetease
from crawler.items.netease import SongNeteaseToPlaylistNetease


class PlaylistNeteaseSpider(RedisSpider):
    """
    网易云音乐歌单相关

    """
    name = 'playlist_netease'
    # start_url存放容器改为redis list
    redis_key = 'playlist_netease:start_urls'
    allowed_domains = ['music.163.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.netease_music.playlist.PlaylistNeteasePipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()
        self.form_data = form_data()

    def start_requests(self):
        # self.cursor.execute("select movie_douban.id,movie_douban.name_zh from movie_douban "
        #                     "left join movie_douban_to_netease "
        #                     "on movie_douban.id=movie_douban_to_netease.id_movie_douban "
        #                     "where movie_douban_to_netease.id_movie_douban is null ")
        # for id, keyword in self.cursor.fetchall():
        #     first_param = """{{s:"{}",type:"web"}}""".format(keyword)
        #     fd = self.form_data.get_form_data(first_param=first_param, api_type=config.TYPE_WEAPI)
        #     yield scrapy.FormRequest(url=config.URL_SEARCH_TIPS,
        #                              formdata=fd,
        #                              meta={'id': id, 'keyword': keyword}, callback=self.parse)
        id = 376493212
        first_param = """{{id:"{}",n:"{}",s:"{}"}}""".format(id, 100000, 0)
        fd = self.form_data.get_form_data(first_param=first_param, api_type=config.TYPE_WEAPI)
        yield scrapy.FormRequest(url=config.URL_PLAYLIST, formdata=fd, meta={'id': id}, callback=self.parse)

    def parse(self, response):
        playlist_id = response.meta['id']
        content = json.loads(response.text)
        if 'playlist' in content and 'tracks' in content['playlist']:
            for song in content['playlist']['tracks']:
                print(song)
                item_song_to_playlist = SongNeteaseToPlaylistNetease()
                item_song_to_playlist['id_song_netease'] = song['id']
                item_song_to_playlist['id_playlist_netease'] = playlist_id
                item_song_to_playlist['song_pop'] = song['pop']
                yield item_song_to_playlist
                item_song = SongNetease()
                item_song['id'] = song['id']
                item_song['id_movie_douban'] = 0
                item_song['name_zh'] = song['name']
                yield item_song
                print('---------')
                print(item_song)
            self.logger.info('get netease playlist\'s songs success,playlist_id:{}'.format(playlist_id))
        else:
            self.logger.warning('get netease playlist\'s songs failed,playlist_id:{}'.format(playlist_id))
