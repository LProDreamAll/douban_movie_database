# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

from scrapy import cmdline

spiders = {
    0: 'movie_douban',
    1: 'celebrity_douban',
    2: 'comment_douban',
    3: 'trailer_douban',
    4: 'image_douban -a type=movie',
    5: 'image_douban -a type=celebrity',
    6: 'search_douban -a type=movie_imdb',
    7: 'search_douban -a type=celebrity_imdb',
    8: 'search_douban -a type=movie_scene',
    9: 'search_douban -a type=celebrity_scene',
    10: 'search_douban -a type=movie_resource',

    11: 'movie_imdb',

    20: 'search_netease',
    21: 'playlist_netease',
    22: 'comment_netease',
    23: 'album_netease',

    31: 'scene',

    41: 'dy2018_resource -a type=all',
    42: 'dy2018_resource -a type=new',
    43: 'loldytt_resource -a type=all',
    44: 'loldytt_resource -a type=new',
    45: 'btbtdy_resource -a type=all',
    46: 'btbtdy_resource -a type=new',
    47: 'xl720_resource -a type=all',
    48: 'xl720_resource -a type=new',
    49: 'hao6v_resource -a type=all',
    50: 'hao6v_resource -a type=new',
    51: 'goudaitv_resource -a type=all',
    52: 'goudaitv_resource -a  type=new',
    53: 'zxzjs_resource -a type=all',
    54: 'zxzjs_resource -a type=new',
    55: '',
    56: '',
    57: '',

}
cmdline.execute('scrapy crawl {}'.format(spiders.get(
    1
)).split())
