# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import random
import re
import string
import scrapy
from crawler.tools.database_pool import database_pool
from crawler.configs import movie_douban as config

from crawler.items.movie_douban import MovieDouban
from crawler.items.movie_douban import AliasMovieDouban
from crawler.items.movie_douban import MovieDoubanToCelebrityDouban


class MovieDoubanSpider(scrapy.Spider):
    """
    豆瓣电影相关

    """
    name = 'movie_douban'
    allowed_domains = ['movie.douban.com']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()

    def start_requests(self):
        self.cursor.execute('select id from movie_douban where start_year=0 and id_movie_imdb=0')
        for id, in self.cursor.fetchall():
            yield scrapy.Request(url="{}{}/".format(config.URL_MOVIE_DOUBAN, id),
                                 cookies=self.get_cookie_douban(),
                                 meta={'id': id}, callback=self.parse)

    def parse(self, response):
        if response.xpath('//div[@id="content"]'):
            movie_id = response.meta['id']
            info = response.xpath('//div[@id="info"]')
            title = response.xpath('//h1/span[1]/text()').get()
            start_year = response.xpath('//h1/span[@class="year"]/text()').get()
            type_list = info.xpath('span[@property="v:genre"]/text()').getall()
            imdb_id = info.xpath('span[text()="IMDb链接:"]/following-sibling::a/text()').get()
            alias_label = info.xpath('span[text()="又名:"]').get()
            runtime = info.xpath('span[@property="v:runtime"]/text()').get()
            # 豆瓣电影
            item_movie = MovieDouban()
            item_movie['id'] = movie_id
            # 影片类型 1:未知 2:电影 3:电视剧 4:短片
            item_movie['id_type_video'] = 2
            if '集数:' in info.xpath('/span/text()').getall():
                item_movie['id_type_video'] = 3
            elif '短片' in type_list:
                item_movie['id_type_video'] = 4
            item_movie['id_movie_imdb'] = re.search('tt(\d+)', imdb_id).group(1) if imdb_id is not None else 0
            item_movie['start_year'] = re.search('[(](\d+)[)]',
                                                 start_year).group(1) if start_year is not None else 0
            # 中文名
            item_movie['name_zh'] = re.search('[\u4e00-\u9fff()\d\s]*',
                                              title).group().strip() if title is not None else ''
            # 原始名
            item_movie['name_origin'] = re.search('[\u4e00-\u9fff()\d\s]*(.*)',
                                                  title).group(1).strip() if title is not None else ''
            # 除中文名以外其他名
            item_movie['name_alias'] = ''
            if alias_label is not None and imdb_id is not None:
                item_movie['name_alias'] =
            item_movie['runtime'] = re.search('\d+', runtime).group() if runtime is not None else 0
            item_movie['url_poster'] = response.xpath('//a[@class="nbgnbg"]/img/@src').get()
            print(item_movie)
            yield item_movie
            # 电影别名
            if alias_label is not None:
                alias_position = 1 if imdb_id is None else 3
                alias_list = info.xpath('text()[last()-{}]'.format(alias_position)).get().split('/')
                for alias in alias_list:
                    item_alias = AliasMovieDouban()
                    item_alias['id_movie_douban'] = movie_id
                    item_alias['name_alias'] = alias.strip()
                    print(item_alias)
                    yield item_alias
            # 电影影人
            celebrity_list = response.xpath('//div[@id="info"]//span/a')
            count = 0
            for celebrity in celebrity_list:
                # 影人类型 2：导演 3:编剧 4：主演
                item_movie_to_celebrity = MovieDoubanToCelebrityDouban()
                item_movie_to_celebrity['id_movie_douban'] = movie_id
                item_movie_to_celebrity['id_celebrity_douban'] = re.search('\d+',
                                                                           celebrity.xpath('@href').get()).group()
                if celebrity.xpath('@ref') == 'v:starring':
                    item_movie_to_celebrity['id_profession'] = 4
                    count += 1
                    item_movie_to_celebrity['sort'] = count
                elif celebrity.xpath('@rel') == 'v:directedBy':
                    item_movie_to_celebrity['id_profession'] = 2
                    item_movie_to_celebrity['sort'] = 0
                elif celebrity.xpath('@class="more-actor"') is not None:
                    continue
                else:
                    item_movie_to_celebrity['id_profession'] = 3
                    item_movie_to_celebrity['sort'] = 0
                yield item_movie_to_celebrity
            # 电影类型
            # code

            self.logger.info('get douban movie success,id:{}'.format(movie_id))
        else:
            self.logger.warning('get douban movie failed,id:{}'.format(movie_id))

    def get_cookie_douban(self):
        """
        豆瓣cookie随机生成

        :return:字典形式的cookie
        """
        return {'Cookie': 'bid=%s' % ''.join(random.sample(string.ascii_letters + string.digits, 11))}
