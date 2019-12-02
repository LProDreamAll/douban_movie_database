# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
from urllib.parse import quote
from crawler.configs import default
from crawler.configs import zhihu as config
from crawler.spiders.base import BaseSpider

from crawler.items.zhihu import MovieZhihu
from crawler.items.zhihu import QuestionZhihu


class MovieZhihuSpider(BaseSpider):
    """
    知乎电影相关

    """
    name = 'movie_zhihu'
    # start_url存放容器改为redis list
    redis_key = 'movie_zhihu:start_urls'
    allowed_domains = ['www.zhihu.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.zhihu.ZhihuPipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open(config.PATH_ZHIHU_COOKIE, mode='a+', encoding='utf-8') as f:
            self.zhihu_cookie = f.readlines()

    def start_requests(self):
        self.cursor.execute(
            "select movie_douban.id,movie_douban.name_zh from movie_douban "
            "left join movie_zhihu "
            "on movie_douban.id=movie_zhihu.id_movie_douban "
            "where movie_zhihu.id_movie_douban is null "
            "and have_seen>={} "
            "order by have_seen desc "
            "limit {}".format(config.HAVE_SEEN_LIMIT, default.SELECT_LIMIT))
        for id, name_zh in self.cursor.fetchall():
            yield scrapy.Request(url="{}{}".format(config.URL_SEARCH, name_zh),
                                 meta={'movie_id': id, 'movie_name': name_zh},
                                 callback=self.parse,
                                 headers={
                                     ':authority': 'www.zhihu.com',
                                     ':method': 'GET',
                                     ':path': '/search?type=content&q=' + quote(name_zh),
                                     ':sheme': 'https',
                                     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                                     # 'accept-encoding': 'gzip, deflate, br',
                                     'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
                                     'cache-control': 'max-age=0',
                                     'cookie': self.zhihu_cookie,
                                     'dnt': 1,
                                     'referer': 'https://www.zhihu.com/',
                                     'upgrade-insecure-requests': 1,
                                     'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
                                 }
                                 )

    def parse(self, response):
        movie_id = response.meta['movie_id']
        movie_name = response.meta['movie_name']
        if response.xpath('//div[@id="SearchMain"]'):
            topic = response.xpath('//div[@class="WikiBox"]')
            if topic:
                url = topic.xpath('.//h2/a/@href').get()
                id_movie_zhihu = re.search('\d+', url).group()
                vote_xp = ''.join(
                    topic.xpath('.//div[@class="WikiBoxReview-SubText WikiBoxReview-RecommendText"]/text()').getall())
                flag = topic.xpath('.//div[@class="WikiBoxReview-Text"]/text()').get()
                if flag and '知乎评分' in flag:
                    score = topic.xpath('.//span[@class="WikiBoxReview-ScoreText"]/text()').get()
                    vote = re.search('\d+', vote_xp).group()
                else:
                    score = 0.0
                    vote = 0
                maoyan_score = 0.0
                maoyan_list = topic.xpath('.//div[@class="WikiBoxHeader-Meta"]')
                for maoyan in maoyan_list:
                    key = maoyan.xpath('span[@class="WikiBoxHeader-MetaKey"]/text()').get()
                    if '评分' in key:
                        values = ''.join(maoyan.xpath('span[@class="WikiBoxHeader-MetaValue"]/text()').getall())
                        if '猫眼' in values:
                            maoyan_score = re.search('\d\.\d', values).group()
                        break
                # 电影话题
                item_movie = MovieZhihu()
                item_movie['id'] = id_movie_zhihu
                item_movie['id_movie_douban'] = movie_id
                item_movie['name_zh'] = topic.xpath('.//h2/a/text()').get()
                item_movie['zhihu_score'] = score
                item_movie['zhihu_vote'] = vote
                item_movie['maoyan_score'] = maoyan_score
                yield item_movie
                # print('topic ---------------')
                # print(item_movie)
                # 影片评价、评论
                essence_list = response.xpath('//li[@class="WikiBoxEssenceContent-ItemWrapper"]')
                if essence_list:
                    for essence in essence_list:
                        url = essence.xpath('a/@href').get()
                        question_id_re = re.search('\d+', url) if url is not None else ''
                        answer = essence.xpath('span/text()').get()
                        answer_re = re.search('\d+', answer) if answer is not None else ''
                        item_question = QuestionZhihu()
                        item_question['id'] = question_id_re.group() if question_id_re != '' else 0
                        item_question['id_movie_zhihu'] = id_movie_zhihu
                        item_question['name_zh'] = essence.xpath('a').xpath('string(.)').get()
                        item_question['answer_num'] = answer_re.group() if answer_re != '' else 0
                        yield item_question
                        # print('essence -----------')
                        # print(item_question)
                # 文章 / 问题
                article_list = response.xpath('//div[@class="ContentItem ArticleItem"]')
                question_list = response.xpath('//div[@class="ContentItem AnswerItem"]')
                for index, question in enumerate(article_list + question_list):
                    url = question.xpath('.//a/@href').get()
                    question_id_re = re.search('\d+', url) if url is not None else ''
                    item_question = QuestionZhihu()
                    item_question['id'] = question_id_re.group() if question_id_re != '' else 0
                    item_question['id_movie_zhihu'] = id_movie_zhihu
                    item_question['name_zh'] = question.xpath('.//a/span').xpath('string(.)').get()
                    # 文章
                    if index < len(article_list):
                        item_question['answer_num'] = 1
                    # 问题
                    else:
                        item_question['answer_num'] = 0
                    yield item_question
                    # print('article or question -----------')
                    # print(item_question)
                self.logger.info('get zhihu search success,movie_id:{},movie_name:{}'.format(movie_id, movie_name))
            else:
                item_movie = MovieZhihu()
                item_movie['id'] = 0
                item_movie['id_movie_douban'] = movie_id
                item_movie['name_zh'] = ''
                item_movie['zhihu_score'] = 0.0
                item_movie['zhihu_vote'] = 0
                item_movie['maoyan_score'] = 0.0
                yield item_movie
                self.logger.warning('get zhihu search None,movie_id:{},movie_name:{}'.format(movie_id, movie_name))
        else:
            self.logger.error('get zhihu search failed,movie_id:{},movie_name:{}'.format(movie_id, movie_name))
