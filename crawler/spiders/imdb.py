# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import re
import scrapy
from crawler.configs import default
from crawler.configs import imdb as config
from crawler.spiders.base import BaseSpider

from crawler.items.imdb import MovieImdb
from crawler.items.imdb import RateImdb


class ImdbSpider(BaseSpider):
    """
    IMDB相关

    """
    name = 'movie_imdb'
    # start_url存放容器改为redis list
    redis_key = 'movie_imdb:start_urls'
    allowed_domains = ['www.omdbapi.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.imdb.ImdbPipeline': 300
        }
    }

    def __init__(self,  **kwargs):
        super().__init__(**kwargs)
        self.type_new = 'new'

    def start_requests(self):
        self.cursor.execute(
            'select id_movie_imdb from movie_douban where id_movie_imdb!=0 and is_updated=1 limit {}'
                .format(default.SELECT_LIMIT))
        for id, in self.cursor.fetchall():
            yield scrapy.Request(url='{}tt{}'.format(config.URL_OMDB_SEARCH, '%07d' % id),
                                 meta={'imdb_id': id}, callback=self.parse)

    def parse(self, response):
        imdb_id = response.meta['imdb_id']
        content = json.loads(response.text)
        if 'imdbID' in content and 'tt{}'.format('%07d' % imdb_id) == content['imdbID']:
            item_movie = MovieImdb()
            item_movie['id'] = imdb_id
            item_movie['url_poster'] = content['Poster']
            item_movie['summary'] = content['Plot']
            yield item_movie
            print('----------------')
            print(item_movie)
            item_rate = RateImdb()
            item_rate['id'] = imdb_id
            item_rate['imdb_score'] = content['imdbRating']
            item_rate['imdb_vote'] = content['imdbVotes'].replace(',', '') if type(content['imdbVotes']) == str else 0
            item_rate['tomato_score'] = 0
            item_rate['mtc_score'] = 0
            for rate in content['Ratings']:
                if rate['Source'] == 'Rotten Tomatoes':
                    item_rate['tomato_score'] = int(re.match('\d+', rate['Value']).group()) / 10
                elif rate['Source'] == 'Metacritic':
                    item_rate['mtc_score'] = int(re.match('(\d+)/100', rate['Value']).group(1)) / 10
            yield item_rate
            print('-----------------')
            print(item_rate)
            self.logger.info('get omdb\'s movie success,imdb_id:{}'.format(imdb_id))
        else:
            self.logger.warning('get omdb\'s movie failed,imdb_id:{}'.format(imdb_id))

