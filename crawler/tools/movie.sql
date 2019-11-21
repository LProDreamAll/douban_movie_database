/*
 电影数据库

 author:	humingk

 目录简介：

 电影：
 公共电影相关
 IMDB电影相关
 豆瓣电影相关

 名人：
 公共名人相关
 IMDB名人相关
 豆瓣名人相关

 片场：
 电影片场相关

 用户：
 公共用户相关
 豆瓣用户相关

 资源：
 电影资源相关
 图片资源相关

 区域：
 场景区域相关

 音乐：
 网易云音乐相关

 表初始化
 选择是否添加外键关系
 IMDB转换SQL语句
 PS:
 id含有 auto_increment 属性的表，id=1均为默认值-未知
 id不含有 auto_increment 属性的表，id=0均为默认值-未知
 */


# 电影 start ========================================================================================

# 公共电影相关 ---------------------------------------------------------------------------------

# 1.公共电影基础表---------------------------------------

# 影片种类/类型  (电影、电视剧...) 
create table type_video
(
    id      tinyint unsigned not null primary key,
    # 影片类型中文名
    name_zh varchar(255)     not null default '',
    # 影片类型英文名
    name_en varchar(255)     not null default '',

    index (name_zh),
    index (name_en)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 电影奖项 
create table award_movie
(
    id      varchar(255) not null primary key,
    # 奖项名称
    name_zh varchar(255) not null default '',

    index (name_zh)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into award_movie
values ('unknown', '未知');

# 电影类型
create table type_movie
(
    id      smallint unsigned not null primary key,
    # 类型中文名
    name_zh varchar(255)      not null default '',

    unique (name_zh)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 2.公共电影关系表---------------------------------------

# IMDB电影相关 ---------------------------------------------------------------------------------

# 1.IMDB电影基础表---------------------------------------

# IMDB电影 
create table movie_imdb
(
    id            bigint unsigned      not null primary key,
    # 影片种类/类型  (电影、电视剧、电视剧的单集...)
    id_type_video tinyint unsigned     not null default 1,
    # IMDB电影英文名
    name_en       varchar(255)         not null default '',
    # IMDB电影发行年份 、 电视剧首集播放年份
    start_year    smallint(4) unsigned not null default 0,
    # IMDB电影发行年份 、 最后一集播放年份
    end_year      smallint(4) unsigned not null default 0,
    # 是否是成人电影 0-不是 1-是
    is_adult      tinyint(1)           not null default 0,
    # IMDB电影原始名
    name_origin   varchar(255)         not null default '',
    # IMDB电影片长 分钟
    runtime       smallint unsigned    not null default 0,
    # imdb海报
    url_poster    varchar(1000)        not null default '',

    index (id_type_video),
    index (name_en),
    index (start_year desc),
    index (end_year desc),
    index (name_origin)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into movie_imdb(id, name_en)
values (0, 'unknown');

# IMDB电影评分
create table rate_imdb
(
    # tt+id,id至少7个数字（不够7个在id前面添0）
    id           bigint unsigned not null primary key,
    # IMDB评分
    imdb_score   decimal(3, 1)   not null default 0.0,
    # IMDB评分人数
    imdb_vote    int unsigned    not null default 0,
    # MTC评分
    mtc_score    decimal(3, 1)   not null default 0.0,
    # 烂番茄新鲜度
    tomato_score decimal(3, 1)   not null default 0.0,

    index (mtc_score desc),
    index (tomato_score desc),
    index (imdb_score desc),
    index (imdb_vote desc)
) ENGINE = InnoDB
  default charset = utf8mb4;


# 2.IMDB电影关系表---------------------------------------

# IMDB电影-电影类型
create table movie_imdb_to_type_movie
(
    id_movie_imdb bigint unsigned   not null,
    id_type_movie smallint unsigned not null,

    primary key (id_movie_imdb, id_type_movie)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣电影相关 ---------------------------------------------------------------------------------

# 1.豆瓣电影基础表---------------------------------------

# 豆瓣电影 
create table movie_douban
(
    id            bigint unsigned      not null primary key,
    # 影片种类/类型-ID  (电影、电视剧、电视剧的单集...)
    id_type_video tinyint unsigned     not null default 1,
    # 豆瓣电影的IMDB-ID
    id_movie_imdb bigint unsigned      not null default 0,
    # 上映时间
    start_year    smallint(4) unsigned not null default 0,
    # 豆瓣电影中文名
    name_zh       varchar(255)         not null default '',
    # 豆瓣电影原始名
    name_origin   varchar(255)         not null default '',
    # 豆瓣电影运行片长 分钟
    runtime       smallint unsigned    not null default 0,
    # 豆瓣电影海报ID
    url_poster    bigint unsigned      not null default 0,
    # 简介
    summary       text,
    # 已看人数
    have_seen     int unsigned         not null default 0,
    # 想看人数
    wanna_seen    int unsigned         not null default 0,
    # 是否更新 0-否 1-已经更新
    is_updated    tinyint unsigned     not null default 0,


    index (id_type_video),
    index (id_movie_imdb),
    index (start_year),
    index (name_zh),
    index (name_origin)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into movie_douban(id, name_zh, name_origin)
values (0, '未知', 'unknown');

# 豆瓣电影评分
create table rate_movie_douban
(
    id     bigint unsigned not null primary key,
    # 豆瓣电影评分 0.0 ~ 10.0
    score  decimal(3, 1)   not null default 0.0,
    # 豆瓣电影评分人数
    vote   int unsigned    not null default 0,
    # 豆瓣1星 %
    score1 decimal(3, 1)   not null default 0.0,
    # 豆瓣2星 %
    score2 decimal(3, 1)   not null default 0.0,
    # 豆瓣3星 %
    score3 decimal(3, 1)   not null default 0.0,
    # 豆瓣4星 %
    score4 decimal(3, 1)   not null default 0.0,
    # 豆瓣5星 %
    score5 decimal(3, 1)   not null default 0.0,

    index (score desc),
    index (vote desc)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 电影别名
create table alias_movie_douban
(
    id_movie_douban bigint unsigned not null default 0,
    # 豆瓣电影别称
    name_alias      varchar(255)    not null default '',

    primary key (id_movie_douban, name_alias)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣电影预告片
create table trailer_movie_douban
(
    id              bigint unsigned not null primary key,
    # 豆瓣电影ID
    id_movie_douban bigint unsigned not null default 0,
    # 预告片mp4链接
    url_video       varchar(255)    not null default '',

    index (id_movie_douban)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣电影经典台词
create table classic_douban
(
    id              bigint unsigned not null auto_increment primary key,
    # 豆瓣电影ID
    id_movie_douban bigint unsigned not null default 0,
    # 经典台词内容
    content         varchar(1000)   not null default '',
    # 经典台词在影片中的出现时间 分钟
    happen_time     int unsigned    not null default 0,
    # 经典台词获得的票数
    agree_vote      int unsigned    not null default 0,

    index (id_movie_douban),
    index (content(20)),
    index (happen_time asc),
    index (agree_vote desc)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into classic_douban
values (0, 0, '', 0, 0);


# 豆瓣电影短评
create table comment_movie_douban
(
    id_movie_douban bigint unsigned not null,
    id_user_douban  varchar(255)    not null,
    # 投票数
    agree_vote      smallint        not null default 0,
    # 短评日期
    create_date     date,
    # 短评内容
    content         varchar(1000)   not null default '',

    primary key (id_movie_douban, id_user_douban),
    index (agree_vote desc),
    index (content(20))
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣电影影评
create table review_movie_douban
(
    id              bigint unsigned not null primary key,
    # 赞同数
    agree_vote      int unsigned    not null default 0,
    # 反对数
    against_vote    int unsigned    not null default 0,
    # 影评日期时间
    create_datetime datetime,
    # 影评内容
    content         text,

    index (agree_vote desc),
    index (against_vote desc),
    index (content(20))
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣电影标签
create table tag_movie
(
    id_movie_douban bigint unsigned not null default 0,
    name_zh         varchar(255)    not null default '',

    primary key (id_movie_douban, name_zh)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 2.豆瓣电影关系表---------------------------------------

# 豆瓣电影-电影类型
create table movie_douban_to_type_movie
(
    id_movie_douban bigint unsigned   not null,
    id_type_movie   smallint unsigned not null,

    primary key (id_movie_douban, id_type_movie)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣电影-奖项
create table movie_douban_to_award_movie
(
    # 获奖豆瓣电影ID
    id_movie_douban     bigint unsigned   not null default 0,
    # 获奖奖项ID
    id_award_movie      varchar(255)      not null default 'unknown',
    # 获奖豆瓣名人ID
    id_celebrity_douban bigint unsigned   not null default 0,
    # 奖项的类别中文名 (最佳XXX...)
    type_award          varchar(255)      not null default '未知',
    # 获奖奖项届数 
    award_th            smallint unsigned not null default 1,
    # 是否提名 0-仅提名，未获奖 1-获奖者，非提名
    is_nominated        tinyint(1)        not null default 0,

    primary key (id_movie_douban, id_award_movie, id_celebrity_douban, type_award, award_th)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣电影-影评
create table movie_douban_to_review_movie_douban
(
    id_movie_douban        bigint unsigned not null,
    id_review_movie_douban bigint unsigned not null,

    primary key (id_movie_douban, id_review_movie_douban)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 电影 end ========================================================================================

# 名人 start ========================================================================================

# 公共名人相关 ---------------------------------------------------------------------------------

# 1.公共名人基础表---------------------------------------

# 名人职业
create table profession
(
    id      tinyint unsigned not null primary key,
    # 职业中文名
    name_zh varchar(255)     not null default '',
    # 职业英文名
    name_en varchar(255)     not null default '',

    index (name_zh),
    index (name_en)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 2.公共名人关系表---------------------------------------

# IMDB名人相关 ---------------------------------------------------------------------------------

# 1.IMDB名人基础表---------------------------------------

# IMDB名人
create table celebrity_imdb
(
    # nm+id,id至少7个数字（不够7个在id前面添0）
    id         bigint unsigned      not null primary key,
    # 英文名
    name_en    varchar(255)         not null default '',
    # 出生年份
    birth_year smallint(4) unsigned not null default 0,
    # 死亡年份
    death_year smallint(4) unsigned not null default 0,

    index (name_en)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into celebrity_imdb(id, name_en)
values (0, 'unknown');

# 2.IMDB名人关系表---------------------------------------

# IMDB电影-名人
create table movie_imdb_to_celebrity_imdb
(
    id_movie_imdb     bigint unsigned  not null,
    id_celebrity_imdb bigint unsigned  not null,
    # 该IMDB名人在该IMDB电影中的职位
    id_profession     tinyint unsigned not null,
    # 该人在该电影中工作描述
    description       varchar(1000)    not null default '',

    primary key (id_movie_imdb, id_celebrity_imdb, id_profession)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣名人相关 ---------------------------------------------------------------------------------

# 1.豆瓣名人基础表---------------------------------------

# 豆瓣名人
create table celebrity_douban
(
    id                bigint unsigned not null primary key,
    # IMDB-ID
    id_celebrity_imdb bigint unsigned not null default 0,
    # 中文名
    name_zh           varchar(255)    not null default '',
    # 英文名
    name_origin       varchar(255)    not null default '',
    # 性别 0-女 1-男 2-其他
    sex               tinyint(1)      not null default 2,
    # 生日日期
    birth_date        date,
    # 豆瓣影人海报ID
    url_portrait      bigint unsigned not null default 0,
    # 影人简介
    summary           text,
    # 是否更新 0-否 1-已更新
    is_updated        tinyint(1)      not null default 0,

    index (id_celebrity_imdb),
    index (name_zh),
    index (name_origin)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into celebrity_douban(id, name_zh, name_origin)
values (0, '未知', 'unknown');

# 影人别名
create table alias_celebrity_douban
(
    id_celebrity_douban bigint unsigned not null default 0,
    # 豆瓣影人别称
    name_alias          varchar(255)    not null default '',
    # 是否为昵称 0-本名 1-昵称
    is_nikename         tinyint(1)      not null default 0,

    primary key (id_celebrity_douban, name_alias)
) ENGINE = InnoDB
  default charset = utf8mb4;


# 2.豆瓣名人关系表---------------------------------------

# 豆瓣电影-名人
create table movie_douban_to_celebrity_douban
(
    id_movie_douban     bigint unsigned   not null,
    id_celebrity_douban bigint unsigned   not null,
    # 该豆瓣名人在该豆瓣电影中的职位
    id_profession       tinyint unsigned  not null default 1,
    # 该豆瓣名人在该豆瓣电影中的主演顺序
    sort                smallint unsigned not null default 0,

    primary key (id_movie_douban, id_celebrity_douban, id_profession),
    index (sort asc)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣电影经典台词-名人
create table celebrity_douban_to_classic
(
    id_celebrity_douban bigint unsigned not null,
    id_classic_douban   bigint unsigned not null,

    primary key (id_celebrity_douban, id_classic_douban)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 名人 end ========================================================================================

# 片场 start ========================================================================================

# 电影片场相关 ---------------------------------------------------------------------------------

# 1.电影片场基础表---------------------------------------

# 场景电影
create table movie_scene
(
    id              bigint unsigned      not null primary key,
    # 场景电影对应的豆瓣电影ID
    id_movie_douban bigint unsigned      not null default 0,
    # 场景电影中文名
    name_zh         varchar(255)         not null default '',
    # 场景电影英文名
    name_en         varchar(255)         not null default '',
    # 上映时间
    start_year      smallint(4) unsigned not null default 0,
    # 场景电影拍摄地点大致描述
    description     varchar(1000)        not null default '',
    # 场景电影地点分布图链接
    url_map         varchar(1000)        not null default '',

    index (id_movie_douban),
    index (name_zh),
    index (name_en)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into movie_scene(id, id_movie_douban, name_zh, name_en)
values (0, 0, '未知', 'unknown');

# 场景名人
create table celebrity_scene
(
    id                  bigint unsigned not null primary key,
    # 场景电影对应的豆瓣名人ID
    id_celebrity_douban bigint unsigned not null default 0,
    # 场景名人中文名
    name_zh             varchar(255)    not null default '',
    # 场景名人英文名
    name_en             varchar(255)    not null default '',

    index (id_celebrity_douban),
    index (name_zh),
    index (name_en)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into celebrity_scene(id, id_celebrity_douban, name_zh, name_en)
values (0, 0, '未知', 'unknown');

# 场景
create table scene
(
    id             bigint unsigned not null primary key,
    # 场景对应的场景电影ID
    id_movie_scene bigint unsigned not null default 0,
    # 场景对应的地点ID
    id_place_scene bigint unsigned not null default 0,
    # 场景中文名
    name_zh        varchar(255)    not null default '',
    # 场景发生在电影中的时间 秒
    happen_time    int unsigned    not null default 0,

    index (id_movie_scene),
    index (id_place_scene),
    index (name_zh),
    index (happen_time asc)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into scene(id, name_zh)
values (0, '未知');

# 场景详情 （一个场景可能对应多个场景详情）
create table scene_detail
(
    id             bigint unsigned not null primary key,
    # 场景详情对应的场景ID
    id_scene       bigint unsigned not null default 0,
    # 场景详情对应的场景电影ID
    id_movie_scene bigint unsigned not null default 0,
    # 场景发生在电影中的时间 秒
    happen_time    int unsigned    not null default 0,
    # 场景描述
    description    varchar(1000)   not null default '',

    index (id_scene),
    index (id_movie_scene),
    index (happen_time asc)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into scene_detail(id, description)
values (0, '未知');

# 2.电影片场关系表---------------------------------------

# 场景电影-场景名人
create table movie_scene_to_celebrity_scene
(
    id_movie_scene     bigint unsigned not null,
    id_celebrity_scene bigint unsigned not null,

    primary key (id_movie_scene, id_celebrity_scene)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 场景详情-场景名人
create table scene_detail_to_celebrity_scene
(
    id_scene_detail    bigint unsigned not null,
    id_celebrity_scene bigint unsigned not null,

    primary key (id_scene_detail, id_celebrity_scene)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 片场 end ========================================================================================

# 用户 start ========================================================================================

# 公共用户相关 ---------------------------------------------------------------------------------

# 1.公共用户基础表---------------------------------------

# 用户角色
create table role
(
    id          tinyint unsigned not null auto_increment primary key,
    # 角色名称
    name_zh     varchar(255)     not null default '',
    # 角色描述
    description varchar(255)     not null default '',

    index (name_zh)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into role
values (1, '未知', 'unknown');

# 用户权限
create table permission
(
    id          int unsigned not null auto_increment primary key,
    # 权限名称
    name_zh     varchar(255) not null default '',
    # 权限路径
    path_src    varchar(255) not null default 'x',
    # 权限描述
    description varchar(255) not null default '',

    index (name_zh),
    unique (path_src)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into permission
values (1, '未知', 'x', '');

# 2.公共用户关系表---------------------------------------

# 角色-权限
create table role_to_permission
(
    id_role       tinyint unsigned not null,
    id_permission int unsigned     not null,

    primary key (id_role, id_permission)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣用户相关 ---------------------------------------------------------------------------------

# 1.豆瓣用户基础表---------------------------------------

# 豆瓣用户
create table user_douban
(
    id      varchar(255) not null primary key,
    # 名字
    name_zh varchar(255) not null default '',

    index (name_zh)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 2.豆瓣用户关系表---------------------------------------

# 豆瓣用户-角色
create table user_douban_to_role
(
    id_user_douban int unsigned     not null,
    id_role        tinyint unsigned not null,

    primary key (id_user_douban, id_role)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣用户-电影
create table user_douban_to_movie_douban
(
    id_user_douban  int unsigned    not null,
    id_movie_douban bigint unsigned not null,
    # 用户对电影的评分 0.0 ～ 10.0
    score           decimal(3, 1)   not null default 0.0,
    # 标记用户是否想看 0-未标记 1-已想看
    is_wish         tinyint(1)      not null default 0,
    # 标记用户是否看过 0-未标记 1-已看过
    is_seen         tinyint(1)      not null default 0,

    primary key (id_user_douban, id_movie_douban, score desc)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣用户-短评
create table user_douban_to_comment_movie_douban
(
    id_user_douban          int unsigned    not null,
    id_comment_movie_douban bigint unsigned not null,

    primary key (id_user_douban, id_comment_movie_douban)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 用户-影评
create table user_douban_to_review_movie_douban
(
    id_user_douban         int unsigned    not null,
    id_review_movie_douban bigint unsigned not null,

    primary key (id_user_douban, id_review_movie_douban)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 豆瓣电影经典台词-用户
create table user_douban_to_classic_douban
(
    id_user_douban    int unsigned    not null,
    id_classic_douban bigint unsigned not null,
    # 豆瓣用户收录时间
    record_datetime   datetime,
    # 豆瓣用户评价
    description       varchar(1000)   not null default '',

    primary key (id_user_douban, id_classic_douban),
    index (record_datetime)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 用户 end ========================================================================================

# 资源 start ========================================================================================

# 电影资源相关 ---------------------------------------------------------------------------------

# 1.电影资源基础表---------------------------------------

# 电影资源网站 
create table website_resource
(
    id          smallint unsigned not null auto_increment primary key,
    # 网站中文名
    name_zh     varchar(255)      not null default '',
    # 网站是否为正版合法网站 0-否 1-是
    is_legal    tinyint(1)        not null default 0,
    # 网站官网地址
    website_src varchar(255)      not null default '',

    index (name_zh)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into website_resource(id, name_zh)
values (1, '未知');


# 电影资源类型 (免费播放、vip免费播放、磁力链接...)
create table type_resource
(
    id      smallint unsigned not null auto_increment primary key,
    # 资源类型中文名
    name_zh varchar(255)      not null default '',

    index (name_zh)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into type_resource
values (1, '未知');

# 电影资源
create table resource_movie
(
    id                  bigint unsigned   not null auto_increment primary key,
    # 资源对应的电影
    id_movie_douban     bigint unsigned   not null default 0,
    # 资源所属网站
    id_website_resource smallint unsigned not null default 1,
    # 资源所属类型
    id_type_resource    smallint unsigned not null default 1,
    # 资源链接
    url_resource        varchar(1000)     not null default '',
    # 资源中文名
    name_zh             varchar(255)      not null default '',

    index (id_movie_douban),
    index (id_website_resource),
    index (id_type_resource),
    unique (url_resource(100)),
    index (name_zh)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into resource_movie(id, name_zh)
values (1, '未知');

# 2.电影资源关系表---------------------------------------


# 图片资源相关 ---------------------------------------------------------------------------------

# 1.图片资源基础表---------------------------------------

/*
 豆瓣电影图片链接格式: https://img3.doubanio.com/view/photo/l/public/p2567198874.webp
 域名： img1、img3、img9
 图片类型: l、m、sqxs、s_ratio_poster

 */

# 图片（豆瓣电影-电影图片）
create table image_movie_douban
(
    id              bigint unsigned  not null primary key,
    # 豆瓣电影ID
    id_movie_douban bigint unsigned  not null default 0,
    # 序号
    sort            tinyint unsigned not null default 0,
    # 长
    length          int unsigned     not null default 0,
    # 宽
    width           int unsigned     not null default 0,

    index (id_movie_douban),
    index (sort asc),
    index (length desc)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 图片（豆瓣电影-影人图片）
create table image_celebrity_douban
(
    id                  bigint unsigned  not null primary key,
    # 豆瓣影人ID
    id_celebrity_douban bigint unsigned  not null default 0,
    # 序号
    sort                tinyint unsigned not null default 0,
    # 长
    length              int unsigned     not null default 0,
    # 宽
    width               int unsigned     not null default 0,

    index (id_celebrity_douban),
    index (sort asc),
    index (length desc)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 图片（场景地点-地点图片）
create table image_place_scene
(
    id             bigint unsigned not null auto_increment primary key,
    # 场景地点ID
    id_place_scene bigint unsigned not null default 0,
    # 图片链接
    url_image      varchar(1000)   not null default '',
    # 图片描述
    description    varchar(255)    not null default '',

    index (id_place_scene)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 图片（场景-场景详情的剧照）
create table image_scene_detail
(
    id              bigint unsigned not null auto_increment primary key,
    # 场景详情ID
    id_scene_detail bigint unsigned not null default 0,
    # 图片链接
    url_image       varchar(1000)   not null default '',

    index (id_scene_detail)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 2.图片资源关系表---------------------------------------

# 资源 end ========================================================================================

# 区域 start ========================================================================================

# 场景区域相关 ---------------------------------------------------------------------------------

# 1.地点区域基础表---------------------------------------

# 地点
create table place_scene
(
    id                 bigint unsigned   not null primary key,
    # 地点范围-洲-id
    id_continent_scene tinyint unsigned  not null default 0,
    # 地点范围-国家-id
    id_country_scene   smallint unsigned not null default 0,
    # 地点范围-州/省-id
    id_state_scene     int unsigned      not null default 0,
    # 地点范围-城市-id
    id_city_scene      int unsigned      not null default 0,

    # 经度
    longitude          decimal(11, 8)    not null default 0.00000000,
    # 纬度
    latitude           decimal(11, 8)    not null default 0.00000000,

    # 中文名
    name_zh            varchar(255)      not null default '',
    # 英文名
    name_en            varchar(255)      not null default '',
    # 其他语言名
    name_other         varchar(255)      not null default '',
    # 别名
    alias              varchar(255)      not null default '',
    # 中文地址
    address_zh         varchar(255)      not null default '',
    # 英文地址
    address_en         varchar(255)      not null default '',
    # 地点描述
    description        varchar(1000)     not null default '',
    # 区域中文
    area_zh            varchar(255)      not null default '',
    # 区域英文
    area_en            varchar(255)      not null default '',
    # 电话号码
    phone              varchar(255)      not null default '',
    # 地点海报图链接
    url_poster         varchar(1000)     not null default '',
    # 地点地球位置图链接
    url_earth          varchar(1000)     not null default '',
    # 地点卫星图链接
    url_satellite      varchar(1000)     not null default '',
    # 地点地图
    url_map            varchar(1000)     not null default '',

    index (id_continent_scene),
    index (id_country_scene),
    index (id_state_scene),
    index (id_city_scene),
    index (longitude),
    index (latitude)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into place_scene(id, name_zh, name_en)
values (0, '未知', 'unknown');

# 场景地点类型 (场景地点专属)
create table type_place_scene
(
    id      tinyint unsigned not null primary key,
    # 地点类型名称
    name_zh varchar(255)     not null default '',

    index (name_zh)
) ENGINE = InnoDB
  default charset = utf8mb4;

# 洲 (场景专属)
create table continent_scene
(
    id      tinyint unsigned not null primary key,
    # 洲中文名
    name_zh varchar(255)     not null default '',
    # 洲英文名
    name_en varchar(255)     not null default '',

    index (name_zh),
    index (name_en)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into continent_scene
values (0, '未知', 'unknown');

# 国家（场景专属）
create table country_scene
(
    id      smallint unsigned not null primary key,
    # 国家中文名
    name_zh varchar(255)      not null default '',
    # 国家英文名
    name_en varchar(255)      not null default '',

    index (name_zh),
    index (name_en)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into country_scene
values (0, '未知', 'unknown');

# 州/省(场景地点专属)
create table state_scene
(
    id      int unsigned not null primary key,
    # 州中文名
    name_zh varchar(255) not null default '',
    # 州英文名
    name_en varchar(255) not null default '',

    index (name_zh),
    index (name_en)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into state_scene
values (0, '未知', 'unknown');

# 城市(场景地点专属)
create table city_scene
(
    id      int unsigned not null primary key,
    # 城市中文名
    name_zh varchar(255) not null default '',
    # 城市英文名
    name_en varchar(255) not null default '',

    index (name_zh),
    index (name_en)
) ENGINE = InnoDB
  default charset = utf8mb4;
insert into city_scene
values (0, '未知', 'unknown');

# 2.地点区域关系表---------------------------------------

# 场景地点-场景地点类型
CREATE TABLE place_scene_to_type_place_scene
(
    id_place_scene      bigint unsigned  NOT NULL,
    id_type_place_scene tinyint unsigned NOT NULL,

    primary key (id_place_scene, id_type_place_scene)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

# 区域 end ========================================================================================

# 音乐 start ========================================================================================

# 1.网易云音乐基础表---------------------------------------

# 歌曲
CREATE TABLE song_netease
(
    id              bigint unsigned NOT NULL primary key,
    # 推荐搜索之歌曲所属豆瓣电影ID 默认 0 （即由歌单或专辑得出的单曲不给出豆瓣ID）
    id_movie_douban bigint unsigned not null default 0,
    # 歌曲中文名
    name_zh         varchar(255)    not null default '',

    index (id_movie_douban),
    index (name_zh)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;
insert into song_netease
values (0, 0, '');


# 用户
CREATE TABLE user_netease
(
    id      bigint unsigned NOT NULL primary key,
    # 用户中文名
    name_zh varchar(255)    not null default '',

    index (name_zh)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;
insert into user_netease(id, name_zh)
values (0, '未知');

# 歌单
CREATE TABLE playlist_netease
(
    id              bigint unsigned   NOT NULL primary key,
    # 推荐搜索之歌单所属豆瓣电影ID
    id_movie_douban bigint unsigned   not null default 0,
    # 歌单中文名
    name_zh         varchar(255)      not null default '',
    # 歌单歌曲总数
    total           smallint unsigned NOT NULL default 0,
    # 歌单播放次数
    play_count      int unsigned      NOT NULL default 0,
    # 封面图片
    url_cover       varchar(1000)     not null default '',
    # 歌单描述
    description     varchar(1000)     not null default '',

    index (id_movie_douban),
    index (name_zh),
    index (play_count desc)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

# 专辑
CREATE TABLE album_netease
(
    id              bigint unsigned   NOT NULL primary key,
    # 推荐搜索之专辑所属豆瓣电影ID
    id_movie_douban bigint unsigned   not null default 0,
    # 专辑中文名
    name_zh         varchar(255)      not null default '',
    # 专辑歌曲总数
    total           smallint unsigned NOT NULL default 0,

    index (id_movie_douban),
    index (name_zh),
    index (total)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

# 评论 (默认热评)
CREATE TABLE comment_netease
(
    id              bigint unsigned NOT NULL primary key,
    # 歌曲ID
    id_song_netease bigint unsigned not null default 0,
    # 用户ID
    id_user_netease bigint unsigned not null default 0,
    # 创建时间
    create_datetime datetime,
    # 评论内容
    content         varchar(1000)   NOT NULL default '',
    # 赞同数
    agree_vote      int unsigned    NOT NULL default 0,

    index (id_song_netease),
    index (id_user_netease),
    index (create_datetime desc),
    index (vote desc)
) ENGINE = INNODB
  DEFAULT CHARSET = UTF8MB4;



# 1.网易云音乐关系表---------------------------------------


# 豆瓣电影-网易云音乐
CREATE TABLE movie_douban_to_netease
(
    id_movie_douban bigint unsigned  NOT NULL,
    id_netease      bigint unsigned  NOT NULL,
    # 决定id_netease为 1:歌曲 2:歌单 3:专辑
    type_netease    tinyint unsigned not null default 0,

    primary key (id_movie_douban, id_netease, type_netease)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

# 歌曲-歌单
CREATE TABLE song_netease_to_playlist_netease
(
    id_song_netease     bigint unsigned     NOT NULL,
    id_playlist_netease bigint unsigned     NOT NULL,
    # 歌曲在歌单中的流行度 0-100
    song_pop            tinyint(3) unsigned NOT NULL default 0,

    primary key (id_song_netease, id_playlist_netease),
    index (song_pop desc)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;

# 歌曲-专辑
CREATE TABLE song_netease_to_album_netease
(
    id_song_netease  bigint unsigned NOT NULL,
    id_album_netease bigint unsigned NOT NULL,

    primary key (id_song_netease, id_album_netease)
) ENGINE = InnoDB
  DEFAULT CHARSET = utf8mb4;


# 音乐 end ========================================================================================

# 表初始化 start ========================================================================================


# 场景地点类型
insert into type_place_scene(id, name_zh)
values (100, '未知'),
       (0, '旅游景点'),
       (1, '历史建筑'),
       (2, '餐饮'),
       (3, '商铺'),
       (4, '自然风光'),
       (5, '民居'),
       (6, '酒店'),
       (7, '地标'),
       (8, '宗教场所'),
       (9, '街道'),
       (10, '影视基地'),
       (11, '公园'),
       (12, '演艺场所'),
       (13, '展馆'),
       (14, '交通站'),
       (15, '商用建筑'),
       (16, '广场'),
       (17, '政府机关'),
       (18, '医疗机构'),
       (19, ''),
       (20, '工厂'),
       (21, '体育场馆'),
       (22, '金融机构'),
       (23, '港口'),
       (24, '社会福利机构'),
       (25, '墓地'),
       (26, '学校');

insert ignore into type_video
values (1, '未知', 'unknown'),
       (2, '电影', 'movie'),
       (3, '电视剧', 'tv series'),
       (4, '短片', 'short'),
       # 来自IMDB
       (5, '', 'tv mini series'),
       (6, '', 'tv short'),
       (7, '', 'tv special'),
       (8, '', 'tvMovie'),
       (9, '', 'video'),
       (10, '', 'video game');

insert into website_resource
values (2, '爱奇艺视频', 1, 'https://www.iqiyi.com'),
       (3, '腾讯视频', 1, 'https://v.qq.com'),
       (4, '哔哩哔哩', 1, 'https://www.bilibili.com'),
       (5, '搜狐视频', 1, 'https://tv.sohu.com'),
       (6, '优酷视频', 1, 'https://www.youku.com'),
       (7, '1905电影网', 1, 'https://vip.1905.com'),
       (8, '芒果TV', 1, 'https://www.mgtv.com'),
       (101, '电影天堂', 0, '');

insert into type_resource
values (2, '免费观看'),
       (3, 'VIP免费观看'),
       (4, '单片付费'),
       (5, '用劵/单片付费'),
       (11, '磁力链接'),
       (12, '迅雷链接');


insert into profession
values (1, '未知',
        'unknown'),
       (2, '导演', 'director'),
       (3, '编剧', 'writer'),
       (4, '主演', 'starring'),
       # 来自IMDB
       (5, '男演员', 'actor'),
       (6, '女演员', 'actress'),
       (7, '', 'archive_footage'),
       (8, '', 'archive_sound'),
       (9, '', 'cinematographer'),
       (10, '', 'composer'),
       (11, '', 'editor'),
       (12, '', 'producer'),
       (13, '', 'production_designer'),
       (14, '', 'self');

insert into type_movie
values (1, '未知'),
       (2, '剧情'),
       (3, '喜剧'),
       (4, '爱情'),
       (5, '动作'),
       (6, '惊悚'),
       (7, '动画'),
       (8, '犯罪'),
       (9, '纪录片'),
       (10, '短片'),
       (11, '恐怖'),
       (12, '悬疑'),
       (13, '科幻'),
       (14, '冒险'),
       (15, '奇幻'),
       (16, '家庭'),
       (17, '战争'),
       (18, '历史'),
       (19, '传记'),
       (20, '音乐'),
       (21, '同性'),
       (22, '古装'),
       (23, '歌舞'),
       (24, '运动'),
       (25, '情色'),
       (26, '儿童'),
       (27, '武侠'),
       (28, '西部'),
       (29, '真人秀'),
       (30, '黑色电影'),
       (31, '灾难'),
       (32, '脱口秀'),
       (33, '舞台艺术'),
       (34, '戏曲'),
       (35, '鬼怪');


# 测试数据
insert into movie_imdb(id, start_year)
values (23071, 1932),
       (127917, 1998),
       (2193456, 2013),
       (1239228, 2008),
       (120731, 1998),
       (11162126, 2019),
       (9243946, 2019),
       (9789686, 2019),
       (8739752, 2019);
insert into celebrity_imdb(id)
values (4082296),
       (0451148);
insert into movie_douban(id)
values (27119724),
       (30242710),
       (26786669),
       (26794435);
insert into celebrity_douban(id)
values (1018983),
       (1005822),
       (1025176),
       (1036390),
       (1047979);


# 表初始化 end ========================================================================================

# 外键关系 start ========================================================================================


# /*

alter table movie_imdb
    add foreign key (id_type_video) references type_video (id);
alter table movie_imdb_to_type_movie
    add foreign key (id_movie_imdb) references movie_imdb (id);
alter table movie_imdb_to_type_movie
    add foreign key (id_type_movie) references type_movie (id);
alter table movie_douban
    add foreign key (id_movie_imdb) references movie_imdb (id);
alter table movie_douban
    add foreign key (id_type_video) references type_video (id);
alter table alias_movie_douban
    add foreign key (id_movie_douban) references movie_douban (id);
alter table trailer_movie_douban
    add foreign key (id_movie_douban) references movie_douban (id);
alter table classic_douban
    add foreign key (id_movie_douban) references movie_douban (id);
alter table comment_movie_douban
    add foreign key (id_movie_douban) references movie_douban (id);
alter table comment_movie_douban
    add foreign key (id_user_douban) references user_douban (id);
alter table rate_movie_douban
    add foreign key (id) references movie_douban (id);
alter table movie_douban_to_type_movie
    add foreign key (id_movie_douban) references movie_douban (id);
alter table movie_douban_to_type_movie
    add foreign key (id_type_movie) references type_movie (id);
alter table movie_douban_to_award_movie
    add foreign key (id_movie_douban) references movie_douban (id);
alter table movie_douban_to_award_movie
    add foreign key (id_award_movie) references award_movie (id);
alter table movie_douban_to_award_movie
    add foreign key (id_celebrity_douban) references celebrity_douban (id);
alter table tag_movie
    add foreign key (id_movie_douban) references movie_douban (id);
alter table movie_douban_to_review_movie_douban
    add foreign key (id_movie_douban) references movie_douban (id);
alter table movie_douban_to_review_movie_douban
    add foreign key (id_review_movie_douban) references review_movie_douban (id);
alter table rate_imdb
    add foreign key (id) references movie_imdb (id);
alter table movie_imdb_to_celebrity_imdb
    add foreign key (id_movie_imdb) references movie_imdb (id);
alter table movie_imdb_to_celebrity_imdb
    add foreign key (id_celebrity_imdb) references celebrity_imdb (id);
alter table movie_imdb_to_celebrity_imdb
    add foreign key (id_profession) references profession (id);
alter table celebrity_douban
    add foreign key (id_celebrity_imdb) references celebrity_imdb (id);
alter table alias_celebrity_douban
    add foreign key (id_celebrity_douban) references celebrity_douban (id);
alter table movie_douban_to_celebrity_douban
    add foreign key (id_movie_douban) references movie_douban (id);
alter table movie_douban_to_celebrity_douban
    add foreign key (id_celebrity_douban) references celebrity_douban (id);
alter table movie_douban_to_celebrity_douban
    add foreign key (id_profession) references profession (id);
alter table celebrity_douban_to_classic
    add foreign key (id_celebrity_douban) references celebrity_douban (id);
alter table celebrity_douban_to_classic
    add foreign key (id_classic_douban) references classic_douban (id);
alter table movie_scene
    add foreign key (id_movie_douban) references movie_douban (id);
alter table celebrity_scene
    add foreign key (id_celebrity_douban) references celebrity_douban (id);
alter table scene
    add foreign key (id_movie_scene) references movie_scene (id);
alter table scene
    add foreign key (id_place_scene) references place_scene (id);
alter table scene_detail
    add foreign key (id_movie_scene) references movie_scene (id);
alter table scene_detail
    add foreign key (id_scene) references scene (id);
alter table user_douban_to_role
    add foreign key (id_user_douban) references user_douban (id);
alter table movie_scene_to_celebrity_scene
    add foreign key (id_movie_scene) references movie_scene (id);
alter table movie_scene_to_celebrity_scene
    add foreign key (id_celebrity_scene) references celebrity_scene (id);
alter table scene_detail_to_celebrity_scene
    add foreign key (id_scene_detail) references scene_detail (id);
alter table scene_detail_to_celebrity_scene
    add foreign key (id_celebrity_scene) references celebrity_scene (id);
alter table user_douban_to_role
    add foreign key (id_role) references role (id);
alter table role_to_permission
    add foreign key (id_role) references role (id);
alter table role_to_permission
    add foreign key (id_permission) references permission (id);
alter table user_douban_to_movie_douban
    add foreign key (id_user_douban) references user_douban (id);
alter table user_douban_to_movie_douban
    add foreign key (id_movie_douban) references movie_douban (id);
alter table user_douban_to_comment_movie_douban
    add foreign key (id_user_douban) references user_douban (id);
alter table user_douban_to_comment_movie_douban
    add foreign key (id_comment_movie_douban) references comment_movie_douban (id);
alter table user_douban_to_review_movie_douban
    add foreign key (id_user_douban) references user_douban (id);
alter table user_douban_to_review_movie_douban
    add foreign key (id_review_movie_douban) references review_movie_douban (id);
alter table user_douban_to_classic_douban
    add foreign key (id_user_douban) references user_douban (id);
alter table user_douban_to_classic_douban
    add foreign key (id_classic_douban) references classic_douban (id);
alter table resource_movie
    add foreign key (id_movie_douban) references movie_douban (id);
alter table resource_movie
    add foreign key (id_website_resource) references website_resource (id);
alter table resource_movie
    add foreign key (id_type_resource) references type_resource (id);
alter table image_celebrity_douban
    add foreign key (id_celebrity_douban) references celebrity_douban (id);
alter table image_movie_douban
    add foreign key (id_movie_douban) references movie_douban (id);
alter table image_place_scene
    add foreign key (id_place_scene) references place_scene (id);
alter table image_scene_detail
    add foreign key (id_scene_detail) references scene_detail (id);
alter table place_scene_to_type_place_scene
    add foreign key (id_place_scene) references place_scene (id);
alter table place_scene_to_type_place_scene
    add foreign key (id_type_place_scene) references type_place_scene (id);
alter table place_scene
    add foreign key (id_continent_scene) references continent_scene (id);
alter table place_scene
    add foreign key (id_country_scene) references country_scene (id);
alter table place_scene
    add foreign key (id_state_scene) references state_scene (id);
alter table place_scene
    add foreign key (id_city_scene) references city_scene (id);
alter table playlist_to_tag_netease
    add foreign key (id_playlist) references playlist (id);
alter table playlist_to_tag_netease
    add foreign key (id_tag_netease) references tag_netease (id);
alter table playlist
    add foreign key (id_movie_douban) references movie_douban (id);
alter table album
    add foreign key (id_movie_douban) references movie_douban (id);
alter table song_netease
    add foreign key (id_movie_douban) references movie_douban (id);
alter table song_to_tag_netease
    add foreign key (id_song) references song_netease (id);
alter table song_to_tag_netease
    add foreign key (id_tag_netease) references tag_netease (id);
alter table song_to_playlist
    add foreign key (id_song) references song_netease (id);
alter table song_to_playlist
    add foreign key (id_playlist) references playlist (id);
alter table song_to_album
    add foreign key (id_song) references song_netease (id);
alter table song_to_album
    add foreign key (id_album) references album (id);
alter table user_netease_to_comment_netease
    add foreign key (id_user_netease) references user_netease (id);
alter table user_netease_to_comment_netease
    add foreign key (id_comment_netease) references comment_netease (id);
alter table song_to_comment_netease
    add foreign key (id_song) references song_netease (id);
alter table song_to_comment_netease
    add foreign key (id_comment_netease) references comment_netease (id);
alter table song_to_singer
    add foreign key (id_song) references song_netease (id);
alter table song_to_singer
    add foreign key (id_singer) references singer (id);
alter table album_to_singer
    add foreign key (id_album) references album (id);
alter table album_to_singer
    add foreign key (id_singer) references singer (id);

*/

# 外键关系 end ========================================================================================

# IMDB转换 end ========================================================================================

/*
 # 人物
 insert into celebrity_imdb(id,name_en,birth_year,death_year)
select nconst,primaryName,ifnull(birthYear,0),ifnull(deathYear,0)
from name_basics;


 # 电影
 insert into type_video(name_en)
select titleType from title_basics where titleType!='episode' group by titleType;

insert into movie_imdb(id,id_type_video,start_year,end_year,is_adult,name_en,name_origin,runtime)
select tconst,
(select id from type_video where name_en=titleType),
ifnull(startYear,0),ifnull(endYear,0),isAdult,
if(isnull(primaryTitle)=0 and char_length(primaryTitle)<255,primaryTitle,''),
if(isnull(originalTitle)=0 and char_length(originalTitle)<255,originalTitle,''),
if(isnull(runtimeMinutes)=0 and runtimeMinutes<60000,runtimeMinutes,0)
from title_basics where titleType!='episode';


 # 评分
 insert into rate_imdb(id,imdb_score,imdb_vote)
select tconst,averageRating,numVotes
from title_ratings where title_ratings.tconst in (select id from movie_imdb);


 # 电影-人物
 insert into profession(name_en,id)
select category,count(*)%199  from title_principals group by category;

insert into movie_imdb_to_celebrity_imdb(id_movie_imdb,id_celebrity_imdb,id_profession,description)
select tconst,nconst,
(select id from profession where name_en=category),
ifnull(job,'')
from title_principals inner join movie_imdb on id=tconst
on duplicate key update id_movie_imdb=tconst;


 # 豆瓣电影1.0中的movie表中的ID转换到2.0的movie_douban表中



 */

# IMDB转换 end ========================================================================================
