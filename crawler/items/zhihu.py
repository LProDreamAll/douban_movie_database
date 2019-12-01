# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy


class MovieZhihu(scrapy.Item):
    id = scrapy.Field()
    id_movie_douban = scrapy.Field()
    name_zh = scrapy.Field()
    zhihu_score = scrapy.Field()
    zhihu_vote = scrapy.Field()
    maoyan_score = scrapy.Field()


class QuestionZhihu(scrapy.Item):
    id = scrapy.Field()
    id_movie_zhihu = scrapy.Field()
    name_zh = scrapy.Field()
    answer_num = scrapy.Field()
