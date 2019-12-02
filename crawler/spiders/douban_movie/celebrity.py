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

from crawler.items.douban import CelebrityDouban
from crawler.items.douban import AliasCelebrityDouban
from crawler.items.douban import MovieDoubanToAwardMovie
from crawler.items.douban import AwardMovie


class CelebrityDoubanSpider(BaseSpider):
    """
    豆瓣影人相关

    """
    name = 'celebrity_douban'
    # start_url存放容器改为redis list
    redis_key = 'celebrity_douban:start_urls'
    allowed_domains = ['movie.douban.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.douban_movie.douban.DoubanPipeline': 300
        }
    }

    def start_requests(self):
        self.cursor.execute('select id from celebrity_douban limit {}'.format(default.SELECT_LIMIT))
        for id, in self.cursor.fetchall():
            yield scrapy.Request(url="{}{}/".format(config.URL_CELEBRITY, id),
                                 cookies=config.get_cookie_douban(),
                                 meta={'id': id}, callback=self.parse)

    def parse(self, response):
        celebrity_id = response.meta['id']
        if response.xpath('//div[@id="content"]'):
            info = response.xpath('//div[@class="info"]')
            title = response.xpath('//h1/text()').get()
            sex = info.xpath('.//span[text()="性别"]/../text()[2]').get()
            imdb_id = info.xpath('.//span[text()="imdb编号"]/following-sibling::a/text()').get()

            birth_date_xp = info.xpath('.//span[text()="出生日期"]/../text()[2]').get()
            birth_re = re.search('\d{4}-\d{2}-\d{2}', birth_date_xp) if birth_date_xp is not None else ''
            birth = birth_re.group() if birth_re != '' else 0

            # 豆瓣影人
            item_celebrity = CelebrityDouban()
            item_celebrity['id'] = celebrity_id
            item_celebrity['id_celebrity_imdb'] = re.search('\d+', imdb_id).group() if imdb_id is not None else 0
            item_celebrity['name_zh'] = re.search('[\u4e00-\u9fff·\s]*',
                                                  title).group().strip() if title is not None else ''
            item_celebrity['name_origin'] = re.search('[\u4e00-\u9fff()·\s]*(.*)',
                                                      title).group(1).strip() if title is not None else ''
            item_celebrity['sex'] = 2
            if re.search('男', sex) is not None:
                item_celebrity['sex'] = 1
            elif re.search('女', sex) is not None:
                item_celebrity['sex'] = 0
            item_celebrity['birth_date'] = int(time.mktime(time.strptime(birth, '%Y-%m-%d')))
            item_celebrity['url_portrait'] = re.search('p(\d+)', response.xpath(
                '//div[@class="pic"]//a[@class="nbg"]/@href').get()).group(1)
            summary_body = response.xpath('//div[@id="intro"]/div[@class="bd"]/span')
            item_celebrity['summary'] = ''
            if not summary_body:
                item_celebrity['summary'] += response.xpath('//div[@id="intro"]/div[@class="bd"]/text()').get()
            else:
                summary_list = summary_body.xpath('text()').getall()
                item_celebrity['summary'] = ''.join(summary_list)
            item_celebrity['update_date'] = self.today
            # print(item_celebrity)
            yield item_celebrity
            # 奖项
            award_list = response.xpath('//ul[@class="award"]')
            for award in award_list:
                title = award.xpath('li[2]/a/text()').get()
                id_award = award.xpath('li[2]/a/@href').get().split('/')[4]
                type_award = award.xpath('li[3]/text()').get()
                movie_award = award.xpath('li[4]/a/@href').get()
                item_award = AwardMovie()
                item_award['id'] = id_award
                item_award['name_zh'] = re.search('第\d+届(.*)', title).group(1)
                # print('---------------------')
                # print(item_award)
                yield item_award
                item_movie_to_award = MovieDoubanToAwardMovie()
                item_movie_to_award['id_movie_douban'] = re.search(
                    '\d+', movie_award).group() if movie_award is not None else 0
                item_movie_to_award['id_award_movie'] = id_award
                item_movie_to_award['id_celebrity_douban'] = celebrity_id
                item_movie_to_award['type_award'] = type_award.split('(提名)')[0]
                item_movie_to_award['award_th'] = re.search('\d+', title).group()
                item_movie_to_award['is_nominated'] = 0 if re.search('提名', type_award) else 1
                # print('---------------------------')
                # print(item_movie_to_award)
                yield item_movie_to_award
            # 影人别名
            alias_zh = info.xpath('ul/li/span[text()="更多外文名"]/../text()[2]').get()
            alias_other = info.xpath('ul/li/span[text()="更多外文名"]/../text()[2]').get()
            alias_list = alias_zh.split('/') if alias_zh is not None else []
            if alias_other is not None:
                alias_list.extend(alias_other.split('/'))
            for alias in alias_list:
                item_alias = AliasCelebrityDouban()
                item_alias['id_celebrity_douban'] = celebrity_id
                item_alias['name_alias'] = re.search('[^\s:].*[^\s()昵称本名]', alias).group().strip()
                item_alias['is_nikename'] = 0
                if re.search('昵称', alias) is not None:
                    item_alias['is_nikename'] = 1
                # print('----------------')
                # print(item_alias)
                yield item_alias
            self.logger.info('get douban celebrity success,id:{}'.format(celebrity_id))
        else:
            self.logger.warning('get douban celebrity failed,id:{}'.format(celebrity_id))
