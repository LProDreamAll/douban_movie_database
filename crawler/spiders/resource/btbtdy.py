# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
from crawler.configs import resource as config
from crawler.spiders.base import BaseSpider

from crawler.items.resource import ResourceMovie


class BtbtdyResourceSpider(BaseSpider):
    """
    BT电影天堂资源相关

    用法:
    scrapy crawl btbtdy_resource -a type={}
    - all           该网站所有电影
    - new           该网站最新电影

    """
    name = 'btbtdy_resource'
    # start_url存放容器改为redis list
    redis_key = 'btbtdy_resource:start_urls'
    allowed_domains = ['www.btbtdy.me']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.resource.ResourcePipeline': 300
        }
    }

    def __init__(self, type=None, **kwargs):
        super().__init__(**kwargs)
        self.type = type
        self.type_new = 'new'
        # 仅爬取最新电影的页数
        self.new_max_pages = 50

    def start_requests(self):
        yield scrapy.Request(url='{}/screen/0-----time-1.html'.format(config.URL_BTBTDY),
                             meta={'page_id': 1}, callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        page_id = response.meta['page_id']
        # 电影列表
        movie_list = response.xpath('//div[@class="cts_ms"]')
        if movie_list:
            for movie in movie_list:
                url = movie.xpath('p[@class="title"]/a/@href').get()
                title = movie.xpath('p[@class="title"]/a/@title').get()
                year_text = movie.xpath('p[@class="des"]/text()').get()
                year = re.search('\d+', year_text).group() if year_text is not None else 0000
                if url is not None:
                    movie_id = re.search('\d+', url).group()
                    yield scrapy.Request(url='{}/vidlist/{}.html'.format(config.URL_BTBTDY, movie_id),
                                         meta={'movie_id': movie_id, 'title': title, 'year': year},
                                         callback=self.parse_movie)
            self.logger.info(
                'get btbtdy\'s movie list success,page:{}'.format(page_id))
            # 仅最新电影
            if self.type == self.type_new and page_id > self.new_max_pages:
                return
            # 下一页
            yield scrapy.Request(url='{}/screen/0-----time-{}.html'.format(config.URL_LOLDYTT, page_id + 1),
                                 meta={'page_id': page_id + 1},
                                 callback=self.parse_movie_list)
        else:
            self.logger.warning(
                'get btbtdy\'s movie list failed,page:{}'.format(page_id))

    def parse_movie(self, response):
        movie_id = response.meta['movie_id']
        title = response.meta['title']
        year = response.meta['year']
        type_list = response.xpath('//div[@class="p_list"]')
        if type_list is not None:
            for type in type_list:
                type_title = type.xpath('h2/text()').get()
                type_id = config.parse_type(type_title) if type_title is not None else 100
                for resource in type.xpath('.//li'):
                    # 在线资源
                    if type_id == 101:
                        name_origin = resource.xpath('a/text()').get()
                        url = '{}{}'.format(config.URL_BTBTDY, resource.xpath('a/@href').get())
                    # 网盘资源
                    elif type_id == 102:
                        name_origin = resource.xpath('span/text()').get()
                        url = resource.xpath('a/@href').get()
                    # 其他资源
                    else:
                        name_origin = resource.xpath('a/text()').get()
                        url = resource.xpath('span/a/@href').get()
                    item_resource = ResourceMovie()
                    item_resource['id_movie_douban'] = 0
                    item_resource['id_movie_imdb'] = 0
                    item_resource['id_website_resource'] = 103
                    item_resource['id_type_resource'] = config.parse_type(name_origin) if type_id == 100 else type_id
                    item_resource['name_zh'] = title
                    item_resource['create_year'] = year
                    item_resource['name_origin'] = name_origin if name_origin is not None else ''
                    item_resource['url_resource'] = url if url is not None else ''
                    yield item_resource
                    print('-------------------------')
                    print(item_resource)
            self.logger.info('get btbtdy\'s movie success,movie_id:{},movie_name:{}'.format(movie_id, title))
        else:
            self.logger.info('get btbtdy\'s movie failed,movie_id:{},movie_name:{}'.format(movie_id, title))
