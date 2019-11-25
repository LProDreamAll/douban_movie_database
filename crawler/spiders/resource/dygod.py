# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
from crawler.configs import resource as config
from crawler.spiders.base import BaseSpider

from crawler.items.resource import ResourceMovie


class DygodResourceSpider(BaseSpider):
    """
    电影天堂资源相关

    """
    name = 'dygod_resource'
    # start_url存放容器改为redis list
    redis_key = 'dygod_resource:start_urls'
    allowed_domains = ['www.dy2018.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.resource.ResourcePipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        yield scrapy.Request(url='{}/{}/'.format(config.URL_DYGOD, 0),
                             meta={'type_id': 0, 'page_id': 1}, callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        type_id = response.meta['type_id']
        page_id = response.meta['page_id']
        # 爬虫结束
        if type_id > 20:
            self.crawler.engine.close_spider(self, 'get dygod resource finished')
        # 电影列表
        movie_list = response.xpath('//a[@class="ulink" and @title]/@href').getall()
        if movie_list:
            for movie in movie_list:
                yield scrapy.Request(url='{}{}'.format(config.URL_DYGOD, movie),
                                     meta={'movie_id': re.search('\d+', movie).group()},
                                     callback=self.parse_movie)
            self.logger.info('get dygod\'s movie list success,type:{},page:{}'.format(type_id, page_id))
        else:
            self.logger.warning('get dygod\'s movie list failed,type:{},page:{}'.format(type_id, page_id))
        # 下一页
        next_page = response.xpath('//div[@class="x"]//a[text()="下一页"]/@href').get()
        if next_page is None:
            next_page = '/{}'.format(type_id + 1)
            next_type_id = type_id + 1
            next_page_id = 1
        else:
            next_type_id = type_id
            next_page_id = page_id + 1
        yield scrapy.Request(url='{}{}'.format(config.URL_DYGOD, next_page),
                             meta={'type_id': next_type_id, 'page_id': next_page_id},
                             callback=self.parse_movie_list)

    def parse_movie(self, response):
        movie_id = response.meta['movie_id']
        title = response.xpath('//h1/text()').get()
        name = re.search('《(.*)》', title).group(1) if title is not None else None
        if title is not None:
            online_list = response.xpath('//div[@class="player_list"]//a/@href').getall()
            offline_list = response.xpath('//td[@style]/a/@href').getall()
            for url in online_list + offline_list:
                item_resource = ResourceMovie()
                item_resource['id_movie_douban'] = 0
                item_resource['id_movie_imdb'] = 0
                item_resource['id_website_resource'] = 101
                item_resource['id_type_resource'] = 101 if config.URL_DYGOD in url else 100
                item_resource['name_zh'] = name
                year_maybe = response.xpath('//div[@id="Zoom"]/text()').getall()
                for index, year in enumerate(year_maybe):
                    if index > 5:
                        break
                    create_year = re.search('年　　代　(\d+)', year)
                    if create_year is not None:
                        item_resource['create_year'] = create_year.group(1)
                        break
                item_resource['name_origin'] = title
                item_resource['url_resource'] = url
                yield item_resource
                print('-------------------------')
                print(item_resource)
            self.logger.info('get dydod\'s movie success,movie_id:{},movie_name:{}'.format(movie_id, name))
        else:
            self.logger.warning('get dydod\'s movie failed,movie_id:{}'.format(movie_id))
