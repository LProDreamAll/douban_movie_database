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
from crawler.items.netease import PlaylistNetease
from crawler.items.netease import AlbumNetease
from crawler.items.netease import MovieDoubanToNetease


class SearchNeteaseSpider(RedisSpider):
    """
    网易云音乐搜索相关

    """
    name = 'search_netease'
    # start_url存放容器改为redis list
    redis_key = 'search_netease:start_urls'
    allowed_domains = ['music.163.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.netease_music.search.SearchNeteasePipeline': 300
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
        keyword = '阿甘正传'
        first_param_dict = config.EAPI_PARAMS
        first_param_dict['s'] = keyword
        first_param_dict['type'] = 1
        first_param = json.dumps(first_param_dict, separators=(',', ':'))
        fd = self.form_data.get_form_data(first_param=first_param, api_type=config.TYPE_EAPI,
                                          eapi_url=config.URL_SEARCH_TIPS_EAPI)
        yield scrapy.FormRequest(url=config.URL_SEARCH_TIPS,
                                 formdata=fd, meta={'id': id, 'keyword': keyword}, callback=self.parse)

    def parse(self, response):
        movie_id = response.meta['id']
        keyword = response.meta['keyword']
        content = json.loads(response.text)
        result = content['result']
        if 'result' in content and ('songs' in result or 'playlists' in result or 'albums' in result):
            # 歌曲
            if 'songs' in result:
                for song in result['songs']:
                    item_movie_to_netease = MovieDoubanToNetease()
                    item_movie_to_netease['id_movie_douban'] = movie_id
                    item_movie_to_netease['id_netease'] = song['id']
                    item_movie_to_netease['type_netease'] = 1
                    yield item_movie_to_netease
                    item_song = SongNetease()
                    item_song['id'] = song['id']
                    item_song['id_movie_douban'] = movie_id
                    item_song['name_zh'] = song['name']
                    yield item_song
                    print('---------------')
                    print(item_song)
            # 歌单
            if 'playlists' in result:
                for playlist in result['playlists']:
                    item_movie_to_netease = MovieDoubanToNetease()
                    item_movie_to_netease['id_movie_douban'] = movie_id
                    item_movie_to_netease['id_netease'] = playlist['id']
                    item_movie_to_netease['type_netease'] = 2
                    yield item_movie_to_netease
                    item_playlist = PlaylistNetease()
                    item_playlist['id'] = playlist['id']
                    item_playlist['id_movie_douban'] = movie_id
                    item_playlist['name_zh'] = playlist['name']
                    item_playlist['total'] = playlist['trackCount']
                    item_playlist['play_count'] = playlist['playCount']
                    item_playlist['url_cover'] = playlist['coverImgUrl']
                    item_playlist['description'] = playlist['description']
                    yield item_playlist
                    print('---------------')
                    print(item_playlist)
            # 专辑
            if 'albums' in result:
                for album in result['albums']:
                    item_movie_to_netease = MovieDoubanToNetease()
                    item_movie_to_netease['id_movie_douban'] = movie_id
                    item_movie_to_netease['id_netease'] = album['id']
                    item_movie_to_netease['type_netease'] = 3
                    yield item_movie_to_netease
                    item_album = AlbumNetease()
                    item_album['id'] = album['id']
                    item_album['id_movie_douban'] = movie_id
                    item_album['name_zh'] = album['name']
                    item_album['total'] = album['size']
                    yield item_album
                    print('----------------')
                    print(item_album)
            self.logger.info('get netease search success,movie_id:{},keyword:{}'.format(movie_id, keyword))
        else:
            self.logger.warning('get netease search failed,movie_id:{},keyword:{}'.format(movie_id, keyword))
