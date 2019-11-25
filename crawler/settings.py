# -*- coding: utf-8 -*-

# Scrapy settings for crawler project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'crawler'

SPIDER_MODULES = ['crawler.spiders']
NEWSPIDER_MODULE = 'crawler.spiders'

# 忽略 robots.txt rules
ROBOTSTXT_OBEY = False

# 日志
# LOG_FILE = 'log_{}.txt'.format(datetime.date.today())
LOG_LEVEL = 'INFO'
# 其它输出是否加入日志
# LOG_STDOUT = True

# 忽略 robots.txt rules
ROBOTSTXT_OBEY = False

# 项目管道
ITEM_PIPELINES = {
    # for redis
    'scrapy_redis.pipelines.RedisPipeline': 100
}

# cookie -----------------------

# True:允许发送cookie False:禁止发送cookie
COOKIES_ENABLED = True

# debug 信息
# COOKIES_DEBUG = True

# 随机请求头 中间件
DOWNLOADER_MIDDLEWARES = {
    'crawler.middlewares.RandomUserAgentMiddleWare': 543,
    # 关闭scrapy自带的代理Middleware
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

# 并发相关 -----------------------

# 连续页面下载间隔时间 s
DOWNLOAD_DELAY = 1

# 默认 Item 并发数：100
CONCURRENT_ITEMS = 100

# 默认 Request 并发数：16
CONCURRENT_REQUESTS = 16

# 默认每个域名的并发数：8
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# 每个IP的最大并发数：0表示忽略
CONCURRENT_REQUESTS_PER_IP = 0

# 缓存 --------------------------

# scrapy缓存 True:允许缓存，每次使用缓存 False:不允许缓存，每次不使用缓存
# HTTPCACHE_ENABLED = True
HTTPCACHE_ENABLED = False

# 设置缓存过期时间（单位：秒）
HTTPCACHE_EXPIRATION_SECS = 3600000

# 缓存路径(默认为：.scrapy/httpcache)
HTTPCACHE_DIR = 'crawler/spiders/httpcache'

# 忽略的状态码
HTTPCACHE_IGNORE_HTTP_CODES = []

# 缓存模式(文件缓存)
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# redis ------------------------
# https://github.com/rmax/scrapy-redis

# redis缓存 True:不允许缓存，自动清理keys False:允许缓存，不自动清理
SCHEDULER_FLUSH_ON_START = True
# SCHEDULER_FLUSH_ON_START = False

# 调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'

# 过滤器(去重),确保所有蜘蛛通过redis共享相同的重复筛选器
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'

# 请求调度使用优先队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.SpiderPriorityQueue'

# 不清理redis队列，允许暂停/恢复爬网
# SCHEDULER_PERSIST = True

# redis 主机+端口号+密码
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_PARAMS = {
    'password': '1233'
}


# ----------------------------------------------------------------------------------------------------

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'crawler (+http://www.yourdomain.com)'


# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
# COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'crawler.middlewares.CrawlerSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'crawler.middlewares.CrawlerDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# ITEM_PIPELINES = {
#    'crawler.pipelines.CrawlerPipeline': 300,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
