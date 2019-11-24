# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
from crawler.configs import douban as config
from crawler.spiders.base import BaseSpider

from crawler.items.douban import ImageMovieDouban
from crawler.items.douban import ImageCelebrityDouban


class ImageDoubanSpider(BaseSpider):
    """
    图片相关

    用法： scrapy crawl image_douban -a type=

    movie       豆瓣电影的图片
    celebrity   豆瓣影人的图片

    """
    name = 'image_douban'
    # start_url存放容器改为redis list
    redis_key = 'image_douban:start_urls'
    allowed_domains = ['movie.douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.douban_movie.douban.DoubanPipeline': 300
        }
    }

    def __init__(self, type=None, **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.type_movie = 'movie'
        self.type_celebrity = 'celebrity'

    def prepare(self, offset, limit):
        """
        获取请求列表

        :param offset:
        :param limit:
        :return:
        """
        if self.type == self.type_movie:
            self.cursor.execute(
                'select movie_douban.id from movie_douban '
                'left join image_movie_douban '
                'on movie_douban.id=image_movie_douban.id_movie_douban '
                'where image_movie_douban.id_movie_douban is null '
                'limit {},{}'.format(offset, limit))
            for id, in self.cursor.fetchall():
                yield scrapy.Request(url="{}{}{}".format(config.URL_IMAGE_MOVIE_START, id, config.URL_IMAGE_MOVIE_END),
                                     cookies=config.get_cookie_douban(),
                                     meta={'id': id}, callback=self.parse)
        elif self.type == self.type_celebrity:
            self.cursor.execute(
                'select celebrity_douban.id from celebrity_douban '
                'left join image_celebrity_douban '
                'on celebrity_douban.id=image_celebrity_douban.id_celebrity_douban '
                'where image_celebrity_douban.id_celebrity_douban is null '
                'limit {},{}'.format(offset, limit))
            for id, in self.cursor.fetchall():
                yield scrapy.Request(
                    url="{}{}{}".format(config.URL_IMAGE_CELEBRITY_START, id, config.URL_IMAGE_CELEBRITY_END),
                    cookies=config.get_cookie_douban(),
                    meta={'id': id}, callback=self.parse)
        self.logger.info(
            'get douban image\'s request list success,type:{},offset:{},limit:{}'.format(self.type, offset, limit))

    def parse(self, response):
        """
        解析电影图片

        :param response:
        :return:
        """
        id = response.meta['id']
        image_list = response.xpath('//div[@class="article"]//li')
        if image_list:
            for index, image in enumerate(image_list):
                item_image = {}
                if self.type == self.type_movie:
                    item_image = ImageMovieDouban()
                elif self.type == self.type_celebrity:
                    item_image = ImageCelebrityDouban()
                item_image['id'] = re.search('photo/(\d+)', image.xpath('.//div[@class="cover"]/a/@href').get()).group(
                    1)
                if self.type == self.type_movie:
                    item_image['id_movie_douban'] = id
                elif self.type == self.type_celebrity:
                    item_image['id_celebrity_douban'] = id
                item_image['sort'] = index + 1
                size = image.xpath('.//div[@class="prop"]/text()').get().split('x')
                item_image['length'] = re.search('\d+', size[0]).group()
                item_image['width'] = re.search('\d+', size[1]).group()
                print('-----------------')
                print(item_image)
                yield item_image
            self.logger.info('get douban image success,id:{},type:{}'.format(id, self.type))
        else:
            self.logger.warning('get douban image failed,id:{},type:{}'.format(id, self.type))
        # 获取新的请求列表
        self.count += 1
        if self.count % self.limit == 0:
            for request in self.prepare(self.count, self.limit):
                yield request
