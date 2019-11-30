# !/usr/bin/env python
# -*- coding: utf-8 -*-

# author: humingk
# ----------------------
import scrapy


class MovieNetease(scrapy.Item):
    id_movie_douban = scrapy.Field()
    id_netease = scrapy.Field()
    netease_type = scrapy.Field()
    sort = scrapy.Field()


class SongNetease(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()


class PlaylistNetease(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()
    total = scrapy.Field()
    play_count = scrapy.Field()
    url_cover = scrapy.Field()
    description = scrapy.Field()


class AlbumNetease(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()
    total = scrapy.Field()
    url_cover = scrapy.Field()


class SongNeteaseToPlaylistNetease(scrapy.Item):
    id_song_netease = scrapy.Field()
    id_playlist_netease = scrapy.Field()
    song_pop = scrapy.Field()


class SongNeteaseToAlbumNetease(scrapy.Item):
    id_song_netease = scrapy.Field()
    id_album_netease = scrapy.Field()


class CommentNetease(scrapy.Item):
    id = scrapy.Field()
    id_song_netease = scrapy.Field()
    id_user_netease = scrapy.Field()
    create_datetime = scrapy.Field()
    content = scrapy.Field()
    agree_vote = scrapy.Field()


class UserNetease(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()


class ArtistNetease(scrapy.Item):
    id = scrapy.Field()
    name_zh = scrapy.Field()
    url_portrait = scrapy.Field()


class ArtistNeteaseToAlbumNetease(scrapy.Item):
    id_artist_netease = scrapy.Field()
    id_album_netease = scrapy.Field()


class ArtistNeteaseToSongNetease(scrapy.Item):
    id_artist_netease = scrapy.Field()
    id_song_netease = scrapy.Field()
