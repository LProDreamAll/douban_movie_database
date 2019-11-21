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
from crawler.items.netease import SongNeteaseToAlbumNetease


class AlbumNeteaseSpider(RedisSpider):
    """
    网易云音乐专辑相关

    """
    name = 'album_netease'
    # start_url存放容器改为redis list
    redis_key = 'album_netease:start_urls'
    allowed_domains = ['music.163.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.netease_music.album.AlbumNeteasePipeline': 300
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
        id = 35623243
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
                item_song['id_movie_douban'] = 0
                item_song['name_zh'] = song['name']
                yield item_song
                print('---------')
                print(item_song)
            self.logger.info('get netease album\'s songs success,album_id:{}'.format(album_id))
        else:
            self.logger.warning('get netease album\'s songs failed,album_id:{}'.format(album_id))
