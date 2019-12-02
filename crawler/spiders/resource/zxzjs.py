# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
import datetime
from crawler.configs import resource as config
from crawler.spiders.base import BaseSpider

from crawler.items.resource import ResourceMovie


class ZxzjsResourceSpider(BaseSpider):
    """
    在线之家资源相关

    用法:
    scrapy crawl zxzjs_resource -a type={}
    - all           该网站所有电影
    - new           该网站最新电影

    """
    name = 'zxzjs_resource'
    # start_url存放容器改为redis list
    redis_key = 'zxzjs_resource:start_urls'
    allowed_domains = ['www.zxzjs.com']
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

    def start_requests(self):
        for type in range(1, 6, 1):
            yield scrapy.Request(
                url='{}/vodshow/{}-----------{}.html'.format(config.URL_ZXZJS, type, self.start_year),
                meta={'type_id': type, 'page_id': 1, 'year': self.start_year}, callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        type_id = response.meta['type_id']
        page_id = response.meta['page_id']
        year = response.meta['year']
        # 电影列表
        movie_list = response.xpath('//ul[@class="stui-vodlist clearfix"]/li/div[@class="stui-vodlist__box"]/a')
        if movie_list:
            for movie in movie_list:
                url_xp = movie.xpath('@href').get()
                url_re = re.search('video/(.*)-1-1\.html', url_xp) if url_xp is not None else ''
                name = movie.xpath('@title').get()

                item_resource = ResourceMovie()
                item_resource['id_movie_douban'] = 0
                item_resource['id_movie_imdb'] = 0
                item_resource['id_website_resource'] = 107
                item_resource['id_type_resource'] = 101
                item_resource['name_zh'] = name
                item_resource['create_year'] = year
                item_resource['name_origin'] = ''
                item_resource['url_resource'] = 'z_{}'.format(url_re.group(1)) if url_re != '' else ''
                yield item_resource
                # print('-------------------------')
                # print(item_resource)
            self.logger.info(
                'get zxzjs\'s movie list success,type:{},page:{},year:{}'.format(type_id, page_id, year))
            # 爬虫结束 / 仅最新电影
            if year < self.end_year or (
                    self.type == self.type_new and year < self.new_min_year and page_id > self.new_max_page):
                return
            # 下一页
            next_page = response.xpath('//a[text()="下一页"]/@href').get()
            next_year = re.search('--------(\d{1})---', next_page).group(1)
            if int(next_year) == year:
                next_page_id = page_id + 1
                next_year_id = self.start_year
            else:
                next_year_id = year - 1
                next_page = '/vodshow/{}-----------{}.html'.format(type_id, year)
                next_page_id = 1
            yield scrapy.Request(url='{}{}'.format(config.URL_ZXZJS, next_page),
                                 meta={'type_id': type_id, 'page_id': next_page_id, 'year': next_year_id},
                                 callback=self.parse_movie_list)
        else:
            self.logger.error(
                'get zxzjs\'s movie list failed,type:{},page:{},year:{}'.format(type_id, page_id, year))
