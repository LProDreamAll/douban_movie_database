# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import re
import scrapy
from crawler.configs import douban as config
from crawler.spiders.base import BaseSpider

from crawler.items.douban import TrailerMovieDouban


class TrailerDoubanSpider(BaseSpider):
    """
    豆瓣预告片相关

    """
    name = 'trailer_douban'
    # start_url存放容器改为redis list
    redis_key = 'trailer_douban:start_urls'
    allowed_domains = ['movie.douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.douban_movie.trailer.TrailerDoubanPipeline': 300
        }
    }

    def prepare(self, offset, limit):
        """
        获取请求列表

        :param offset:
        :param limit:
        :return:
        """
        self.cursor.execute("select id from trailer_movie_douban where url_video='' limit {},{}".format(offset, limit))
        for id, in self.cursor.fetchall():
            yield scrapy.Request(url="{}{}/".format(config.URL_TRAILER_MOVIE, id),
                                 cookies=config.get_cookie_douban(),
                                 meta={'id': id}, callback=self.parse)
        self.logger.info('get douban trailer\'s request list success,offset:{},limit:{}'.format(offset, limit))

    def parse(self, response):
        trailer_id = response.meta['id']
        if response.xpath('//div[@id="content"]'):
            item_trailer = TrailerMovieDouban()
            item_trailer['id'] = trailer_id
            item_trailer['id_movie_douban'] = re.search('\d+', response.xpath('//h1/a/@href').get()).group()
            trailer_url = json.loads(response.xpath('//script[@type="application/ld+json"]/text()').get())
            item_trailer['url_video'] = trailer_url['embedUrl']
            yield item_trailer
            print('---------------------')
            print(item_trailer)
            self.logger.info('get douban trailer success,trailer_id:{}'.format(trailer_id))
        else:
            self.logger.warning('get douban trailer failed,trailer_id:{}'.format(trailer_id))
        # 获取新的请求列表
        self.count += 1
        if self.count % self.limit == 0:
            for request in self.prepare(self.count, self.limit):
                yield request
