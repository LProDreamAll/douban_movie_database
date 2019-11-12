# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import scrapy
from crawler.items.scene import Movie
from crawler.configs import scene as config

"""
关于场景

"""


class SceneSpider(scrapy.Spider):
    """
    关于电影的场景

    """

    name = 'scene'
    allowed_domains = ['api.mocation.cc']

    def start_requests(self):
        """
        爬取电影列表总数

        :return:
        """
        yield scrapy.Request(url=config.URL_MOVIE_LIST + '11111', callback=self.parse)

    def parse(self, response):
        """
        解析电影列表总数

        :param response:
        :return:
        """
        content = json.loads(response.text)
        if content['data'] and content['data']['total']:
            total = content['data']['total']
            self.logger.info('prepare to get movie list , total:{}'.format(total))
            # 获取每一页电影列表
            # for page in range(int(total / config.movie_list_num) + 1):
            for page in range(1):
                yield scrapy.Request(url='{}{}'.format(config.URL_MOVIE_LIST, page),
                                     callback=self.parse_movie_list)
        else:
            self.logger.error('get movie list failed')
            return

    def parse_movie_list(self, response):
        """
        解析电影列表

        :param response:
        :return:
        """
        content = json.loads(response.text)
        if content['data'] and content['data']['movies']:
            for movie in content['data']['movies']:
                # 获取电影列表中的电影
                yield scrapy.Request(url='{}{}'.format(config.URL_MOVIE, movie['id']),
                                     callback=self.parse_movie)
                # for place in movie['placeIds']:
                #     获取电影中的地点
                #     yield scrapy.Request(url='{}{}'.format(config.url_place, place),
                #                          callback=self.parse_place)
            self.logger.info(
                'get movie list success ,page:{},total:{}'.format(response.url.split('=')[-1],
                                                                  content['data']['total']))
        else:
            self.logger.warning(
                'get movie list failed ,page:{},total:{}'.format(response.url.split('=')[-1], content['data']['total']))

    def parse_movie(self, response):
        """
        解析电影详情

        :param response:
        :return:
        """
        content = json.loads(response.text)
        if content['data'] and content['data']['movie']:
            movie = content['data']['movie']
            item = Movie()
            item['id'] = movie['id']
            item['name_zh'] = movie['cname']
            item['name_en'] = movie['ename']
            item['start_year'] = movie['year']
            item['description'] = movie['overview']
            self.logger.info('get movie success, id:{},name:{}'.format(movie['id'], movie['cname']))
            return item
        else:
            self.logger.warning('get movie failed,possible id：{}'.format(response.url.split('/')[-1]))

    def parse_place(self, response):
        """
        解析地点详情

        :param response:
        :return:
        """
        content = json.loads(response.text)
        if content['data'] and content['data']['place']:
            place = content['data']['place']
            self.logger.info('get place success, id:{},name:{}'.format(place['id'], place['cname']))
        else:
            self.logger.warning('get place failed,possible id：{}'.format(response.url.split('/')[-1]))
