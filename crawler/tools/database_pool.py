# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import pymysql
from crawler.configs import default as config
from DBUtils.PooledDB import PooledDB

# 数据库连接池(PooledDB)
database_pool = PooledDB(
    # 使用数据库的模块
    creator=pymysql,
    # 数据库最大连接数
    maxconnections=10,
    # 初始化时，链接池中至少创建的空闲的链接
    mincached=5,
    # 初始化时，链接池中至多创建的空闲的链接,0不限制
    maxcached=0,
    # 链接池中最多共享的链接数量
    # PS: 由于pymysql和MySQLdb模块的threadsafety都为1
    # 所以_maxcached永远为0，所有链接都共享
    maxshared=10,
    # 连接池中如果没有可用连接后，是否阻塞等待
    blocking=True,
    # 一个链接最多被重复使用的次数，None表示无限制
    maxusage=None,
    # 开始会话前执行的命令列表,如["set datestyle to ...", "set time zone ..."]
    setsession=[],
    # ping MySQL服务端，检查是否服务可用
    # 如：0 = None = never, 1 = default = whenever it is requested,
    # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
    ping=0,
    host=config.DB_HOST,
    port=config.DB_PORT,
    user=config.DB_USER,
    password=config.DB_PASSWD,
    database=config.DB_NAME,
    charset=config.DB_CHARSET
)
