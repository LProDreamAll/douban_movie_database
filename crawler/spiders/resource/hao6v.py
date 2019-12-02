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

    用法:
    scrapy crawl hao6v_resource -a type={}
    - all           该网站所有电影
    - new           该网站最新电影

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
        self.type_new = 'new'
        # 仅爬取最新电影的页数 (每种类型)
        self.new_max_pages = 10

    def start_requests(self):
        for type in config.HAO6V_TYPE_LIST:
            yield scrapy.Request(url='{}/s/{}/'.format(config.URL_HAO6V, type),
                                 meta={'type': type, 'page_id': 1}, callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        type = response.meta['type']
        page_id = response.meta['page_id']
        # 电影列表
        movie_list = response.xpath('//ul[@class="list"]/li/a')
        if movie_list:
            for movie in movie_list:
                url = movie.xpath('@href').get()
                title = movie.xpath('font/text()').get()
                if title is None:
                    title = movie.xpath('text()').get()
                name = ''
                year = 0
                name_xp = re.search('《(.*)》', title) if title != '' else None
                if name_xp is not None:
                    name = name_xp.group(1)
                year_xp = re.match('\d*', title) if title != '' else None
                if year_xp is not None:
                    year = year_xp.group()
                yield scrapy.Request(url='{}{}'.format(config.URL_HAO6V, url),
                                     meta={
                                         'movie_id': re.search('\d+/(.*)\.html', url).group(1),
                                         'movie_name': name,
                                         'year': year}, priority=2,
                                     callback=self.parse_movie)
            self.logger.info(
                'get hao6v movie list success,type:{},page:{}'.format(type, page_id))
            # 仅最新电影
            if self.type == self.type_new and page_id > self.new_max_pages:
                return
            # 下一页
            yield scrapy.Request(url='{}/s/{}/index_{}.html'.format(config.URL_HAO6V, type, page_id + 1),
                                 meta={'type': type, 'page_id': page_id + 1}, priority=1,
                                 callback=self.parse_movie_list)
        else:
            self.logger.error(
                'get hao6v movie list failed,type:{},page:{}'.format(type, page_id))

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
                    passwd = re.search('[a-zA-Z0-9]{4}', text)
                    if passwd:
                        name_origin = '网盘提取码:{}'.format(passwd.group())
                    else:
                        name_origin = '网盘链接'
                    type_id = 102
                elif '在线观看' in text:
                    if 'http://www.hao6v.com/diany' in url:
                        url = ''
                    else:
                        url = 'v_{}'.format(re.search('cc/(.*)\.html', url).group(1))
                    name_origin = '在线观看:《{}》'.format(movie_name)
                    type_id = 101
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
                # print('-------------------------')
                # print(item_resource)
            self.logger.info('get hao6v movie success,movie_id:{},movie_name:{}'.format(movie_id, movie_name))
        else:
            self.logger.error('get hao6v movie failed,movie_id:{},movie_name:{}'.format(movie_id, movie_name))
