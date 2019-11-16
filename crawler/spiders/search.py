# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

import random
import re
import string
import scrapy
from scrapy_redis.spiders import RedisSpider
from crawler.tools.database_pool import database_pool
from crawler.configs import search as config

from crawler.items.search import MovieDouban
from crawler.items.search import MovieScene
from crawler.items.search import CelebrityDouban
from crawler.items.search import CelebrityScene


class SearchSpider(RedisSpider):
    """
    关于搜索匹配,以下五种情况对应搜索

    用法： scrapy crawl search -a type=

    movie_imdb          IMDB的ttID(电影)
    celebrity_imdb      IMDB的nmID(人物)
    movie_scene         片场的name(电影)
    celebrity_scene     片场的name(人物)
    movie_resource      资源的name(电影)

    """

    name = 'search'
    # start_url存放容器改为redis list
    redis_key = 'search:start_urls'
    allowed_domains = ['search.douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.search.SearchPipeline': 300
        }
    }

    def __init__(self, type=None, **kwargs):
        super().__init__(**kwargs)
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()
        self.type = type
        self.type_movie_imdb = 'movie_imdb'
        self.type_celebrity_imdb = 'celebrity_imdb'
        self.type_movie_scene = 'movie_scene'
        self.type_celebrity_scene = 'celebrity_scene'
        self.type_movie_resource = 'movie_resource'

    def start_requests(self):
        """
        爬取搜索内容

        :return:
        """
        if self.type == self.type_movie_imdb:
            self.cursor.execute('select id,start_year from movie_imdb')
            for id, start_year in self.cursor.fetchall():
                yield scrapy.Request(url=config.URL_SEARCH_MOVIE_DOUBAN + 'tt' + '%07d' % id,
                                     meta={'id': id, 'start_year': start_year}, cookies=self.get_cookie_douban(),
                                     callback=self.parse)
        elif self.type == self.type_movie_scene:
            self.cursor.execute('select id,name_zh,start_year from movie_scene where id_movie_douban=0')
            for id, name_zh, start_year in self.cursor.fetchall():
                yield scrapy.Request(url=config.URL_SEARCH_MOVIE_DOUBAN + name_zh,
                                     meta={'id': id, 'start_year': start_year}, cookies=self.get_cookie_douban(),
                                     callback=self.parse)
        elif self.type == self.type_movie_resource:
            pass
        elif self.type == self.type_celebrity_imdb:
            self.cursor.execute('select id from celebrity_imdb')
            for id in self.cursor.fetchall():
                yield scrapy.Request(url=config.URL_SEARCH_MOVIE_DOUBAN + 'nm' + '%07d' % id, meta={'id': id},
                                     cookies=self.get_cookie_douban(), callback=self.parse)
        elif self.type == self.type_celebrity_scene:
            self.cursor.execute('select id,name_zh from celebrity_scene where id_celebrity_douban=0')
            for id, name_zh in self.cursor.fetchall():
                yield scrapy.Request(url=config.URL_SEARCH_MOVIE_DOUBAN + name_zh, meta={'id': id},
                                     cookies=self.get_cookie_douban(), callback=self.parse)

    def parse(self, response):
        """
        解析搜索内容

        :param response:
        :return:
        """
        print('--------------------------------------------------------------')
        print(response.url)

        # 标记是否取得结果 True：取得结果 False:未取得结果
        flag = False
        title_list = response.xpath('//div[@class="item-root"]//div[@class="title"]/a')
        print(title_list)
        if title_list:
            for title in title_list:
                text = title.xpath('text()').get()
                href = title.xpath('@href').get()
                print(text)
                print(href)
                # 标题类型 https://movie.douban.com/s... 第25个字符 s:movie类型 c:celebrity类型
                title_type = href[25]
                # 标题时间 括号中的年份 celebrity类型则为空
                title_year = re.findall(r'[(](.*?)[)]', text)[-1]
                # 标题名称
                title_name = text.split(' ')[0]
                # 标题ID
                title_id = re.findall(r'\d+', href)[-1]
                # 当前任务为电影类型 and 搜索结果为电影类型 and 上映时间在精确度范围内
                if self.type.split('_')[0] == 'movie' and title_type == 's' and abs(
                        int(title_year) - response.meta['start_year']) <= config.ACCURACY_RELEASE_TIME:
                    if self.type == self.type_movie_imdb:
                        item_movie_douban = MovieDouban()
                        item_movie_douban['id'] = title_id
                        item_movie_douban['name_zh'] = title_name
                        yield item_movie_douban
                    elif self.type == self.type_movie_scene:
                        item_movie_scene = MovieScene()
                        item_movie_scene['id_movie_douban'] = title_id
                        item_movie_scene['id'] = response.meta['id']
                        yield item_movie_scene
                    elif self.type == self.type_movie_resource:
                        # --- coding ---
                        pass
                    flag = True
                # 当前任务为影人类型 and 搜索结果为影人类型
                elif self.type.split('_')[0] == 'celebrity' and title_type == 'c':
                    if self.type == self.type_celebrity_imdb:
                        item_celebrity_douban = CelebrityDouban()
                        item_celebrity_douban['id'] = title_id
                        item_celebrity_douban['name_zh'] = title_name
                        yield item_celebrity_douban
                    elif self.type == self.type_celebrity_scene:
                        item_celebrity_scene = CelebrityScene()
                        item_celebrity_scene['id_celebrity_douban'] = title_id
                        item_celebrity_scene['id'] = response.meta['id']
                        yield item_celebrity_scene
                    flag = True
                # 找到最佳匹配结果，即可跳出
                if flag:
                    self.logger.info(
                        'get search list success,id:{},name:{},type:{}'.format(response.meta['id'], title_name,
                                                                               self.type))
                    break
        if not flag:
            # 搜索失败，部分类型标记为已搜索，避免重复搜索
            if self.type == self.type_movie_scene:
                item_movie_scene = MovieScene()
                item_movie_scene['id_movie_douban'] = 1
                item_movie_scene['id'] = response.meta['id']
                yield item_movie_scene
            elif self.type == self.type_celebrity_scene:
                item_celebrity_scene = CelebrityScene()
                item_celebrity_scene['id_celebrity_douban'] = 1
                item_celebrity_scene['id'] = response.meta['id']
                yield item_celebrity_scene
            self.logger.warning('get search list failed,id:{},type:{}'.format(response.meta['id'], self.type))

    def get_cookie_douban(self):
        """
        豆瓣cookie随机生成

        :return:字典形式的cookie
        """
        return {'Cookie': 'bid=%s' % ''.join(random.sample(string.ascii_letters + string.digits, 11))}
