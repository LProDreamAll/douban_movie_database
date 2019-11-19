# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re
import scrapy
from crawler.tools.database_pool import database_pool
from crawler.configs import default
from crawler.configs import movie_douban as config
from scrapy_redis.spiders import RedisSpider

from crawler.items.movie_douban import MovieDouban
from crawler.items.movie_douban import AliasMovieDouban
from crawler.items.movie_douban import MovieDoubanToCelebrityDouban
from crawler.items.movie_douban import MovieDoubanToTypeMovie
from crawler.items.movie_douban import RateMovieDouban
from crawler.items.movie import TagMovie
from crawler.items.movie import AwardMovie
from crawler.items.movie_douban import MovieDoubanToAwardMovie


class MovieDoubanSpider(RedisSpider):
    """
    豆瓣电影相关

    """
    name = 'movie_douban'
    # start_url存放容器改为redis list
    redis_key = 'movie_douban:start_urls'
    allowed_domains = ['movie.douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.movie_douban.MovieDoubanPipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.conn = database_pool.connection()
        self.cursor = self.conn.cursor()

    def start_requests(self):
        self.cursor.execute('select id from movie_douban where is_updated=0')
        for id, in self.cursor.fetchall():
            yield scrapy.Request(url="{}{}/".format(config.URL_MOVIE_DOUBAN, id),
                                 cookies=default.get_cookie_douban(),
                                 meta={'id': id}, callback=self.parse)

    def parse(self, response):
        movie_id = response.meta['id']
        if response.xpath('//div[@id="content"]'):
            info = response.xpath('//div[@id="info"]')
            title = response.xpath('//h1/span[1]/text()').get()
            start_year = response.xpath('//h1/span[@class="year"]/text()').get()
            type_list = info.xpath('span[@property="v:genre"]/text()').getall()
            imdb_id = info.xpath('span[text()="IMDb链接:"]/following-sibling::a/text()').get()
            # 豆瓣电影
            item_movie = MovieDouban()
            item_movie['id'] = movie_id
            # 影片类型 1:未知 2:电影 3:电视剧 4:短片
            item_movie['id_type_video'] = 2
            if '集数:' in info.xpath('/span/text()').getall():
                item_movie['id_type_video'] = 3
            elif '短片' in type_list:
                item_movie['id_type_video'] = 4
            item_movie['id_movie_imdb'] = re.search('tt(\d+)', imdb_id).group(1) if imdb_id is not None else 0
            item_movie['start_year'] = re.search('[(](\d+)[)]',
                                                 start_year).group(1) if start_year is not None else 0
            # 中文名
            item_movie['name_zh'] = re.search('[\u4e00-\u9fff()\d\s]*',
                                              title).group().strip() if title is not None else ''
            # 原始名
            item_movie['name_origin'] = re.search('[\u4e00-\u9fff()\d\s]*(.*)',
                                                  title).group(1).strip() if title is not None else ''
            item_movie['runtime'] = info.xpath('span[@property="v:runtime"]/@content').get()
            item_movie['url_poster'] = re.search('p(\d+)',
                                                 response.xpath('//a[@class="nbgnbg"]/img/@src').get()).group(1)
            item_movie['summary'] = ''.join(response.xpath('//span[@property="v:summary"]/text()').getall())
            see_list = response.xpath('//div[@class="subject-others-interests-ft"]/a/text()').getall()
            item_movie['have_seen'] = 0
            item_movie['wanna_seen'] = 0
            for see in see_list:
                if re.match('(\d+)人看过', see) is not None:
                    item_movie['have_seen'] = re.search('(\d+)人看过', see).group(1)
                if re.match('(\d+)人想看', see) is not None:
                    item_movie['wanna_seen'] = re.search('(\d+)人想看', see).group(1)
            item_movie['is_updated'] = 1
            print('--------------------------------------')
            print(item_movie)
            yield item_movie
            # 电影别名
            alias_label = info.xpath('span[text()="又名:"]').get()
            if alias_label is not None:
                alias_position = 1 if imdb_id is None else 3
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
                print("each =======================================================================")
                print(celebrity.get())
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
            self.logger.info('get douban movie success,id:{}'.format(movie_id))
        else:
            self.logger.warning('get douban movie failed,id:{}'.format(movie_id))
