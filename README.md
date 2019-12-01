# douban_movie_database
豆瓣电影Plus数据库,包括豆瓣电影、IMDB、网易云音乐、片场

## 项目框架图
...
## 数据库ER关系图
...
## 安装方式

### 基础配置

```shell
# 克隆到本地
git clone https://github.com/humingk/douban_movie_database

# pip配置依赖包
cd douban_movie_database
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# 配置数据库(MySQL)
mysql: create database movie;
sudo mysql -uroot -p movie < crawler/tools/movie.sql
```

### IMDB配置
参考[IMDB官方接口数据库转化为满足三范式的关系型数据库](https://humingk.github.io/mysql-imdb/)

```shell
# 配置数据库
mysql: create database imdb;

# tsv转换
s32imdbpy.py [IMDB压缩文件目录] mysql+pymysql://root:[MySQL密码]@localhost:3306/imdb

# 数据库转换 imdb => movie
# 参见博文代码
```

## 使用方式

```shell
用法：scrapy crawl [蜘蛛] [-a type=<种类>]

    search_douban               由豆瓣搜索/数据库匹配指定电影
        -a type=movie_imdb          由IMDB电影匹配获取豆瓣电影
        -a type=celebrity_imdb      由IMDB影人匹配获取豆瓣影人
        -a type=movie_scene         由豆瓣电影匹配对应场景电影
        -a type=celebrity_scene     由豆瓣影人匹配对应场景影人
        -a type=movie_resource      由豆瓣电影匹配对应资源电影
    
    movie_imdb                  由IMDB/豆瓣电影获取IMDB、烂番茄、MTC
    
    new_douban                  获取豆瓣最新上映电影
    
    movie_douban                获取豆瓣电影详情
    
    celebrity_douban            获取豆瓣影人详情
    
    comment_douban              获取豆瓣电影热门评论
    
    trailer_douban              获取豆瓣电影预告片
    
    image_douban                获取豆瓣电影/影人图片
        -a type=movie               获取豆瓣电影图片
        -a type=celebrity           获取豆瓣影人图片
    
    scene                       获取场景电影、地点
    
    search_netease              由豆瓣电影获取相关的网易云音乐
    
    playlist_netease            由歌单获取歌单详情
    
    album_netease               由专辑获取专辑详情
    
    comment_netease             由歌曲获取歌曲的热门评论
    
    dy2018_resource             获取电影天堂资源
        -a type=all                 所有资源
        -a type=new                 最新资源
        
    loldytt_resource            获取LOL电影天堂资源
        -a type=all                 所有资源
        -a type=new                 最新资源
    
    btbtdy_resource             获取BT电影天堂资源
        -a type=all                 所有资源
        -a type=new                 最新资源
    
    xl720_resource              获取迅雷电影天堂资源
        -a type=all                 所有资源
        -a type=new                 最新资源
    
    hao6v_resource              获取6V电影网资源
        -a type=all                 所有资源
        -a type=new                 最新资源
    
    goudaitv_resource           获取狗带TV资源
        -a type=all                 所有资源
        -a type=new                 最新资源
    
    zxzjs_resource              获取在线之家资源
        -a type=all                 所有资源
        -a type=new                 最新资源

```

## 数据来源

- [IMDB](https://www.imdb.com)
- [豆瓣电影](https://movie.douban.com)
- [网易云音乐](https://music.163.com)
- [片场](http://www.mocation.cc)
- [OMDB](http://www.omdbapi.com)
- [电影天堂](https://www.dy2018.com)
- [LOL电影天堂](https://www.loldytt.tv)
- [BT电影天堂](http://www.btbtdy.me)
- [迅雷电影天堂](https://www.xl720.com)
- [6V电影网](http://www.hao6v.com)
- [狗带TV](http://www.goodaitv.com)
- [在线之家](http://www.zxzjs.com)
