# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

import re
import execjs
import scrapy
from crawler.configs import douban as config
from crawler.spiders.base import BaseSpider

from crawler.items.search import ResourceMovie
from crawler.items.search import MovieDouban
from crawler.items.search import MovieScene
from crawler.items.search import CelebrityDouban
from crawler.items.search import CelebrityScene


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

    def __init__(self, type=None, **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.type_movie_imdb = 'movie_imdb'
        self.type_celebrity_imdb = 'celebrity_imdb'
        self.type_movie_scene = 'movie_scene'
        self.type_celebrity_scene = 'celebrity_scene'
        self.type_movie_resource = 'movie_resource'
        # 编译JS解密代码,通过call调用
        self.decrypt_js = execjs.compile(
            open('./tools/douban_search_decrypt.js', mode='r', encoding='gbk', errors='ignore').read())

    def prepare(self, offset, limit):
        """
        获取请求列表

        :param offset:
        :param limit:
        :return:
        """
        # 从imdb获取待请求电影列表
        if self.type == self.type_movie_imdb:
            self.cursor.execute('select movie_imdb.id,movie_imdb.start_year from movie_imdb '
                                'left join movie_douban '
                                'on movie_imdb.id=movie_douban.id_movie_imdb '
                                'where movie_douban.id_movie_imdb is null '
                                'and movie_imdb.is_douban_updated=0 '
                                'limit {},{}'.format(offset, limit))
            for id, start_year in self.cursor.fetchall():
                yield scrapy.Request(url=config.URL_SEARCH_MOVIE + 'tt' + '%07d' % id,
                                     meta={'id': id, 'start_year': start_year}, cookies=config.get_cookie_douban(),
                                     callback=self.parse)
        # 从scene获取待请求电影列表
        elif self.type == self.type_movie_scene:
            self.cursor.execute('select id,name_zh,start_year from movie_scene '
                                'where id_movie_douban=0 and is_douban_updated=0 '
                                'limit {},{}'.format(offset, limit))
            for id, name_zh, start_year in self.cursor.fetchall():
                result = self.match_movie(name_zh, start_year)
                # 在movie_douban中匹配到指定电影
                if result[0]:
                    item_scene = MovieScene()
                    item_scene['id'] = id
                    item_scene['id_movie_douban'] = result[1]
                    yield item_scene
                    print('scene (mysql) ---------')
                    print(item_scene)
                # 匹配失败,采用search方式
                else:
                    yield scrapy.Request(url=config.URL_SEARCH_MOVIE + name_zh,
                                         meta={'id': id, 'start_year': start_year}, cookies=config.get_cookie_douban(),
                                         callback=self.parse)
        # 从resource获取待请求电影列表,根据 名称,年份 匹配电影
        elif self.type == self.type_movie_resource:
            self.cursor.execute('select id,name_zh,create_year from resource_movie '
                                'where id_movie_douban=0 and id_movie_imdb=0 and is_douban_updated=0 '
                                'and id_website_resource> 100 and id_type_resource>=100 '
                                'limit {},{}'.format(offset, limit))
            for id, name_zh, create_year in self.cursor.fetchall():
                result = self.match_movie(name_zh, create_year)
                # 在movie_douban中匹配到指定电影
                if result[0]:
                    item_resource = ResourceMovie()
                    item_resource['id'] = id
                    item_resource['id_movie_douban'] = result[1]
                    item_resource['id_movie_imdb'] = result[2]
                    yield item_resource
                    print('resource (mysql) ----------')
                    print(item_resource)
                # 匹配失败,采用search方式
                else:
                    yield scrapy.Request(url='{}{}'.format(config.URL_SEARCH_MOVIE, name_zh),
                                         meta={'id': id, 'start_year': create_year}, callback=self.parse)
        # 从imdb获取待请求影人列表
        elif self.type == self.type_celebrity_imdb:
            self.cursor.execute('select celebrity_imdb.id from celebrity_imdb '
                                'left join celebrity_douban '
                                'on celebrity_imdb.id=celebrity_douban.id_celebrity_imdb '
                                'where celebrity_douban.id_celebrity_imdb is null '
                                'limit {},{}'.format(offset, limit))
            for id, in self.cursor.fetchall():
                yield scrapy.Request(url=config.URL_SEARCH_MOVIE + 'nm' + '%07d' % id, meta={'id': id},
                                     cookies=config.get_cookie_douban(), callback=self.parse)
        # 从scene获取待请求影人列表
        elif self.type == self.type_celebrity_scene:
            self.cursor.execute('select id,name_en from celebrity_scene '
                                'where id_celebrity_douban=0 and is_douban_updated=0 '
                                'limit {},{}'.format(offset, limit))
            for id, name_en in self.cursor.fetchall():
                # 从celebrity_douban中匹配影人
                cursor2 = self.conn.cursor()
                cursor2.execute('select id from celebrity_douban '
                                'where name_en={}'.format(name_en))
                result = cursor2.fetchall()
                # 匹配到唯一的指定影人
                if len(result) == 1:
                    item_celebrity = CelebrityScene()
                    item_celebrity['id'] = id
                    item_celebrity['id_celebrity_douban'] = result[0][0]
                    yield item_celebrity
                # 匹配到多个影人
                elif len(result) > 1:
                    result2 = self.match_celebrity_scene(id, result)
                    if result2[0]:
                        item_celebrity = CelebrityScene()
                        item_celebrity['id'] = id
                        item_celebrity['id_celebrity_douban'] = result2[1]
                        yield item_celebrity
                # 匹配失败,采用search
                else:
                    yield scrapy.Request(url=config.URL_SEARCH_MOVIE + name_en, meta={'id': id},
                                         cookies=config.get_cookie_douban(), callback=self.parse)
        self.logger.info(
            'get douban search\'s request list success,type:{},offset:{},limit:{}'.format(self.type, offset, limit))

    def parse(self, response):
        """
        解析搜索内容

        :param response:
        :return:
        """
        # 标记是否取得结果 True：取得结果 False:未取得结果
        flag = False
        # 解密搜索结果中的window.__DATA__
        data_encrypted = re.search('window.__DATA__ = "([^"]*)"',
                                   response.xpath('/html/body/script[6]/text()').get()).group(1)
        title_list = self.decrypt_js.call('decrypt', data_encrypted)['payload']['items']
        id = response.meta['id']
        if title_list:
            for title in title_list:
                # 标题类型 search_common：影人 search_subject：电影
                title_type = title['tpl_name']
                if title_type not in ('search_common', 'search_subject'):
                    continue
                # 标题名称
                title_name = title['title'].split(' ')[0]
                # 标题时间 括号中的年份 celebrity类型则为空
                title_year = re.search('[(](\d+)[)]', title['title']).group(
                    1) if title_type == 'search_subject' else None
                # 标题ID
                title_id = title['id']
                # 当前任务为电影类型 and 搜索结果为电影类型 and 上映时间在精确度范围内
                if self.type.split('_')[0] == 'movie' and title_type == 'search_subject' and abs(
                        int(title_year) - response.meta['start_year']) <= config.ACCURACY_RELEASE_TIME:
                    if self.type == self.type_movie_imdb:
                        item_movie_douban = MovieDouban()
                        item_movie_douban['id'] = title_id
                        item_movie_douban['name_zh'] = title_name
                        yield item_movie_douban
                        print('---------')
                        print(item_movie_douban)
                    elif self.type == self.type_movie_scene:
                        item_movie_scene = MovieScene()
                        item_movie_scene['id_movie_douban'] = title_id
                        item_movie_scene['id'] = id
                        yield item_movie_scene
                        print('scene (douban search) ----------')
                        print(item_movie_scene)
                    elif self.type == self.type_movie_resource:
                        item_resource = ResourceMovie()
                        item_resource['id'] = id
                        item_resource['id_movie_douban'] = title_id
                        item_resource['id_movie_imdb'] = 0
                        yield item_resource
                        print('resource (douban search) ----------')
                        print(item_resource)
                    flag = True
                # 当前任务为影人类型 and 搜索结果为影人类型
                elif self.type.split('_')[0] == 'celebrity' and title_type == 'search_common':
                    if self.type == self.type_celebrity_imdb:
                        item_celebrity_douban = CelebrityDouban()
                        item_celebrity_douban['id'] = title_id
                        item_celebrity_douban['name_zh'] = title_name
                        yield item_celebrity_douban
                        print('----------')
                        print(item_celebrity_douban)
                    elif self.type == self.type_celebrity_scene:
                        if len(title_list) == 1:
                            item_celebrity_scene = CelebrityScene()
                            item_celebrity_scene['id_celebrity_douban'] = title_id
                            item_celebrity_scene['id'] = id
                            yield item_celebrity_scene
                            print('-----------')
                            print(item_celebrity_scene)
                        elif len(title_list) > 1:
                            # 当前搜索项影人所参与的电影集合
                            cursor = self.conn.cursor()
                            cursor.execute('select distinct id_movie_douban from movie_douban_to_celebrity_douban '
                                           'where id_celebrity_douban={}'.format(title_id))
                            result = self.match_celebrity_scene(title_id, cursor.fetchall())
                            if result[0]:
                                item_celebrity_scene = CelebrityScene()
                                item_celebrity_scene['id_celebrity_douban'] = title_id
                                item_celebrity_scene['id'] = id
                                yield item_celebrity_scene
                                print('-----------')
                                print(item_celebrity_scene)
                            else:
                                continue
                    flag = True
                # 找到最佳匹配结果，即可跳出
                if flag:
                    self.logger.info('get search list success,id:{},name:{},type:{}'
                                     .format(id, title_name, self.type))
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
                item_celebrity_scene['id'] = id
                yield item_celebrity_scene
            self.logger.warning('get search list failed,id:{},type:{}'.format(id, self.type))
        # 获取新的请求列表
        self.count += 1
        if self.count % self.limit == 0:
            for request in self.prepare(self.count, self.limit):
                yield request

    def match_movie(self, name_zh, start_year):
        """
        从movie_douban中匹配对应电影

        :param name_zh: 电影中文名
        :param start_year: 电影年份
        :return: 是否匹配,豆瓣电影ID,IMDB电影ID
        """
        cursor2 = self.conn.cursor()
        cursor2.execute('select id,id_movie_imdb from movie_douban '
                        'where name_zh={} and '
                        '( start_year={} or start_year={} or start_year={}) '
                        .format(name_zh, start_year, start_year - 1, start_year + 1))
        result = cursor2.fetchall()
        # 匹配到指定电影
        if len(result) == 1:
            return True, result[0][0], result[0][1]
        else:
            return False, None, None

    def match_celebrity_scene(self, id_celebrity_scene, id_celebrity_douban_list):
        """
        从多个豆瓣影人中匹配到唯一的指定影人

        :param id_celebrity_scene: 场景影人ID
        :param id_celebrity_douban_list: 豆瓣影人ID列表,格式: ((id,),(id,))
        :return:是否匹配到,该场景影人匹配到的豆瓣影人ID
        """
        # 场景影人ID -> 场景电影列表 -> 豆瓣电影ID列表
        cursor = self.conn.cursor()
        cursor.execute('select movie_scene.id_movie_douban from movie_scene '
                       'left join movie_scene_to_celebrity_scene '
                       'on movie_scene.id=movie_scene_to_celebrity_scene.id_movie_scene '
                       'where movie_scene_to_celebrity_scene.id_celebrity_scene={} '
                       'and movie_scene.id_movie_douban!=0'.format(id_celebrity_scene))
        # 豆瓣电影ID列表
        id_movie_douban_list = []
        for id_movie_douban, in cursor.fetchall():
            id_movie_douban_list.append(id_movie_douban)
        # 豆瓣影人ID列表中,若某个豆瓣影人参与了此场景影人ID的电影,则说明此场景影人大概率为当前豆瓣影人
        for id_celebrity_douban, in id_celebrity_douban_list:
            cursor2 = self.conn.cursor()
            cursor2.execute('select distinct id_movie_douban from movie_douban_to_celebrity_douban '
                            'where id_celebrity_douban={}'.format(id_celebrity_douban))
            for id_movie_douban, in cursor2.fetchall():
                if id_movie_douban in id_movie_douban_list:
                    return True, id_celebrity_douban
        return False, None
