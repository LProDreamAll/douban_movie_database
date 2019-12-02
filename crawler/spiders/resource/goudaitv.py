# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import datetime
import re
import scrapy
from crawler.configs import resource as config
from crawler.spiders.base import BaseSpider

from crawler.items.resource import ResourceMovie


class GoudaitvResourceSpider(BaseSpider):
    """
    狗带TV资源相关

    用法:
    scrapy crawl goudaitv_resource -a type={}
    - all           该网站所有电影
    - new           该网站最新电影

    """
    name = 'goudaitv_resource'
    # start_url存放容器改为redis list
    redis_key = 'goudaitv_resource:start_urls'
    allowed_domains = ['www.goudaitv.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.resource.ResourcePipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_new = 'new'
        self.start_year = datetime.datetime.now().year
        self.end_year = 1989
        # 仅最新电影,每种类型年份限制
        self.new_min_year = self.start_year - 2
        # 仅最新电影,每种类型每种年份页数限制
        self.new_max_page = 10
        # 仅爬取最新电影年份 (每种类型)
        self.new_max_pages = 100

    def start_requests(self):
        for type in (1, 2, 42, 44):
            yield scrapy.Request(
                url='{}/vodshow/{}--------{}---{}.html'.format(config.URL_GOUDAITV, type, 1, self.start_year),
                meta={'type': type, 'page_id': 1, 'year': self.start_year}, callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        type = response.meta['type']
        page_id = response.meta['page_id']
        year = response.meta['year']
        # 电影列表
        movie_list = response.xpath('//li[@class="fed-list-item fed-padding fed-col-xs4 fed-col-sm3 fed-col-md2"]')
        if movie_list:
            for movie in movie_list:
                url = movie.xpath(
                    'a[@class="fed-list-title fed-font-xiv fed-text-center fed-text-sm-left fed-visible fed-part-eone"]/@href').get()
                movie_id = re.search('\d+', url).group()
                name = movie.xpath(
                    'a[@class="fed-list-title fed-font-xiv fed-text-center fed-text-sm-left fed-visible fed-part-eone"]/text()').get()
                item_resource = ResourceMovie()
                item_resource['id_movie_douban'] = 0
                item_resource['id_movie_imdb'] = 0
                item_resource['id_website_resource'] = 106
                item_resource['id_type_resource'] = 101
                item_resource['name_zh'] = name
                item_resource['create_year'] = year
                item_resource['name_origin'] = movie.xpath(
                    'a/span[@class="fed-list-remarks fed-font-xii fed-text-white fed-text-center"]/text()').get()
                item_resource['url_resource'] = 'g_{}'.format(movie_id)
                yield item_resource
                # print('-------------------------')
                # print(item_resource)
            self.logger.info(
                'get goudaitv\'s movie list success,type:{},page:{},year:{}'.format(type, page_id, year))
            # 仅最新电影
            if self.type == self.type_new and page_id > self.new_max_pages:
                return
            # 下一页
            next_page = response.xpath('//a[@class="fed-btns-info fed-rims-info" and text()="下页"]/@href').get()
            if next_page is not None:
                next_year = year
                next_page = page_id + 1
            else:
                next_year = year - 1
                next_page = 1
            yield scrapy.Request(
                url='{}/vodshow/{}--------{}---{}.html'.format(config.URL_GOUDAITV, type, next_page, next_year),
                meta={'type': type, 'page_id': next_page, 'year': next_year},
                callback=self.parse_movie_list)
        else:
            self.logger.error(
                'get goudaitv\'s movie list failed,type:{},page:{},year:{}'.format(type, page_id, year))
