# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re

# 电影天堂
URL_DYGOD = 'https://www.dy2018.com'

# LOL电影天堂
URL_LOLDYTT = 'https://www.loldytt.tv'

# BT电影天堂
URL_BTBTDY = 'http://www.btbtdy.me'

# 迅雷电影天堂
URL_XL720 = 'https://www.xl720.com'

# LOL电影天堂 电影类型列表
LOLDYTT_TYPE_LIST = [
    'Dongzuodianying',
    'Kehuandianying',
    'Kongbudianying',
    'Xijudianying',
    'Aiqingdianying',
    'Juqingdianying',
    'Zhanzhengdianying',
    'Anime',
    'Zuixinzongyi',
    'Dianshiju',
    'Zuixinmeiju',
    'Zuixinhanju',
    'Zuixingangju',
    'Ouxiangju',
    'Zuixinriju',
    'Taiguodianshiju'
]

TYPE_LIST = {
    1: '免费观看',
    2: 'VIP免费观看',
    3: '单片付费',
    4: '用劵/单片付费',

    100: '未知',

    101: '在线观看',
    102: '网盘',

    111: 'BluRay',
    112: '1080p',
    113: '1280超清',
    114: '1024超清',
    115: '720p',
    116: '1280高清',
    117: '1024高清',
}


# 解析资源类型
def parse_type(name):
    if name is None:
        return 100
    if '在线' in name or '播放' in name:
        return 101
    elif '网盘' in name:
        return 102
    elif '1280' in name:
        if '超清' in name:
            return 113
        elif '高清' in name:
            return 116
    elif '1024' in name:
        if '超清' in name:
            return 114
        elif '高清' in name:
            return 117
    elif '1080' in name:
        return 112
    elif '720' in name:
        return 115
    elif '蓝光' in name or 'BluRay' in name:
        return 111
    else:
        return 100
