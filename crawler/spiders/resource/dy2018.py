# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
from crawler.configs import resource as config
from crawler.spiders.base import BaseSpider

from crawler.items.resource import ResourceMovie


class Dy2018ResourceSpider(BaseSpider):
    """
    电影天堂资源相关

    用法:
    scrapy crawl dy2018_resource -a type={}
    - all           该网站所有电影
    - new           该网站最新电影

    """
    name = 'dy2018_resource'
    # start_url存放容器改为redis list
    redis_key = 'dy2018_resource:start_urls'
    allowed_domains = ['www.dy2018.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.resource.ResourcePipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_new = 'new'
        # 仅爬取最新电影的页数 (每种类型)
        self.new_max_pages = 5

    def start_requests(self):
        for type_id in range(0, 20, 1):
            yield scrapy.Request(url='{}/{}/'.format(config.URL_DY2018, type_id),
                                 meta={'type_id': type_id, 'page_id': 1}, callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        type_id = response.meta['type_id']
        page_id = response.meta['page_id']
        # 电影列表
        movie_list = response.xpath('//a[@class="ulink" and @title]/@href').getall()
        if movie_list:
            for movie in movie_list:
                yield scrapy.Request(url='{}{}'.format(config.URL_DY2018, movie),
                                     meta={'movie_id': re.search('\d+', movie).group()},
                                     priority=2, callback=self.parse_movie)
            self.logger.info('get dy2018 movie list success,type:{},page:{}'.format(type_id, page_id))
            # 仅最新电影
            if self.type == self.type_new and page_id > self.new_max_pages:
                return
            # 下一页
            yield scrapy.Request(url='{}/{}/index_{}.html'.format(config.URL_DY2018, type_id, page_id + 1),
                                 meta={'type_id': type_id, 'page_id': page_id + 1}, priority=1,
                                 callback=self.parse_movie_list)
        else:
            self.logger.error('get dy2018 movie list failed,type:{},page:{}'.format(type_id, page_id))

    def parse_movie(self, response):
        movie_id = response.meta['movie_id']
        title = response.xpath('//h1/text()').get()
        if title:
            name = re.search('《(.*)》', title).group(1) if title is not None else ''
            online_list = response.xpath('//div[@class="player_list"]//a/@href').getall()
            offline_list = response.xpath('//td[@style]/a/@href').getall()
            for url in online_list + offline_list:
                item_resource = ResourceMovie()
                item_resource['id_movie_douban'] = 0
                item_resource['id_movie_imdb'] = 0
                item_resource['id_website_resource'] = 101
                item_resource['id_type_resource'] = 101 if config.URL_DY2018 in url else 100
                item_resource['name_zh'] = name
                create_year = 0
                year_xp = response.xpath('//div[@id="Zoom"]/text()').getall()
                for index, year in enumerate(year_xp):
                    if index > 5:
                        break
                    year_re = re.search('年　　代　(\d+)', year)
                    if year_re is not None:
                        create_year = year_re.group(1)
                        break
                item_resource['create_year'] = create_year
                item_resource['name_origin'] = title
                item_resource['url_resource'] = url
                if item_resource['id_type_resource'] == 101:
                    item_resource['url_resource'] = 't_{}'.format(
                        re.search('id=https://(.*)/index\.m3u8', url).group(1))
                yield item_resource
                # print('-------------------------')
                # print(item_resource)
            self.logger.info('get dy2018 movie success,movie_id:{},movie_name:{}'.format(movie_id, name))
        else:
            self.logger.error('get dy2018 movie failed,movie_id:{}'.format(movie_id))
