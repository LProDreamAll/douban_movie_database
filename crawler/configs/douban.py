# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------

"""
豆瓣配置

"""
import random
import string

# 豆瓣电影 + ID + /
URL_MOVIE = 'https://movie.douban.com/subject/'

# 豆瓣影人 +  ID + /
URL_CELEBRITY = 'https://movie.douban.com/celebrity/'

# 豆瓣电影图片 start + ID + end
URL_IMAGE_MOVIE_START = 'https://movie.douban.com/subject/'
URL_IMAGE_MOVIE_END = '/photos?type=S&start=0&sortby=like&size=a&subtype=o'

# 豆瓣影人图片 start + ID + end
URL_IMAGE_CELEBRITY_START = 'https://movie.douban.com/celebrity/'
URL_IMAGE_CELEBRITY_END = '/photos/?type=C&start=0&sortby=size&size=a&subtype=a'

# 豆瓣电影智能搜索框 + 搜索关键字
URL_SEARCH_TIPS_MOVIE = 'https://movie.douban.com/j/subject_suggest?q='

# 豆瓣电影搜索页面 + 搜索关键字
URL_SEARCH_MOVIE = 'https://search.douban.com/movie/subject_search?search_text='

# 搜索内容电影上映时间精确度
ACCURACY_RELEASE_TIME = 1

# 电影短评链接 start + ID +end
URL_COMMENT_MOVIE_START = 'https://movie.douban.com/subject/'
URL_COMMENT_MOVIE_END = '/comments?start=0&limit=20&sort=new_score&status=P'

# 电影预告片链接 + ID + /
URL_TRAILER_MOVIE = 'https://movie.douban.com/trailer/'

# 豆瓣电影最新上映 + start
URL_MOVIE_NEW = 'https://movie.douban.com/j/new_search_subjects?sort=R&range=0,10&tags=&start='

# 最新上映 最大数
NEW_MOVIE_MAX = 1000

# 豆瓣搜索解密JS路径
# console模式
# PATH_DOUBAN_SEARCH_DECRYPT = './crawler/tools/douban_search_decrypt.js'
# PyCharm Debug模式
PATH_DOUBAN_SEARCH_DECRYPT = './tools/douban_search_decrypt.js'


def get_cookie_douban():
    """
    豆瓣cookie随机生成

    :return:字典形式的cookie
    """
    return {'Cookie': 'bid=%s' % ''.join(random.sample(string.ascii_letters + string.digits, 11))}


# 资源类型,下标即ID
TYPE_RESOURCE_LIST = [
    '',
    '',
    '免费观看',
    'VIP免费观看',
    '单片付费',
    '用劵/单片付费'
]

# 资源网站，下标即ID
WEBSITE_RESOURCE_LIST = [
    '',
    '',
    '爱奇艺视频',
    '腾讯视频',
    '哔哩哔哩',
    '搜狐视频',
    '优酷视频',
    '1905电影网',
    '芒果TV'
]

# 电影类型 下标即为其ID
TYPE_MOVIE_LIST = [
    '',
    '未知',
    '剧情',
    '喜剧',
    '爱情',
    '动作',
    '惊悚',
    '动画',
    '犯罪',
    '纪录片',
    '短片',
    '恐怖',
    '悬疑',
    '科幻',
    '冒险',
    '奇幻',
    '家庭',
    '战争',
    '历史',
    '传记',
    '音乐',
    '同性',
    '古装',
    '歌舞',
    '运动',
    '情色',
    '儿童',
    '武侠',
    '西部',
    '真人秀',
    '黑色电影',
    '灾难',
    '脱口秀',
    '舞台艺术',
    '戏曲',
    '鬼怪'
]
