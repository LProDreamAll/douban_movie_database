# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

from scrapy import cmdline

spiders = {
    # IMDB => 豆瓣
    1: 'search_douban -a type=movie_imdb',
    2: 'search_douban -a type=celebrity_imdb',

    # IMDB评分
    3: 'movie_imdb',

    # 豆瓣
    11: 'new_douban',

    # 豆瓣详情
    12: 'movie_douban',
    13: 'celebrity_douban',

    14: 'comment_douban',
    15: 'trailer_douban',

    16: 'image_douban -a type=movie',
    17: 'image_douban -a type=celebrity',

    # 场景
    21: 'scene',

    # 场景 => 豆瓣
    22: 'search_douban -a type=movie_scene',
    23: 'search_douban -a type=celebrity_scene',

    # 知乎
    26: 'movie_zhihu',

    # 网易云音乐
    31: 'search_netease',
    32: 'comment_netease',
    33: 'playlist_netease',
    34: 'album_netease',

    # 资源
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

    # 资源 => 豆瓣
    61: 'search_douban -a type=movie_resource',

}
cmdline.execute('scrapy crawl {}'.format(spiders.get(
    26
)).split())
