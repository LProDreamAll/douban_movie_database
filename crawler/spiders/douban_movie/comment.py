# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import time
import scrapy
from crawler.configs import default
from crawler.configs import douban as config
from crawler.spiders.base import BaseSpider

from crawler.items.douban import CommentMovieDouban
from crawler.items.douban import UserDouban
from crawler.items.douban import UserDoubanToMovieDouban


class CommentDoubanSpider(BaseSpider):
    """
    豆瓣电影评论相关

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

    def start_requests(self):
        self.cursor.execute('select movie_douban.id from movie_douban '
                            'left join comment_movie_douban '
                            'on movie_douban.id=comment_movie_douban.id_movie_douban '
                            'where comment_movie_douban.id_movie_douban is null '
                            'limit {}'.format(default.SELECT_LIMIT))
        for id, in self.cursor.fetchall():
            yield scrapy.Request(url="{}{}{}".format(config.URL_COMMENT_MOVIE_START, id, config.URL_COMMENT_MOVIE_END),
                                 cookies=config.get_cookie_douban(),
                                 meta={'id': id}, callback=self.parse)

    def parse(self, response):
        movie_id = response.meta['id']
        comment_list = response.xpath('//div[@class="comment-item"]')
        if comment_list.xpath('div'):
            for comment in comment_list:
                item_user = UserDouban()
                user_id = comment.xpath('.//span[@class="comment-info"]/a/@href').get().split('/')[4]
                item_user['id'] = user_id
                item_user['name_zh'] = comment.xpath('.//span[@class="comment-info"]/a/text()').get()
                # print('--------------')
                # print(item_user)
                yield item_user

                item_comment = CommentMovieDouban()
                item_comment['id_movie_douban'] = movie_id
                item_comment['id_user_douban'] = user_id
                item_comment['agree_vote'] = comment.xpath('.//span[@class="votes"]/text()').get()
                create_date = comment.xpath('.//span[@title]/text()').get()
                create = re.search('\d{4}-\d{2}-\d{2}', create_date).group() if create_date is not None else None
                item_comment['create_date'] = int(
                    time.mktime(time.strptime(create, '%Y-%m-%d'))) if create is not None else 0
                item_comment['content'] = comment.xpath('.//span[@class="short"]/text()').get()
                # print('-------------------------')
                # print(item_comment)
                yield item_comment

                score_xp = comment.xpath('//span[@class="comment-info"]/span[2]/@class').get()
                score_re = re.search('\d+', score_xp) if score_xp is not None else 0

                item_user_movie = UserDoubanToMovieDouban()
                item_user_movie['id_user_douban'] = user_id
                item_user_movie['id_movie_douban'] = movie_id
                item_user_movie['score'] = int(score_re.group()) / 5 if score_re != 0 else 0
                item_user_movie['is_wish'] = 0
                item_user_movie['is_seen'] = 1
                yield item_user_movie
            self.logger.info('get douban movie\'s comments success,id:{}'.format(movie_id))
        else:
            self.logger.warning('get douban movie\'s comments failed,id:{}'.format(movie_id))
