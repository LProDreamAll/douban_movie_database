# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import re

URL_DYGOD = 'https://www.dy2018.com'

TYPE_LIST = {
    1: '未知',
    2: '免费观看',
    3: 'VIP免费观看',
    4: '单片付费',
    5: '用劵/单片付费',

    101: '在线观看',
    102: '磁力链接',
    103: '迅雷链接',

    111: 'BD在线观看',
}


# 解析资源类型
def parse_type(url):
    if re.match('magnet', url) is not None:
        return 102
    elif re.match('https://www.dy2018.com', url) is not None:
        return 111
