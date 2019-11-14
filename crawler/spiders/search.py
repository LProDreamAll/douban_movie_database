# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

import json
import scrapy
from scrapy_redis.spiders import RedisSpider
from crawler.tools.database_pool import database_pool
from crawler.configs import search as config

from crawler.items.search import MovieDouban


class SearchSpider(RedisSpider):
    """
    关于搜索匹配,以下五种情况对应搜索

    用法： scrapy crawl search -a type=

    imdb_tt         IMDB的tt
    imdb_nm         IMDB的nm
    scene_movie     片场的 name(电影)
    scene_celebrity 片场的 name(人物)
    resource        资源的 name(电影)

    """

    name = 'search'
    # start_url存放容器改为redis list
    redis_key = 'search:start_urls'
    allowed_domains = ['movie.douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.search.SearchPipeline': 300
        }
    }

    # def __init__(self, **kwargs):
    # def __init__(self, type=None, **kwargs):
    #     super().__init__(**kwargs)
    # self.type = type
    # super().__init__(**kwargs)
    # self.conn = database_pool.connection()
    # self.cursor = self.conn.cursor()

    def start_requests(self):
        """
        爬取搜索内容

        :return:
        """
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute('select id,start_year from movie_imdb')
        for id, year in self.cursor.fetchall():
            # yield scrapy.Request(url=config.URL_SEARCH_MOVIE_DOUBAN + 'tt' + '%07d' % id, meta={'year': year},
            yield scrapy.Request(url=config.URL_SEARCH_MOVIE_DOUBAN + 'tt' + '%07d' % id, callback=self.parse)

    def parse(self, response):
        """
        解析搜索内容

        :param response:
        :return:
        """
        content = json.loads(response.text)
        if content:
            # 电影类型 and 上映时间+-3
            if content[0]['type'] == 'movie':
                # if content[0]['type'] == 'movie' and abs(int(content[0]['year']) - response.meta['year']) <= 3:
                item_movie_douban = MovieDouban()
                item_movie_douban['id'] = content[0]['id']
                item_movie_douban['name_zh'] = content[0]['title']
                yield item_movie_douban
