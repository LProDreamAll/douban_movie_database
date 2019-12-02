# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

import re
import execjs
import scrapy
from crawler.configs import default
from crawler.configs import douban as config
from crawler.spiders.base import BaseSpider

from crawler.items.search import ResourceMovie
from crawler.items.search import MovieDouban
from crawler.items.search import MovieScene
from crawler.items.search import CelebrityDouban
from crawler.items.search import CelebrityScene
from crawler.items.search import MovieImdb
from crawler.items.search import CelebrityImdb


class SearchDoubanSpider(BaseSpider):
    """
    关于豆瓣电影搜索

    用法：
    scrapy crawl search_douban -a type={}
    - movie_imdb        根据imdb_ID获取豆瓣电影ID
    - celebrity_imdb    根据imdb_ID获取豆瓣影人ID
    - movie_scene       根据场景_名称获取豆瓣电影ID
    - celebrity_scene   根据场景_名称获取豆瓣影人ID
    - movie_resource    根据资源_名称获取豆瓣电影ID

    """

    name = 'search_douban'
    # start_url存放容器改为redis list
    redis_key = 'search_douban:start_urls'
    allowed_domains = ['search.douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.douban_movie.search.SearchDoubanPipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 类型
        self.type_movie_imdb = 'movie_imdb'
        self.type_celebrity_imdb = 'celebrity_imdb'
        self.type_movie_scene = 'movie_scene'
        self.type_celebrity_scene = 'celebrity_scene'
        self.type_movie_resource = 'movie_resource'
        # 编译JS解密代码,通过call调用
        self.decrypt_js = execjs.compile(
            open(config.PATH_DOUBAN_SEARCH_DECRYPT, mode='r', encoding='gbk', errors='ignore').read())
        # 用于更新数据库的游标
        self.cursor_update = self.conn.cursor()

    def start_requests(self):
        # 从imdb获取待请求电影列表
        if self.type == self.type_movie_imdb:
            self.cursor.execute('select movie_imdb.id,movie_imdb.start_year from movie_imdb '
                                'left join movie_douban '
                                'on movie_imdb.id=movie_douban.id_movie_imdb '
                                'where movie_douban.id_movie_imdb is null '
                                'and movie_imdb.id_movie_douban=0 '
                                'and movie_imdb.start_year<=2019 '
                                'and movie_imdb.runtime>=60 '
                                'order by movie_imdb.start_year desc '
                                'limit {}'.format(default.SELECT_LIMIT))
            for id, start_year in self.cursor.fetchall():
                yield scrapy.Request(url=config.URL_SEARCH_MOVIE + 'tt' + '%07d' % id,
                                     meta={'id': id, 'start_year': start_year}, cookies=config.get_cookie_douban(),
                                     callback=self.parse)
        # 从scene获取待请求电影列表
        elif self.type == self.type_movie_scene:
            self.cursor.execute('select id,name_zh,start_year from movie_scene '
                                'where id_movie_douban=0 '
                                'limit {}'.format(default.SELECT_LIMIT))
            for id, name_zh, start_year in self.cursor.fetchall():
                result = self.match_movie(name_zh, start_year)
                # 在movie_douban中匹配到指定电影,更新数据库
                if result[0]:
                    item_movie_scene = MovieScene()
                    item_movie_scene['id'] = id
                    item_movie_scene['id_movie_douban'] = result[1]
                    self.cursor_update.execute('insert into movie_scene(id,id_movie_douban) values({0},{1}) '
                                               'on duplicate key update '
                                               'id_movie_douban={1}'.format(id, result[1]))
                    # print('scene (mysql) ---------')
                    # print(id)
                    # print(result[1])
                    self.logger.info('get mysql- list success,id:{},name:{},type:{}'
                                     .format(id, name_zh, self.type))
                # 匹配失败,采用search方式
                else:
                    yield scrapy.Request(url=config.URL_SEARCH_MOVIE + name_zh,
                                         meta={'id': id, 'start_year': start_year},
                                         cookies=config.get_cookie_douban(),
                                         callback=self.parse)
            self.conn.commit()
        # 从resource获取待请求电影列表,根据 名称,年份 匹配电影
        elif self.type == self.type_movie_resource:
            self.cursor.execute('select id,id_movie_imdb,name_zh,create_year from resource_movie '
                                'where id_movie_douban=0 '
                                'and id_website_resource> 100 '
                                'and id_type_resource>=100 '
                                'limit {}'.format(default.SELECT_LIMIT))
            for id, id_movie_imdb, name_zh, create_year in self.cursor.fetchall():
                # 根据imdb编号找到对应电影
                if id_movie_imdb != 0:
                    cursor2 = self.conn.cursor()
                    cursor2.execute('select id from movie_douban where id_movie_imdb={}'.format(id_movie_imdb))
                    result = cursor2.fetchall()
                    if len(result) == 1:
                        id_movie_douban = result[0][0]
                    # search根据imdb编号找到对应电影
                    else:
                        yield scrapy.Request(url=config.URL_SEARCH_MOVIE + 'tt' + '%07d' % id_movie_imdb,
                                             meta={'id': id, 'start_year': create_year}, callback=self.parse)
                        continue
                # idmb编号为0,根据电影名和年份找到对应电影
                else:
                    result = self.match_movie(name_zh, create_year)
                    id_movie_douban = result[1] if result[0] else 0
                # 在movie_douban中匹配到指定电影
                if id_movie_douban != 0:
                    self.cursor_update.execute('insert into resource_movie(id,id_movie_douban) '
                                               'values ({0},{1}) '
                                               'on duplicate key update '
                                               'id_movie_douban={1}}'.format(id, id_movie_douban))
                    # print('resource (mysql) ----------')
                    # print(id)
                    # print(id_movie_douban)
                # 匹配失败,采用search方式
                else:
                    yield scrapy.Request(url='{}{}'.format(config.URL_SEARCH_MOVIE, name_zh),
                                         meta={'id': id, 'start_year': create_year}, callback=self.parse)
            self.conn.commit()
        # 从imdb获取待请求影人列表
        elif self.type == self.type_celebrity_imdb:
            self.cursor.execute('select celebrity_imdb.id from celebrity_imdb '
                                'left join celebrity_douban '
                                'on celebrity_imdb.id=celebrity_douban.id_celebrity_imdb '
                                'where celebrity_douban.id_celebrity_imdb is null '
                                'and celebrity_imdb.id_celebrity_douban=0 '
                                'limit {}'.format(default.SELECT_LIMIT))
            for id, in self.cursor.fetchall():
                yield scrapy.Request(url=config.URL_SEARCH_MOVIE + 'nm' + '%07d' % id, meta={'id': id},
                                     cookies=config.get_cookie_douban(), callback=self.parse)
        # 从scene获取待请求影人列表
        elif self.type == self.type_celebrity_scene:
            self.cursor.execute('select id,name_en from celebrity_scene '
                                'where id_celebrity_douban=0 and name_en!="" '
                                'limit {}'.format(default.SELECT_LIMIT))
            for id, name_en in self.cursor.fetchall():
                # 从celebrity_douban中匹配影人
                cursor2 = self.conn.cursor()
                cursor2.execute('select id from celebrity_douban '
                                'where name_origin="{}"'.format(name_en))
                result = cursor2.fetchall()
                # 匹配到唯一的指定影人
                if len(result) == 1:
                    self.cursor_update.execute('insert into celebrity_scene(id,id_celebrity_douban) values ({0},{1}) '
                                               'on duplicate key update '
                                               'id_celebrity_douban={1} '.format(id, result[0][0]))
                    # print('celebrity_scene (mysql) ----------')
                    # print(id)
                    # print(result[0][0])
                # 匹配失败,采用search
                else:
                    yield scrapy.Request(url=config.URL_SEARCH_MOVIE + name_en, meta={'id': id},
                                         cookies=config.get_cookie_douban(), callback=self.parse)
            self.conn.commit()

    def parse(self, response):
        id = response.meta['id']
        if response.xpath('//div[@id="wrapper"]'):
            # 标记是否取得结果 True：取得结果 False:未取得结果
            flag = False
            # 解密搜索结果中的window.__DATA__
            data_encrypted = re.search('window.__DATA__ = "([^"]*)"',
                                       response.xpath('/html/body/script[6]/text()').get()).group(1)
            title_list = self.decrypt_js.call('decrypt', data_encrypted)['payload']['items']
            if title_list:
                for title in title_list:
                    # 标题类型 search_common：影人 search_subject：电影
                    title_type = title['tpl_name']
                    if title_type not in ('search_common', 'search_subject'):
                        continue
                    # 电影类型,匹配中文名
                    title_name = ''
                    if title['title'] is not None:
                        title_name = re.search('[\u4e00-\u9fff()\?？!！,，\.。：·\d\s]*', title['title']).group().strip()
                    # 标题时间 括号中的年份 celebrity类型则为空
                    title_year = 0
                    if title_type == 'search_subject':
                        title_year_re = re.search('[(](\d+)[)]', title['title'])
                        if title_year_re is not None:
                            title_year = title_year_re.group(1)
                    # 标题ID
                    title_id = title['id']
                    # 当前任务为电影类型 and 搜索结果为电影类型 and 上映时间在精确度范围内
                    if self.type.split('_')[0] == 'movie' and title_type == 'search_subject' and abs(
                            int(title_year) - response.meta['start_year']) <= config.ACCURACY_RELEASE_TIME:
                        if self.type == self.type_movie_imdb:
                            item_movie_douban = MovieDouban()
                            item_movie_douban['id'] = title_id
                            item_movie_douban['id_movie_imdb'] = id
                            item_movie_douban['name_zh'] = title_name
                            item_movie_douban['start_year'] = title_year
                            yield item_movie_douban
                            # print('---------')
                            # print(item_movie_douban)
                            item_movie_imdb = MovieImdb()
                            item_movie_imdb['id'] = id
                            item_movie_imdb['id_movie_douban'] = title_id
                            yield item_movie_imdb
                        elif self.type == self.type_movie_scene:
                            item_movie_scene = MovieScene()
                            item_movie_scene['id'] = id
                            item_movie_scene['id_movie_douban'] = title_id
                            yield item_movie_scene
                            # print('scene (douban search) ----------')
                            # print(item_movie_scene)
                        elif self.type == self.type_movie_resource:
                            item_resource = ResourceMovie()
                            item_resource['id'] = id
                            item_resource['id_movie_douban'] = title_id
                            yield item_resource
                            # print('resource (douban search) ----------')
                            # print(item_resource)
                        flag = True
                    # 当前任务为影人类型 and 搜索结果为影人类型
                    elif self.type.split('_')[0] == 'celebrity' and title_type == 'search_common':
                        # 影人类型,匹配英文名
                        title_name = ''
                        if title['title'] is not None:
                            title_name = re.search('[\u4e00-\u9fff()·\s]*(.*)', title['title']).group(1).strip()
                        if self.type == self.type_celebrity_imdb:
                            item_celebrity_douban = CelebrityDouban()
                            item_celebrity_douban['id'] = title_id
                            item_celebrity_douban['id_celebrity_imdb'] = id
                            item_celebrity_douban['name_origin'] = title_name
                            yield item_celebrity_douban
                            # print('----------')
                            # print(item_celebrity_douban)
                            item_celebrity_imdb = CelebrityImdb()
                            item_celebrity_imdb['id'] = id
                            item_celebrity_imdb['id_celebrity_douban'] = title_id
                            yield item_celebrity_imdb
                        elif self.type == self.type_celebrity_scene:
                            item_celebrity_scene = CelebrityScene()
                            item_celebrity_scene['id'] = id
                            item_celebrity_scene['id_celebrity_douban'] = title_id
                            yield item_celebrity_scene
                            # print('-----------')
                            # print(item_celebrity_scene)
                        flag = True
                    # 找到最佳匹配结果，即可跳出
                    if flag:
                        self.logger.info('get search list success,id:{},name:{},type:{}'
                                         .format(id, title_name, self.type))
                        break
            # 搜索失败，部分类型标记为已搜索，避免重复搜索
            if not flag:
                if self.type == self.type_movie_scene:
                    item_movie_scene = MovieScene()
                    item_movie_scene['id'] = response.meta['id']
                    item_movie_scene['id_movie_douban'] = 1
                    yield item_movie_scene
                elif self.type == self.type_celebrity_scene:
                    item_celebrity_scene = CelebrityScene()
                    item_celebrity_scene['id_celebrity_douban'] = 1
                    item_celebrity_scene['id'] = id
                    yield item_celebrity_scene
                elif self.type == self.type_movie_resource:
                    item_resource = ResourceMovie()
                    item_resource['id'] = id
                    item_resource['id_movie_douban'] = 1
                    yield item_resource
                elif self.type == self.type_movie_imdb:
                    item_movie_imdb = MovieImdb()
                    item_movie_imdb['id'] = id
                    item_movie_imdb['id_movie_douban'] = 1
                    yield item_movie_imdb
                elif self.type == self.type_celebrity_imdb:
                    item_celebrity_imdb = CelebrityImdb()
                    item_celebrity_imdb['id'] = id
                    item_celebrity_imdb['id_celebrity_douban'] = 1
                    yield item_celebrity_imdb
                self.logger.warning('get search list None,id:{},type:{}'.format(id, self.type))
        else:
            self.logger.error('get search list failed,id:{},type:{}'.format(id, self.type))

    def match_movie(self, name_zh, start_year):
        """
        从movie_douban中匹配对应电影

        :param name_zh: 电影中文名
        :param start_year: 电影年份
        :return: 是否匹配,豆瓣电影ID
        """
        cursor2 = self.conn.cursor()
        cursor2.execute('select id from movie_douban '
                        'where name_zh="{}" and '
                        '( start_year={} or start_year={} or start_year={}) '
                        .format(name_zh, start_year, start_year - 1, start_year + 1))
        result = cursor2.fetchall()
        # 匹配到指定电影
        if len(result) == 1:
            return True, result[0][0]
        # 未匹配到 / 甚至匹配到多个
        else:
            return False, None
