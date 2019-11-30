# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
import random

# 热评个数
NUM_HOT_COMMENT = 20

# -----------------------------------

# weapi 搜索链接 (类型集合)
URL_WEAPI_SEARCH_TIPS = 'https://music.163.com/weapi/search/suggest/web'

# eapi 搜索链接 （信息较全）(但类型单一)
URL_EAPI_SEARCH_TIPS = 'https://music.163.com/eapi/v1/search/get'

# eapi 请求参数中需要用到的搜索链接
URL_SEARCH_TIPS_EAPI_NEED = '/api/v1/search/get'

# eapi 歌曲热门评论链接 + ID
URL_COMMENT_HOT = 'http://music.163.com/eapi/v1/resource/hotcomments/R_SO_4_'

# eapi 请求参数中需要用到的歌曲热门评论链接 + ID
URL_COMMENT_HOT_EAPI = '/api/v1/resource/hotcomments/R_SO_4_'

# weapi 歌单链接
URL_PLAYLIST = 'https://music.163.com/weapi/v1/playlist/detail'

# weapi 专辑链接 + ID
URL_ALBUM = 'https://music.163.com/weapi/v1/album/'

# weapi 歌曲资源 (资源有时间限制，舍弃)
# URL_RESOURCE = 'https://music.163.com/weapi/song/enhance/player/url/v1'

# api类型
TYPE_WEAPI = 0
TYPE_EAPI = 1
API_TYPE = TYPE_WEAPI

# 模拟参数
SECOND_PARAM = "010001"
THIRD_PARAM = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
FORTH_PARAM = "0CoJUm6Qyw8W8jud"

# 密钥偏移量
IV = "0102030405060708"
# EAPI_KEY
EAPI_KEY = "e82ckenh8dichen8"

# 请求表单之params,用于获取params的两次AES加密Key
FIRST_KEY = FORTH_PARAM
SECOND_KEY = 16 * 'F'

# 请求表单之encSecKey
ENCSECKEY = "257348aecb5e556c066de214e531faadd1c55d814f9be95fd06d6bff9f4c7a41f831f6394d5a3fd2e3881736d94a02ca919d952872e7d0a50ebfa1769a7a62d512f5f1ca21aec60bc3819a9c3ffca5eca9a0dba6d6f7249b06f5965ecfff3695b54e1c28f3f624750ed39e7de08fc8493242e26dbc4484a01c76f739e135637c"

# 为eapi添加的请求头
EAPI_HEADERS = {
    'os': 'osx',
    'appver': '2.5.3',
    'requestId': str(random.randint(10000000, 99999999)),
    'clientSign': '',
}

# eapi的请求参数（eapi公共）
EAPI_PARAMS = {
    'verifyId': 1,
    'os': 'OSX',
    'header': json.dumps(EAPI_HEADERS, separators=(',', ':'))
}
