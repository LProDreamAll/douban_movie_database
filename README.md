# douban_movie_database
豆瓣电影Plus数据库持久化爬虫，包括 豆瓣电影、网易云音乐、片场、IMDB等

## 安装方式

```shell
# 克隆到本地
git clone https://github.com/humingk/douban_movie_database

# 配置依赖包
cd douban_movie_database
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple

# 配置数据库(MySQL)

...

```

## 使用方式

```shell
# 豆瓣电影
scrapy crawl movie_douban

# 豆瓣影人
scrapy crawl celebrity_douban

# 豆瓣图片
scrapy crawl image_douban -a type={}
- movie             电影图片
- celebrity         影人图片

# 豆瓣搜索
scrapy crawl search_douban -a type={}
- movie_imdb        根据imdb_ID获取豆瓣电影ID
- celebrity_imdb    根据imdb_ID获取豆瓣影人ID
- movie_scene       根据场景_名称获取豆瓣电影ID
- celebrity_scene   根据场景_名称获取豆瓣影人ID
- movie_resource    根据资源_名称获取豆瓣电影ID

# 电影场景
scrapy crawl scene

...

```