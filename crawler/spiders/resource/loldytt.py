# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
from crawler.configs import resource as config
from crawler.spiders.base import BaseSpider

from crawler.items.resource import ResourceMovie


class LoldyttResourceSpider(BaseSpider):
    """
    LOL电影天堂资源相关

    """
    name = 'loldytt_resource'
    # start_url存放容器改为redis list
    redis_key = 'loldytt_resource:start_urls'
    allowed_domains = ['www.loldytt.tv']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.resource.ResourcePipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.type_sum = len(config.LOLDYTT_TYPE_LIST)

    def start_requests(self):
        yield scrapy.Request(url='{}/{}/chart/1.html'.format(config.URL_LOLDYTT, config.LOLDYTT_TYPE_LIST[0]),
                             meta={'type_id': 0, 'page_id': 1}, callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        type_id = response.meta['type_id']
        page_id = response.meta['page_id']
        # 爬虫结束
        if type_id >= self.type_sum:
            self.crawler.engine.close_spider(self, 'get loldytt resource finished')
        # 电影列表
        movie_list = response.xpath('//div[@class="box3"]//a[@title]/@href').getall()
        if movie_list:
            for movie in movie_list:
                yield scrapy.Request(url=movie,
                                     meta={'movie_id': movie.split('/')[4]},
                                     callback=self.parse_movie)
            self.logger.info(
                'get loldytt\'s movie list success,type:{},page:{}'.format(config.LOLDYTT_TYPE_LIST[type_id], page_id))
        else:
            self.logger.warning(
                'get loldytt\'s movie list failed,type:{},page:{}'.format(config.LOLDYTT_TYPE_LIST[type_id], page_id))
        # 下一页
        next_page = response.xpath('//div[@class="pagebox"]/a[text()="下一页"]/@href').get()
        if next_page is None:
            next_page = '/{}/chart/1.html'.format(config.LOLDYTT_TYPE_LIST[type_id + 1])
            next_type_id = type_id + 1
            next_page_id = 1
        else:
            next_type_id = type_id
            next_page_id = page_id + 1
        yield scrapy.Request(url='{}{}'.format(config.URL_LOLDYTT, next_page),
                             meta={'type_id': next_type_id, 'page_id': next_page_id},
                             callback=self.parse_movie_list)

    def parse_movie(self, response):
        movie_id = response.meta['movie_id']
        title = response.xpath('//h1/a/text()').get()
        if title is not None:
            resource_list = response.xpath('//div[@id="liebiao"]//a[@title]')
            for resource in resource_list:
                url = resource.xpath('@href').get()
                name_origin = resource.xpath('text()').get()
                description = response.xpath('//*[@id="juqing"]//text()').getall()
                flag_year = False
                flag_imdb = False
                create_year = None
                imdb_id = 0
                for detail in description:
                    if flag_year and flag_imdb:
                        break
                    year = re.search('(\d{4})-\d{2}-\d{2}', detail)
                    imdb = re.search('IMDb链接: tt(\d+)', detail)
                    if year is not None:
                        create_year = year.group(1)
                        flag_year = True
                    if imdb is not None:
                        imdb_id = imdb.group(1)
                        flag_imdb = True
                item_resource = ResourceMovie()
                item_resource['id_movie_douban'] = 0
                item_resource['id_movie_imdb'] = imdb_id
                item_resource['id_website_resource'] = 102
                item_resource['id_type_resource'] = config.parse_type(name_origin)
                item_resource['name_zh'] = title
                item_resource['create_year'] = create_year
                item_resource['name_origin'] = name_origin
                item_resource['url_resource'] = url
                yield item_resource
                print('-------------------------')
                print(item_resource)
            self.logger.info('get loldytt\'s movie success,movie_id:{},movie_name:{}'.format(movie_id, title))
        else:
            self.logger.warning('get loldytt\'s movie failed,movie_id:{}'.format(movie_id))
