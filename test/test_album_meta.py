# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 17:26
from unittest import TestCase

from api.kuwo_music_api import *
from music_meta.album_meta import Album

import json


class AlbumTest(TestCase):

    def test_from_dict(self):
        artist_id = 89199
        rsp = get_kuwo_all_singer_album(artist_id)
        print(rsp)
        album = Album.from_dict(rsp["data"]["albumList"][0])
        print(album)

    def test_from_json(self):
        artist_id = 89199
        rsp = get_kuwo_all_singer_album(artist_id)
        album_json_str = json.dumps(rsp["data"]["albumList"][5], ensure_ascii=False)
        album = Album.from_json(album_json_str)
        print(album)

    def test_to_dict(self):
        artist_id = 89199
        rsp = get_kuwo_all_singer_album(artist_id)
        album = Album.from_dict(rsp["data"]["albumList"][3])
        print(album.to_dict())
