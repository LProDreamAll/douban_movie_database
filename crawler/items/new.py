# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy


class MovieDouban(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()
