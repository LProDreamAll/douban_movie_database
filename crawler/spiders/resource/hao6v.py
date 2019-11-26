# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
from crawler.configs import resource as config
from crawler.spiders.base import BaseSpider

from crawler.items.resource import ResourceMovie


class Hao6vResourceSpider(BaseSpider):
    """
    6v电影网资源相关

    """
    name = 'hao6v_resource'
    # start_url存放容器改为redis list
    redis_key = 'hao6v_resource:start_urls'
    allowed_domains = ['www.hao6v.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.resource.ResourcePipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_sum = len(config.HAO6V_TYPE_LIST)

    def start_requests(self):
        yield scrapy.Request(url='{}/s/{}/'.format(config.URL_HAO6V, config.HAO6V_TYPE_LIST[0]),
                             meta={'type_id': 0, 'page_id': 1}, callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        type_id = response.meta['type_id']
        page_id = response.meta['page_id']
        # 爬虫结束
        if type_id >= self.type_sum:
            self.crawler.engine.close_spider(self, 'get hao6v resource finished')
        # 电影列表
        movie_list = response.xpath('//ul[@class="list"]/li/a')
        if movie_list:
            for movie in movie_list:
                url = movie.xpath('@href').get()
                title = movie.xpath('text()').get()
                name = re.search('《(.*)》', title).group(1) if title is not None else ''
                year = re.match('\d*', title).group() if title is not None else ''
                yield scrapy.Request(url='{}{}'.format(config.URL_HAO6V, url),
                                     meta={
                                         'movie_id': re.search('/(.*)\.html', url).group(),
                                         'movie_name': name,
                                         'year': year},
                                     callback=self.parse_movie)
            self.logger.info(
                'get hao6v\'s movie list success,type:{},page:{}'.format(config.HAO6V_TYPE_LIST[type_id], page_id))
        else:
            self.logger.warning(
                'get hao6v\'s movie list failed,type:{},page:{}'.format(config.HAO6V_TYPE_LIST[type_id], page_id))
        # 下一页
        next_page = response.xpath('//div[@class="listpage"][1]/a[text()="下一页"]/@href').get()
        if next_page is None:
            next_page = '/s/{}/'.format(config.HAO6V_TYPE_LIST[type_id + 1])
            next_type_id = type_id + 1
            next_page_id = 1
        else:
            next_type_id = type_id
            next_page_id = page_id + 1
        yield scrapy.Request(url='{}{}'.format(config.URL_HAO6V, next_page),
                             meta={'type_id': next_type_id, 'page_id': next_page_id},
                             callback=self.parse_movie_list)

    def parse_movie(self, response):
        movie_id = response.meta['movie_id']
        movie_name = response.meta['movie_name']
        year = response.meta['year']
        resource_list = response.xpath('//tbody/tr/td')
        if resource_list:
            for resource in resource_list:
                url = resource.xpath('a/@href').get()
                text = ''.join(resource.xpath('text()').getall())
                if '网盘' in text:
                    name_origin = '网盘提取码:{}'.format(re.search('[a-zA-Z0-9]{4}', text).group())
                    type_id = 102
                else:
                    name_origin = resource.xpath('a/text()').get()
                    type_id = config.parse_type(name_origin)
                item_resource = ResourceMovie()
                item_resource['id_movie_douban'] = 0
                item_resource['id_movie_imdb'] = 0
                item_resource['id_website_resource'] = 105
                item_resource['id_type_resource'] = type_id
                item_resource['name_zh'] = movie_name
                item_resource['create_year'] = year
                item_resource['name_origin'] = name_origin
                item_resource['url_resource'] = url
                yield item_resource
                print('-------------------------')
                print(item_resource)
            self.logger.info('get hao6v\'s movie success,movie_id:{},movie_name:{}'.format(movie_id, movie_name))
        else:
            self.logger.warning('get hao6v\'s movie failed,movie_id:{},movie_name:{}'.format(movie_id, movie_name))
