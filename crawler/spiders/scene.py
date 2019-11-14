# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import json
from scrapy_redis.spiders import RedisSpider
from crawler.configs import scene as config
from crawler.items.scene import *


class SceneSpider(RedisSpider):
    """
    关于电影的场景

    """

    name = 'scene'
    # start_url存放容器改为redis list
    redis_key = 'scene:start_urls'
    allowed_domains = ['api.mocation.cc']

    def start_requests(self):
        """
        爬取电影列表总数

        :return:
        """
        yield scrapy.Request(url=config.URL_MOVIE_LIST + '11111', callback=self.parse)

    def parse(self, response):
        """
        解析电影列表总数

        :param response:
        :return:
        """
        content = json.loads(response.text)
        if content['data'] and content['data']['total']:
            total = content['data']['total']
            self.logger.info('prepare to get movie list , total:{}'.format(total))
            # 请求电影列表的每一页
            for page in range(int(total / config.NUM_MOVIE_LIST) + 1):
                yield scrapy.Request(url='{}{}'.format(config.URL_MOVIE_LIST, page),
                                     callback=self.parse_movie_list)
                # ----------------------------------------------------------------------------------------------------------
                break
        else:
            self.logger.error('get movie list failed')
            return

    def parse_movie_list(self, response):
        """
        解析电影列表

        :param response:
        :return:
        """
        content = json.loads(response.text)
        if content['data'] and content['data']['movies']:
            for movie in content['data']['movies']:
                # 请求电影列表中的电影
                yield scrapy.Request(url='{}{}'.format(config.URL_MOVIE, movie['id']),
                                     callback=self.parse_movie)
                # ---------------------------------------------------------------------------------------------------------
                count = 0
                for place in movie['placeIds']:
                    # 请求电影中的地点
                    yield scrapy.Request(url='{}{}'.format(config.URL_PLACE, place),
                                         callback=self.parse_place)
                # ---------------------------------------------------------------------------------------------------------
                count += 1
                if count < 5:
                    continue
                elif count > 10:
                    break
            self.logger.info(
                'get movie list success ,page:{},total:{}'.format(response.url.split('=')[-1],
                                                                  content['data']['total']))
        else:
            self.logger.warning(
                'get movie list failed ,page:{},total:{}'.format(response.url.split('=')[-1], content['data']['total']))

    def parse_movie(self, response):
        """
        解析电影详情

        :param response:
        :return:
        """
        content = json.loads(response.text)
        if content['data'] and content['data']['movie']:
            data = content['data']['movie']
            item_movie = MovieScene()
            item_movie['id'] = data['id']
            item_movie['name_zh'] = data['cname']
            item_movie['name_en'] = data['ename']
            item_movie['start_year'] = data['year']
            item_movie['description'] = data['overview']
            item_movie['url_map'] = data['staticMapUrl']
            self.logger.info('get movie success, id:{},name:{}'.format(item_movie['id'], item_movie['name_zh']))
            yield item_movie
            # 场景
            for plot in data['plots']:
                item_scene = Scene()
                item_scene['id'] = plot['sceneId']
                item_scene['id_movie_scene'] = item_movie['id']
                item_scene['id_place_scene'] = plot['placeId']
                item_scene['name_zh'] = plot['sceneName']
                item_scene['happen_time'] = plot['position']
                self.logger.info('get scene success, id:{},name:{}'.format(item_scene['id'], item_scene['name_zh']))
                yield item_scene
        else:
            self.logger.warning('get movie failed,possible id：{}'.format(response.url.split('/')[-1]))

    def parse_place(self, response):
        """
        解析地点详情

        :param response:
        :return:
        """
        content = json.loads(response.text)
        if content['data'] and content['data']['place']:
            data = content['data']['place']
            item_place = PlaceScene()
            item_place['id'] = data['id']
            item_place['id_continent_scene'] = data['level0Id']
            item_place['id_country_scene'] = data['level1Id']
            item_place['id_state_scene'] = data['level2Id']
            item_place['id_city_scene'] = data['level3Id']
            item_place['longitude'] = data['lat']
            item_place['latitude'] = data['lng']
            item_place['name_zh'] = data['cname']
            item_place['name_en'] = data['ename']
            item_place['name_other'] = data['oname']
            item_place['alias'] = data['alias']
            item_place['address_zh'] = data['caddress']
            item_place['address_en'] = data['eaddress']
            item_place['description'] = data['description']
            item_place['area_zh'] = data['areaCname']
            item_place['area_en'] = data['areaEname']
            item_place['phone'] = data['phone']
            item_place['url_poster'] = data['coverPath']
            item_place['url_earth'] = data['mapPath']
            item_place['url_satellite'] = data['satellitePath']
            item_place['url_map'] = data['staticMapUrl']
            self.logger.info('get place success, id:{},name:{}'.format(item_place['id'], item_place['name_zh']))
            yield item_place
            # 场景详情
            for scene in data['scenes']:
                for detail in scene['details']:
                    item_scene_detail = SceneDetail()
                    item_scene_detail['id'] = detail['id']
                    item_scene_detail['id_scene'] = detail['sceneId']
                    item_scene_detail['id_movie_scene'] = scene['movieId']
                    item_scene_detail['happen_time'] = detail['position']
                    item_scene_detail['description'] = detail['description']
                    yield item_scene_detail
                    # 场景详情的人物
                    if detail['persons']:
                        for person in detail['persons']:
                            item_celebrity = CelebrityScene()
                            item_celebrity['id'] = person['id']
                            item_celebrity['name_zh'] = person['cname']
                            item_celebrity['name_en'] = person['ename']
                            yield item_celebrity
                            # 场景详情-人物 对应关系
                            item_celebrity_to_scene_detail = SceneDetailToCelebrityScene()
                            item_celebrity_to_scene_detail['id_celebrity_scene'] = item_celebrity['id']
                            item_celebrity_to_scene_detail['id_scene_detail'] = item_scene_detail['id']
                            yield item_celebrity_to_scene_detail
                    # 场景详情的剧照图
                    for still in detail['stills']:
                        item_image_scene_detail = ImageSceneDetail()
                        item_image_scene_detail['id_scene_detail'] = item_scene_detail['id']
                        item_image_scene_detail['url_image'] = still['picPath']
                        yield item_image_scene_detail

            # 地点实景图
            for pic in data['realGraphics']:
                item_image_place = ImagePlaceScene()
                item_image_place['id_place_scene'] = item_place['id']
                item_image_place['url_image'] = pic['picPath']
                item_image_place['description'] = pic['description']
                yield item_image_place
            # 地点类型
            for type in data['categories']:
                item_type = PlaceSceneToTypePlaceScene()
                item_type['id_place_scene'] = item_place['id']
                item_type['id_type_place_scene'] = type
                yield item_type
            # 地点范围
            item_continent = ContinentScene()
            item_continent['id'] = item_place['id_continent_scene']
            item_continent['name_zh'] = data['level0Cname']
            item_continent['name_en'] = data['level0Ename']
            yield item_continent
            item_country = CountryScene()
            item_country['id'] = item_place['id_country_scene']
            item_country['name_zh'] = data['level1Cname']
            item_country['name_en'] = data['level1Ename']
            yield item_country
            item_state = StateScene()
            item_state['id'] = item_place['id_state_scene']
            item_state['name_zh'] = data['level2Cname']
            item_state['name_en'] = data['level2Ename']
            yield item_state
            item_city = CityScene()
            item_city['id'] = item_place['id_city_scene']
            item_city['name_zh'] = data['level3Cname']
            item_city['name_en'] = data['level3Ename']
            yield item_city
        else:
            self.logger.warning('get place failed,possible id：{}'.format(response.url.split('/')[-1]))
