# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
from crawler.configs import resource as config
from crawler.spiders.base import BaseSpider

from crawler.items.resource import ResourceMovie


class Xl720ResourceSpider(BaseSpider):
    """
    迅雷电影天堂资源相关

    用法:
    scrapy crawl xl720_resource -a type={}
    - all           该网站所有电影
    - new           该网站最新电影

    """
    name = 'xl720_resource'
    # start_url存放容器改为redis list
    redis_key = 'xl720_resource:start_urls'
    allowed_domains = ['www.xl720.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.resource.ResourcePipeline': 300
        }
    }

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.type_new = 'new'
        # 仅爬取最新电影的页数
        self.new_max_pages = 100

    def start_requests(self):
        yield scrapy.Request(url='{}/filter'.format(config.URL_XL720),
                             meta={'page_id': 1}, callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        page_id = response.meta['page_id']
        # 电影列表
        movie_list = response.xpath('//h3/a')
        if movie_list:
            for movie in movie_list:
                url = movie.xpath('@href').get()
                if url is not None:
                    movie_id = re.search('(\d+)\.html', url).group(1)
                    title = re.search('([\u4e00-\u9fff()\d\s]*)\s.*\((\d+)\)', movie.xpath('text()').get())
                    yield scrapy.Request(url=url,
                                         meta={'movie_id': movie_id, 'title': title.group(1), 'year': title.group(2)},
                                         callback=self.parse_movie)
            self.logger.info(
                'get xl720\'s movie list success,page:{}'.format(page_id))
            # 仅最新电影
            if self.type == self.type_new and page_id > self.new_max_pages:
                return
            # 下一页
            yield scrapy.Request(url='{}/filter/page/{}'.format(config.URL_LOLDYTT, page_id + 1),
                                 meta={'page_id': page_id + 1},
                                 callback=self.parse_movie_list)
        else:
            self.logger.warning(
                'get xl720\'s movie list failed,page:{}'.format(page_id))

    def parse_movie(self, response):
        movie_id = response.meta['movie_id']
        title = response.meta['title']
        year = response.meta['year']
        resource_list = response.xpath('//div[@class="download-link"]/a')
        if resource_list:
            imdb_id = 0
            info_list = response.xpath('//div[@id="info"]/text()').getall()
            for info in reversed(info_list):
                imdb = re.search(' IMDb链接: tt(\d+)', info)
                if imdb is not None:
                    imdb_id = imdb.group(1)
                    break
            for resource in resource_list:
                url = resource.xpath('@href').get()
                name_origin = resource.xpath('text()').get()
                item_resource = ResourceMovie()
                item_resource['id_movie_douban'] = 0
                item_resource['id_movie_imdb'] = imdb_id
                item_resource['id_website_resource'] = 104
                item_resource['id_type_resource'] = config.parse_type(name_origin)
                item_resource['name_zh'] = title
                item_resource['create_year'] = year
                item_resource['name_origin'] = name_origin
                item_resource['url_resource'] = url
                yield item_resource
                print('-------------------------')
                print(item_resource)
            self.logger.info('get xl720\'s movie success,movie_id:{},movie_name:{}'.format(movie_id, title))
        else:
            self.logger.warning('get xl720\'s movie failed,movie_id:{},movie_name:{}'.format(movie_id, title))
