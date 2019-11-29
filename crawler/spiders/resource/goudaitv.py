# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
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
    allowed_domains = ['www.goodaitv.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.resource.ResourcePipeline': 300
        }
    }

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.type_new = 'new'
        # 仅爬取最新电影的页数 (每种类型)
        self.new_max_pages = 100

    def start_requests(self):
        for type in config.GOUDAITV_TYPE_LIST:
            yield scrapy.Request(url='{}/v/{}.html'.format(config.URL_GOUDAITV, type),
                                 meta={'type': type, 'page_id': 1}, callback=self.parse_movie_list)

    def parse_movie_list(self, response):
        type = response.meta['type']
        page_id = response.meta['page_id']
        # 电影列表
        movie_list = response.xpath('//a[@class="link-hover"]')
        if movie_list:
            for movie in movie_list:
                movie_id = re.search('\d+', movie.xpath('@href').get()).group()
                name = movie.xpath('@title').get()
                create_year = 0000
                info_list = movie.xpath('span[@class="lzbz"]/p/text()').getall()
                for info in reversed(info_list):
                    year = re.search('\d{4}', info)
                    if year is not None:
                        create_year = year.group()
                        break
                item_resource = ResourceMovie()
                item_resource['id_movie_douban'] = 0
                item_resource['id_movie_imdb'] = 0
                item_resource['id_website_resource'] = 106
                item_resource['id_type_resource'] = 101
                item_resource['name_zh'] = name
                item_resource['create_year'] = create_year
                item_resource['name_origin'] = name
                item_resource['url_resource'] = '{0}/videoplayer/{1}.html?{1}-1-1'.format(config.URL_GOUDAITV, movie_id)
                yield item_resource
                print('-------------------------')
                print(item_resource)
            self.logger.info(
                'get goudaitv\'s movie list success,type:{},page:{}'.format(type, page_id))
            # 仅最新电影
            if self.type == self.type_new and page_id > self.new_max_pages:
                return
            # 下一页
            yield scrapy.Request(url='{}/v/{}-{}.html'.format(config.URL_GOUDAITV, type, page_id + 1),
                                 meta={'type': type, 'page_id': page_id + 1},
                                 callback=self.parse_movie_list)
        else:
            self.logger.warning(
                'get goudaitv\'s movie list failed,type:{},page:{}'.format(type, page_id))
