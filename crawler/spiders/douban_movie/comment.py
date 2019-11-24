# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
from crawler.configs import douban as config
from crawler.spiders.base import BaseSpider

from crawler.items.douban import CommentMovieDouban
from crawler.items.douban import UserDouban


class CommentDoubanSpider(BaseSpider):
    """
    豆瓣影人相关

    """
    name = 'comment_douban'
    # start_url存放容器改为redis list
    redis_key = 'comment_douban:start_urls'
    allowed_domains = ['movie.douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.douban_movie.douban.DoubanPipeline': 300
        }
    }

    def prepare(self, offset, limit):
        """
        获取请求列表

        :param offset:
        :param limit:
        :return:
        """
        self.cursor.execute('select movie_douban.id from movie_douban '
                            'left join comment_movie_douban '
                            'on movie_douban.id=comment_movie_douban.id_movie_douban '
                            'where comment_movie_douban.id_movie_douban is null '
                            'limit {},{}'.format(offset, limit))
        for id, in self.cursor.fetchall():
            yield scrapy.Request(url="{}{}{}".format(config.URL_COMMENT_MOVIE_START, id, config.URL_COMMENT_MOVIE_END),
                                 cookies=config.get_cookie_douban(),
                                 meta={'id': id}, callback=self.parse)
        self.logger.info('get douban comment\'s request list success,offset:{},limit:{}'.format(offset, limit))

    def parse(self, response):
        movie_id = response.meta['id']
        comment_list = response.xpath('//div[@class="comment-item"]')
        if comment_list.xpath('div'):
            for comment in comment_list:
                item_user = UserDouban()
                user_id = comment.xpath('.//span[@class="comment-info"]/a/@href').get().split('/')[4]
                item_user['id'] = user_id
                item_user['name_zh'] = comment.xpath('.//span[@class="comment-info"]/a/text()').get()
                print('--------------')
                print(item_user)
                yield item_user
                item_comment = CommentMovieDouban()
                item_comment['id_movie_douban'] = movie_id
                item_comment['id_user_douban'] = user_id
                item_comment['agree_vote'] = comment.xpath('.//span[@class="votes"]/text()').get()
                create_date = comment.xpath('.//span[@title]/text()').get()
                item_comment['create_date'] = re.search('\d{4}-\d{2}-\d{2}', create_date).group()
                item_comment['content'] = comment.xpath('.//span[@class="short"]/text()').get()
                print('-------------------------')
                print(item_comment)
                yield item_comment
            self.logger.info('get douban movie\'s comments success,id:{}'.format(movie_id))
        else:
            self.logger.warning('get douban movie\'s comments failed,id:{}'.format(movie_id))
        # 获取新的请求列表
        self.count += 1
        if self.count % self.limit == 0:
            for request in self.prepare(self.count, self.limit):
                yield request