# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 22:54

from unittest import TestCase

from api.kuwo_music_api import *
from music_meta.singer_meta import Singer

import json


class SingerTest(TestCase):

    def test_from_dict(self):
        singer_name = "潘玮柏"
        rsp = get_kuwo_artist_by_search_keyword(singer_name)
        singer_data = rsp["data"]["list"][0]
        singer = Singer.from_dict(singer_data)
        print(singer)

    def test_from_json(self):
        singer_name = "潘玮柏"
        rsp = get_kuwo_artist_by_search_keyword(singer_name)
        singer_data = rsp["data"]["list"][0]
        sing_json = json.dumps(singer_data,ensure_ascii=False)
        singer = Singer.from_json(sing_json)
        print(singer)

    def test_to_dict(self):
        singer_name = "周杰伦"
        rsp = get_kuwo_artist_by_search_keyword(singer_name)
        singer_data = rsp["data"]["list"][0]
        singer = Singer.from_dict(singer_data)
        print(singer.to_dict())
