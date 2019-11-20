# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
from crawler.tools.database_pool import database_pool
from crawler.configs import douban as config
from scrapy_redis.spiders import RedisSpider

from crawler.items.douban import CommentMovieDouban
from crawler.items.douban import UserDouban


class CommentDoubanSpider(RedisSpider):
    """
    豆瓣影人相关

    """
    name = 'comment_douban'
    # start_url存放容器改为redis list
    redis_key = 'comment_douban:start_urls'
    allowed_domains = ['movie.douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.douban_movie.comment.CommentDoubanPipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()

    def start_requests(self):
        self.cursor.execute('select movie_douban.id from movie_douban '
                            'left join comment_movie_douban '
                            'on movie_douban.id=comment_movie_douban.id_movie_douban '
                            'where comment_movie_douban.id_movie_douban is null')
        for id, in self.cursor.fetchall():
            yield scrapy.Request(url="{}{}{}".format(config.URL_COMMENT_MOVIE_START, id, config.URL_COMMENT_MOVIE_END),
                                 cookies=config.get_cookie_douban(),
                                 meta={'id': id}, callback=self.parse)

    def parse(self, response):
        movie_id = response.meta['id']
        if response.xpath('//div[@id="content"]'):
            comment_list = response.xpath('//div[@class="comment-item"]')
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
