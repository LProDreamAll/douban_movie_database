# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy

"""
豆瓣相关

"""


# 电影相关

class MovieDouban(scrapy.Item):
    id = scrapy.Field()
    id_type_video = scrapy.Field()
    id_movie_imdb = scrapy.Field()
    start_year = scrapy.Field()
    name_zh = scrapy.Field()
    name_origin = scrapy.Field()
    runtime = scrapy.Field()
    url_poster = scrapy.Field()
    summary = scrapy.Field()
    have_seen = scrapy.Field()
    wanna_seen = scrapy.Field()
    is_updated = scrapy.Field()


class AliasMovieDouban(scrapy.Item):
    id_movie_douban = scrapy.Field()
    name_alias = scrapy.Field()


class MovieDoubanToCelebrityDouban(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_celebrity_douban = scrapy.Field()
    id_profession = scrapy.Field()
    sort = scrapy.Field()


class MovieDoubanToTypeMovie(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_type_movie = scrapy.Field()


class RateMovieDouban(scrapy.Item):
    id = scrapy.Field()
    score = scrapy.Field()
    vote = scrapy.Field()
    score1 = scrapy.Field()
    score2 = scrapy.Field()
    score3 = scrapy.Field()
    score4 = scrapy.Field()
    score5 = scrapy.Field()


class MovieDoubanToAwardMovie(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_award_movie = scrapy.Field()
    id_celebrity_douban = scrapy.Field()
    type_award = scrapy.Field()
    award_th = scrapy.Field()
    is_nominated = scrapy.Field()


class TagMovie(scrapy.Item):
    id_movie_douban = scrapy.Field()
    name_zh = scrapy.Field()


class AwardMovie(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()


class ImageMovieDouban(scrapy.Item):
    id = scrapy.Field()
    id_movie_douban = scrapy.Field()
    sort = scrapy.Field()
    length = scrapy.Field()
    width = scrapy.Field()


class TrailerMovieDouban(scrapy.Item):
    id = scrapy.Field()
    id_movie_douban = scrapy.Field()
    url_video = scrapy.Field()


# 影人相关

class CelebrityDouban(scrapy.Item):
    id = scrapy.Field()
    id_celebrity_imdb = scrapy.Field()
    name_zh = scrapy.Field()
    name_origin = scrapy.Field()
    sex = scrapy.Field()
    birth_date = scrapy.Field()
    url_portrait = scrapy.Field()
    summary = scrapy.Field()
    is_updated = scrapy.Field()


class AliasCelebrityDouban(scrapy.Item):
    id_celebrity_douban = scrapy.Field()
    name_alias = scrapy.Field()
    is_nikename = scrapy.Field()


class ImageCelebrityDouban(scrapy.Item):
    id = scrapy.Field()
    id_celebrity_douban = scrapy.Field()
    sort = scrapy.Field()
    length = scrapy.Field()
    width = scrapy.Field()


class ResourceMovie(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_website_resource = scrapy.Field()
    id_type_resource = scrapy.Field()
    url_resource = scrapy.Field()
    name_zh = scrapy.Field()


# 评论相关

class CommentMovieDouban(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_user_douban = scrapy.Field()
    agree_vote = scrapy.Field()
    create_date = scrapy.Field()
    content = scrapy.Field()


class UserDouban(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()
