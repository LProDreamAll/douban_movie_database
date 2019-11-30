# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import scrapy
from datetime import datetime
from crawler.tools.netease_encrypt import form_data
from crawler.configs import default
from crawler.configs import netease as config
from crawler.spiders.base import BaseSpider

from crawler.items.netease import CommentNetease
from crawler.items.netease import UserNetease


class CommentNeteaseSpider(BaseSpider):
    """
    网易云音乐热门评论相关

    """
    name = 'comment_netease'
    # start_url存放容器改为redis list
    redis_key = 'comment_netease:start_urls'
    allowed_domains = ['music.163.com']
    custom_settings = {
        'ITEM_PIPELINES': {
            'crawler.pipelines.netease.NeteasePipeline': 300
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.form_data = form_data()

    def start_requests(self):
        self.cursor.execute("select song_netease.id from song_netease "
                            "left join comment_netease "
                            "on song_netease.id=comment_netease.id_song_netease "
                            "where comment_netease.id_song_netease is null "
                            'limit {}'.format(default.SELECT_LIMIT))
        for id, in self.cursor.fetchall():
            first_param_dict = config.EAPI_PARAMS
            first_param_dict['rid'] = ''
            first_param_dict['offset'] = 0
            first_param_dict['limit'] = config.NUM_HOT_COMMENT
            first_param = json.dumps(first_param_dict, separators=(',', ':'))
            fd = self.form_data.get_form_data(first_param=first_param, api_type=config.TYPE_EAPI,
                                              eapi_url='{}{}'.format(config.URL_COMMENT_HOT_EAPI, id))
            yield scrapy.FormRequest(url='{}{}'.format(config.URL_COMMENT_HOT, id),
                                     formdata=fd, meta={'id': id}, callback=self.parse)

    def parse(self, response):
        song_id = response.meta['id']
        content = json.loads(response.text)
        # 成功获取结果
        if 'hotComments' in content:
            result = content['hotComments']
            # 获取结果不为空
            if result:
                for comment in result:
                    item_comment = CommentNetease()
                    item_comment['id'] = comment['commentId']
                    item_comment['id_song_netease'] = song_id
                    item_comment['id_user_netease'] = comment['user']['userId']
                    item_comment['create_datetime'] = datetime.fromtimestamp(
                        int(comment['time']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    item_comment['content'] = comment['content']
                    item_comment['agree_vote'] = comment['likedCount']
                    yield item_comment
                    print('------------')
                    print(item_comment)
                    item_user = UserNetease()
                    item_user['id'] = comment['user']['userId']
                    item_user['name_zh'] = comment['user']['nickname']
                    yield item_user
                    print('-----------')
                    print(item_user)
                self.logger.info('get netease hot comment success,movie_id:{}'.format(song_id))
            # 获取结果为空,此歌暂无热门评论,标记为已搜索
            else:
                item_comment = CommentNetease()
                item_comment['id'] = 0
                item_comment['id_song_netease'] = song_id
                item_comment['id_user_netease'] = 0
                item_comment['create_datetime'] = 0
                item_comment['content'] = ''
                item_comment['agree_vote'] = 0
                yield item_comment
                self.logger.info('get netease hot comment None,movie_id:{}'.format(song_id))
        # 获取结果失败
        else:
            self.logger.warning('get netease hot comment failed,movie_id:{}'.format(song_id))
