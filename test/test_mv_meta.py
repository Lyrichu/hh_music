# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 17:50

from unittest import TestCase

from api.kuwo_music_api import *
from music_meta.mv_meta import Mv

import json


class AlbumTest(TestCase):

    def test_from_dict(self):
        artist_id = 89199
        rsp = get_kuwo_all_singer_mv(artist_id)
        mv = Mv.from_dict(rsp["data"]["mvlist"][0])
        print(mv)

    def test_from_json(self):
        artist_id = 89199
        rsp = get_kuwo_all_singer_mv(artist_id)
        mv_json_str = json.dumps(rsp["data"]["mvlist"][5], ensure_ascii=False)
        mv = Mv.from_json(mv_json_str)
        print(mv)

    def test_to_dict(self):
        artist_id = 89199
        rsp = get_kuwo_all_singer_mv(artist_id)
        mv = Mv.from_dict(rsp["data"]["mvlist"][3])
        print(mv.to_dict())
