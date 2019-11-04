# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import scrapy


class SceneSpider(scrapy.Spider):
    """
    关于电影的场景

    """

    name = 'scene'
    allowed_domains = ['api.mocation.cc']
    start_url = 'http://api.mocation.cc/api/movie/hot-and-default?page=11111'
    custom_settings = {
        # 电影列表 + 页码
        'URL_MOVIE_LIST': 'http://api.mocation.cc/api/movie/hot-and-default?page=',
        # 电影列表每页电影的个数
        'MOVIE_LIST_NUM': 30,
        # 电影详情 + 电影ID
        'URL_MOVIE': 'http://api.mocation.cc/api/movie/',
        # 地点详情 + 地点ID
        'URL_PLACE': 'http://api.mocation.cc/api/place/'
    }

    def parse(self, response):
        """
        解析电影列表总数

        :param response:
        :return:
        """
        content = json.loads(response.text)
        if content['data'] and content['data']['total']:
            total = content['data']['total']
            self.logger.debug('prepare to get movie list , total:{}'.format(total))
            # 获取每一页电影列表
            for page in range(total / self.custom_settings['MOVIE_LIST_NUM'] + 1):
                yield scrapy.Request(url='{}{}'.format(self.custom_settings['URL_MOVIE_LIST'], page),
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
        if content['data'] and content['data']['movie']:
            for movie in content['data']['movie']:
                # 获取电影列表中的电影
                yield scrapy.Request(url='{}{}'.format(self.custom_settings['URL_MOVIE'], movie['id']),
                                     callback=self.parse_movie)
                for place in movie['placeIds']:
                    # 获取电影中的地点
                    yield scrapy.Request(url='{}{}'.format(self.custom_settings['URL_PLACE'], place),
                                         callback=self.parse_place)
            self.logger.debug(
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
            pass

    def parse_place(self, response):
        """
        解析地点详情

        :param response:
        :return:
        """
        content = json.loads(response.text)
        if content['data'] and content['data']['movie']:
            pass
