# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import scrapy
from crawler.configs import douban as config
from crawler.spiders.base import BaseSpider

from crawler.items.new import MovieDouban


class NewDoubanSpider(BaseSpider):
    """
    豆瓣最新上映相关

    """
    name = 'new_douban'
    # start_url存放容器改为redis list
    redis_key = 'new_douban:start_urls'
    allowed_domains = ['movie.douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.douban_movie.new.NewDoubanPipeline': 300
        }
    }

    def start_requests(self):
        for num in range(0, config.NEW_MOVIE_MAX, 15):
            yield scrapy.Request(url="{}{}".format(config.URL_MOVIE_NEW, num),
                                 cookies=config.get_cookie_douban(),
                                 meta={'num': num}, callback=self.parse)

    def parse(self, response):
        num = response.meta['num']
        content = json.loads(response.text)
        if 'data' in content:
            for movie in content['data']:
                item_movie = MovieDouban()
                item_movie['id'] = movie['id']
                item_movie['name_zh'] = movie['title']
                yield item_movie
                # print('--------------')
                # print(item_movie)
            self.logger.info('get douban new success,now_num:{}'.format(num))
        else:
            self.logger.warning('get douban new failed,now_num:{}'.format(num))
