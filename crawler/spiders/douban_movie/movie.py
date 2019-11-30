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

from crawler.items.douban import MovieDouban
from crawler.items.douban import AliasMovieDouban
from crawler.items.douban import MovieDoubanToCelebrityDouban
from crawler.items.douban import MovieDoubanToTypeMovie
from crawler.items.douban import RateMovieDouban
from crawler.items.douban import TagMovie
from crawler.items.douban import AwardMovie
from crawler.items.douban import UserDouban
from crawler.items.douban import ReviewMovieDouban
from crawler.items.douban import MovieDoubanToReviewMovieDouban
from crawler.items.douban import UserDoubanToReviewMovieDouban
from crawler.items.douban import UserDoubanToMovieDouban
from crawler.items.douban import MovieDoubanToAwardMovie
from crawler.items.douban import TrailerMovieDouban
from crawler.items.resource import ResourceMovie


class MovieDoubanSpider(BaseSpider):
    """
    豆瓣电影相关

    """
    name = 'movie_douban'
    # start_url存放容器改为redis list
    redis_key = 'movie_douban:start_urls'
    allowed_domains = ['movie.douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.douban_movie.douban.DoubanPipeline': 300
        }
    }

    def start_requests(self):
        self.cursor.execute('select id from movie_douban '
                            'where update_date=0 limit {}'.format(default.SELECT_LIMIT))
        for id, in self.cursor.fetchall():
            yield scrapy.Request(url="{}{}/".format(config.URL_MOVIE, id),
                                 cookies=config.get_cookie_douban(),
                                 meta={'id': id}, callback=self.parse)

    def parse(self, response):
        movie_id = response.meta['id']
        if response.xpath('//div[@id="content"]'):
            info = response.xpath('//div[@id="info"]')
            title = response.xpath('//h1/span[1]/text()').get()
            type_list = info.xpath('span[@property="v:genre"]/text()').getall()

            imdb_xp = info.xpath('span[text()="IMDb链接:"]/following-sibling::a/text()').get()
            imdb_re = re.search('tt(\d+)', imdb_xp) if imdb_xp is not None else ''
            id_movie_imdb = imdb_re.group(1) if imdb_re != '' else 0

            year_xp = response.xpath('//h1/span[@class="year"]/text()').get()
            year_re = re.search('[(](\d+)[)]', year_xp) if year_xp is not None else ''
            start_year = year_re.group(1) if year_re != '' else 0

            name_zh_xp = re.search('[\u4e00-\u9fff()：\d\s]*', title) if title is not None else ''
            name_zh = name_zh_xp.group().strip() if name_zh_xp != '' else ''

            name_origin_xp = re.search('[\u4e00-\u9fff()\d\s]*(.*)', title) if title is not None else ''
            name_origin = name_origin_xp.group(1).strip() if name_origin_xp != '' else ''

            runtime = info.xpath('span[@property="v:runtime"]/@content').get()

            url_poster_xp = response.xpath('//a[@class="nbgnbg"]/img/@src').get()
            url_poster_re = re.search('[ps](\d+)', url_poster_xp) if url_poster_xp is not None else ''
            url_poster = url_poster_re.group(1) if url_poster_re != '' else ''

            summary_list_xp = response.xpath('//span[@property="v:summary"]/text()').getall()
            summary = ''
            for summary_xp in summary_list_xp:
                summary += summary_xp.strip()

            see_list = response.xpath('//div[@class="subject-others-interests-ft"]/a/text()').getall()

            # 豆瓣电影
            item_movie = MovieDouban()
            item_movie['id'] = movie_id
            # 影片类型 1:未知 2:电影 3:电视剧 4:短片
            item_movie['id_type_video'] = 2
            if '集数:' in info.xpath('/span/text()').getall():
                item_movie['id_type_video'] = 3
            elif '短片' in type_list:
                item_movie['id_type_video'] = 4
            item_movie['id_movie_imdb'] = id_movie_imdb
            item_movie['start_year'] = start_year
            item_movie['name_zh'] = name_zh
            item_movie['name_origin'] = name_origin
            item_movie['runtime'] = runtime if runtime is not None else 0
            item_movie['url_poster'] = url_poster
            item_movie['summary'] = summary
            item_movie['have_seen'] = 0
            item_movie['wanna_see'] = 0
            for see in see_list:
                if re.match('(\d+)人看过', see) is not None:
                    item_movie['have_seen'] = re.search('(\d+)人看过', see).group(1)
                if re.match('(\d+)人想看', see) is not None:
                    item_movie['wanna_see'] = re.search('(\d+)人想看', see).group(1)
            item_movie['update_date'] = self.today
            print('--------------------------------------')
            print(item_movie)
            yield item_movie

            trailer_xp = response.xpath('//li[@class="label-trailer"]/a/@href').get()
            trailer_re = re.search('\d+', trailer_xp) if trailer_xp is not None else ''

            # 电影预告片
            item_trailer = TrailerMovieDouban()
            item_trailer['id'] = trailer_re.group() if trailer_re is not None else 0
            item_trailer['id_movie_douban'] = movie_id
            item_trailer['url_video'] = ''
            yield item_trailer
            # 电影别名
            alias_label = info.xpath('span[text()="又名:"]').get()
            if alias_label is not None:
                alias_position = 1 if imdb_xp is None else 3
                alias_list = info.xpath('text()[last()-{}]'.format(alias_position)).get().split('/')
                for alias in alias_list:
                    item_alias = AliasMovieDouban()
                    item_alias['id_movie_douban'] = movie_id
                    item_alias['name_alias'] = alias.strip()
                    print('--------------------------------------')
                    print(item_alias)
                    yield item_alias
            # 电影影人
            celebrity_list = info.xpath('.//span/a')
            count = 0
            for celebrity in celebrity_list:
                # 影人类型 2：导演 3:编剧 4：主演
                item_movie_to_celebrity = MovieDoubanToCelebrityDouban()
                item_movie_to_celebrity['id_movie_douban'] = movie_id
                item_movie_to_celebrity['id_celebrity_douban'] = re.search('\d+',
                                                                           celebrity.xpath('@href').get()).group()
                # 主演
                if celebrity.xpath('@rel').get() == 'v:starring':
                    item_movie_to_celebrity['id_profession'] = 4
                    count += 1
                    item_movie_to_celebrity['sort'] = count
                    print('celebrity --------------------------------------')
                    print(item_movie_to_celebrity)
                    yield item_movie_to_celebrity
                    continue
                # 导演
                elif celebrity.xpath('@rel').get() == 'v:directedBy':
                    item_movie_to_celebrity['id_profession'] = 2
                # 编剧
                else:
                    item_movie_to_celebrity['id_profession'] = 3
                item_movie_to_celebrity['sort'] = 0
                print('celebrity --------------------------------------')
                print(item_movie_to_celebrity)
                yield item_movie_to_celebrity
            # 电影类型
            for type_name in type_list:
                item_movie_to_type = MovieDoubanToTypeMovie()
                item_movie_to_type['id_movie_douban'] = movie_id
                if type_name in config.TYPE_MOVIE_LIST:
                    item_movie_to_type['id_type_movie'] = config.TYPE_MOVIE_LIST.index(type_name)
                else:
                    continue
                print('--------------------------------------')
                print(item_movie_to_type)
                yield item_movie_to_type
            # 电影评分
            is_score = response.xpath('//div[@class="rating_sum"]/text()').get()
            if re.search('暂无评分', is_score) is None:
                score = response.xpath('//div[@rel="v:rating"]')
                item_score = RateMovieDouban()
                item_score['id'] = movie_id
                item_score['score'] = score.xpath('div/strong/text()').get()
                item_score['vote'] = score.xpath('.//span[@property="v:votes"]/text()').get()
                vote_list = score.xpath('.//span[@class="rating_per"]/text()').getall()
                for index, vote in enumerate(vote_list):
                    item_score['score{}'.format(5 - index)] = re.search('(.*)%', vote).group(1)
                print('--------------------------------------')
                print(item_score)
                yield item_score
            # 电影标签
            tag_list = response.xpath('//div[@class="tags-body"]/a/text()').getall()
            for tag in tag_list:
                item_tag_movie = TagMovie()
                item_tag_movie['id_movie_douban'] = movie_id
                item_tag_movie['name_zh'] = tag
                print('--------------------------------------')
                print(item_tag_movie)
            # 电影奖项
            award_list = response.xpath('//div[@class="mod"]/ul')
            for award in award_list:
                title = award.xpath('li[1]/a/text()').get()
                id_award = award.xpath('li[1]/a/@href').get().split('/')[4]
                type_award = award.xpath('li[2]/text()').get()
                celebrity_award = award.xpath('li[3]/a/@href').get()
                item_award = AwardMovie()
                item_award['id'] = id_award
                item_award['name_zh'] = re.search('第\d+届(.*)', title).group(1)
                yield item_award
                item_movie_to_award = MovieDoubanToAwardMovie()
                item_movie_to_award['id_movie_douban'] = movie_id
                item_movie_to_award['id_award_movie'] = id_award
                item_movie_to_award['id_celebrity_douban'] = re.search('\d+',
                                                                       celebrity_award).group() if celebrity_award is not None else 0
                item_movie_to_award['type_award'] = type_award.split('(提名)')[0]
                item_movie_to_award['award_th'] = re.search('\d+', title).group()
                item_movie_to_award['is_nominated'] = 0 if re.search('提名', type_award) else 1
                print('--------------------------------------')
                print(item_movie_to_award)
                yield item_movie_to_award
            # 电影影评
            review_list = response.xpath('//div[@class="main review-item"]')
            if review_list:
                for review in review_list:
                    user_id = review.xpath('header/a[@class="name"]/@href').get().split('/')[4]

                    item_user = UserDouban()
                    item_user['id'] = user_id
                    item_user['name_zh'] = review.xpath('header/a[@class="name"]/text()').get()
                    yield item_user

                    date_xp = review.xpath('header/span[@content]/text()').get()
                    review_title = review.xpath('div[@class="main-bd"]/h2/a/text()').get()
                    review_id_xp = review.xpath('div[@class="main-bd"]/h2/a/@href').get()
                    review_id_re = re.search('\d+', review_id_xp) if review_id_xp is not None else ''
                    review_id = review_id_re.group() if review_id_re != '' else 0
                    agree_vote = review.xpath('.//a[@title="有用"]/span/text()').get().strip()
                    against_vote = review.xpath('.//a[@title="没用"]/span/text()').get().strip()

                    item_review = ReviewMovieDouban()
                    item_review['id'] = review_id
                    item_review['agree_vote'] = agree_vote if agree_vote != '' else 0
                    item_review['against_vote'] = against_vote if against_vote != '' else 0
                    item_review['create_datetime'] = int(
                        time.mktime(time.strptime(date_xp, '%Y-%m-%d %H:%M:%S'))) if date_xp is not None else 0
                    item_review['title'] = review_title
                    item_review['content'] = ''.join(
                        review.xpath('.//div[@class="short-content"]/text()').getall()).strip().strip('()').strip()
                    yield item_review
                    print('------------')
                    print(item_review)
                    item_user_review = UserDoubanToReviewMovieDouban()
                    item_user_review['id_user_douban'] = user_id
                    item_user_review['id_review_movie_douban'] = review_id
                    yield item_user_review
                    item_movie_review = MovieDoubanToReviewMovieDouban()
                    item_movie_review['id_movie_douban'] = movie_id
                    item_movie_review['id_review_movie_douban'] = review_id
                    yield item_movie_review

                    score_xp = review.xpath('header/span[@title]/@class').get()
                    score_re = re.search('\d+', score_xp) if score_xp is not None else ''
                    score = int(score_re.group()) if score_re != '' else 0

                    item_user_movie = UserDoubanToMovieDouban()
                    item_user_movie['id_user_douban'] = user_id
                    item_user_movie['id_movie_douban'] = movie_id
                    item_user_movie['score'] = score / 5
                    item_user_movie['is_wish'] = 0
                    item_user_movie['is_seen'] = 1
                    yield item_user_movie
            # 电影资源
            resource_list = response.xpath('//ul[@class="bs"]/li')
            if resource_list:
                for resource in resource_list:
                    item_resource = ResourceMovie()
                    item_resource['id_movie_douban'] = movie_id
                    item_resource['id_movie_imdb'] = id_movie_imdb
                    item_resource['id_website_resource'] = 1
                    website = resource.xpath('a/text()').get().strip()
                    if website in config.WEBSITE_RESOURCE_LIST:
                        item_resource['id_website_resource'] = config.WEBSITE_RESOURCE_LIST.index(website)
                    type = resource.xpath('..//span/text()').get().strip()
                    item_resource['id_type_resource'] = 1
                    if type in config.TYPE_RESOURCE_LIST:
                        item_resource['id_type_resource'] = config.TYPE_RESOURCE_LIST.index(type)
                    item_resource['name_zh'] = name_zh
                    item_resource['create_year'] = start_year
                    item_resource['name_origin'] = name_zh
                    url_resource = resource.xpath('a/@href').get()
                    item_resource['url_resource'] = re.search('https://www\.douban\.com/link2/\?url=(.*)',
                                                              url_resource).group(1) if url_resource is not None else ''
                    print('--------------------')
                    print(item_resource)
                    yield item_resource
            self.logger.info('get douban movie success,id:{}'.format(movie_id))
        else:
            self.logger.warning('get douban movie failed,id:{}'.format(movie_id))
