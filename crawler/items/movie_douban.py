# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy

"""
豆瓣电影相关

"""


class MovieDouban(scrapy.Item):
    id = scrapy.Field()
    id_type_video = scrapy.Field()
    id_movie_imdb = scrapy.Field()
    start_year = scrapy.Field()
    name_zh = scrapy.Field()
    name_origin = scrapy.Field()
    runtime = scrapy.Field()
    url_poster = scrapy.Field()


class AliasMovieDouban(scrapy.Item):
    id_movie_douban = scrapy.Field()
    name_alias = scrapy.Field()


class MovieDoubanToCelebrityDouban(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_celebrity_douban = scrapy.Field()
    id_profession = scrapy.Field()
    sort = scrapy.Field()


class RateMovieDouban(scrapy.Item):
    id = scrapy.Field()
    score = scrapy.Field()
    vote = scrapy.Field()
    score1 = scrapy.Field()
    score2 = scrapy.Field()
    score3 = scrapy.Field()
    score4 = scrapy.Field()
    score5 = scrapy.Field()


class CommentMovieDouban(scrapy.Item):
    id = scrapy.Field()
    agree_vote = scrapy.Field()
    create_date = scrapy.Field()
    content = scrapy.Field()


class ReviewMovieDouban(scrapy.Item):
    id = scrapy.Field()
    agree_vote = scrapy.Field()
    create_date = scrapy.Field()
    content = scrapy.Field()


class MovieDoubanToTypeMovie(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_type_movie = scrapy.Field()


class MovieDoubanToTagMovie(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_tag_movie = scrapy.Field()


class MovieDoubanToAwardMovie(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_award_movie = scrapy.Field()
    id_type_award = scrapy.Field()
    id_celebrity_douban = scrapy.Field()
    award_th = scrapy.Field()
    gain_year = scrapy.Field()


class MovieDoubanToAreaDouban(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_area_douban = scrapy.Field()
    show_date = scrapy.Field()


class MovieDoubanToAreaDouban(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_area_douban = scrapy.Field()
    show_date = scrapy.Field()


class MovieDoubanToCommentMovieDouban(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_comment_movie_douban = scrapy.Field()


class MovieDoubanToReviewMovieDouban(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_review_movie_douban = scrapy.Field()


# 影人相关

class CelebrityDouban(scrapy.Item):
    id = scrapy.Field()
    id_celebrity_imdb = scrapy.Field()
    id_country_imdb = scrapy.Field()
    id_state_imdb = scrapy.Field()
    id_city_imdb = scrapy.Field()
    name_zh = scrapy.Field()
    name_en = scrapy.Field()
    name_other = scrapy.Field()
    name_zh_more = scrapy.Field()
    name_en_more = scrapy.Field()
    name_other_more = scrapy.Field()
    sex = scrapy.Field()
    birth_date = scrapy.Field()
    description = scrapy.Field()
    url_portrait = scrapy.Field()


class CelebrityDoubanToProfession(scrapy.Item):
    id_celebrity_douban = scrapy.Field()
    id_profession = scrapy.Field()
