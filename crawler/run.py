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
    4: 'image_douban -a tpye=movie',
    5: 'image_douban -a tpye=celebrity',
    6: 'search_douban -a tpye=movie_imdb',
    7: 'search_douban -a tpye=celebrity_imdb',
    8: 'search_douban -a tpye=movie_scene',
    9: 'search_douban -a tpye=celebrity_scene',
    10: 'search_douban -a tpye=movie_resource',

    11: 'search_netease',
    12: 'playlist_netease',
    13: 'comment_netease',
    14: 'album_netease',

    15: 'scene',
    16: '',
}
cmdline.execute('scrapy crawl {}'.format(spiders.get(
    4
)).split())
