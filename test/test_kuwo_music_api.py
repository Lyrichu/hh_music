# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/27 14:06
from unittest import TestCase

from api.kuwo_music_api import *
from const.kuwo_api_constants import *


class KuwoMusicApiTest(TestCase):

    def test_get_kuwo_music_play_url(self):
        mid1 = 162457325
        br1 = KuwoMusicBr.BR_192KMP3.value
        rsp1 = get_kuwo_music_play_url(mid1, br1)
        self.assertNotEqual(200, rsp1["code"])

        mid2 = 235882595
        br2 = KuwoMusicBr.BR_128KMP3.value
        rsp2 = get_kuwo_music_play_url(mid2, br2)
        self.assertEqual(200, rsp2["code"])

    def test_get_kuwo_mv_play_url(self):
        mid = 235882595
        rsp = get_kuwo_mv_play_url(mid)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_music_lyric(self):
        mid = 235882595
        rsp = get_kuwo_music_lyric(mid)
        assert "data" in rsp

    def test_get_kuwo_music_by_search(self):
        key = "我记得"
        pn = 2
        rn = 15
        rsp = get_kuwo_music_by_search(key=key, pn=pn, rn=rn)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_music_search_hint(self):
        key = "我记得"
        pn = 3
        rn = 20
        rsp = get_kuwo_music_search_hint(key=key, pn=pn, rn=rn)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_music_by_search_keyword(self):
        key = "我记得"
        pn = 1
        rn = 30
        rsp = get_kuwo_music_by_search_keyword(key=key, pn=pn, rn=rn)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_album_by_search_keyword(self):
        key = "十二新作"
        pn = 2
        rn = 15
        rsp = get_kuwo_album_by_search_keyword(key=key, pn=pn, rn=rn)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_mv_by_search_keyword(self):
        key = "流沙"
        pn = 1
        rn = 15
        rsp = get_kuwo_mv_by_search_keyword(key=key, pn=pn, rn=rn)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_play_list_by_search_keyword(self):
        key = "欧美流行"
        pn = 2
        rn = 20
        rsp = get_kuwo_play_list_by_search_keyword(key=key, pn=pn, rn=rn)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_artist_by_search_keyword(self):
        key = "周深"
        pn = 1
        rn = 10
        rsp = get_kuwo_artist_by_search_keyword(key=key, pn=pn, rn=rn)
        self.assertEqual(200, rsp["code"])
        print(rsp)

    def test_get_kuwo_banner(self):
        rsp = get_kuwo_banner()
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_comment(self):
        sid = 9066675
        rsp1 = get_kuwo_comment(sid)
        self.assertEqual("ok", rsp1["result"])

        rsp2 = get_kuwo_comment(sid, comment_type=KuwoMusicCommentType.NEW_COMMENT.value)
        self.assertEqual("ok", rsp2["result"])

    def test_get_kuwo_rec_play_list(self):
        rsp = get_kuwo_rec_play_list()
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_play_list_music(self):
        pid = 1082685104
        rsp = get_kuwo_play_list_music(pid)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_default_play_list(self):
        rsp = get_kuwo_default_play_list()
        self.assertEqual(200, rsp["code"])
        self.assertEqual(30, len(rsp["data"]["data"]))

    def test_get_kuwo_album_play_list(self):
        album_id = 434604  # 吉姆餐厅
        rsp = get_kuwo_album_play_list(album_id)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_play_list_tag(self):
        rsp = get_kuwo_play_list_tag()
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_play_list_with_tag(self):
        pid = 2189
        rsp = get_kuwo_play_list_with_tag(pid)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_all_singer(self):
        rsp = get_kuwo_all_singer(KuwoMusicAllSingerCategory.CHINESE_FEMALE.value, prefix='Z')
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_all_singer_music(self):
        artist_id = 89199
        rsp = get_kuwo_all_singer_music(artist_id)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_all_singer_album(self):
        artist_id = 89199
        rsp = get_kuwo_all_singer_album(artist_id)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_all_singer_mv(self):
        artist_id = 89199
        rsp = get_kuwo_all_singer_mv(artist_id)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_music_info(self):
        mid = 235882595
        rsp = get_kuwo_music_info(mid)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_rank_list(self):
        rsp = get_kuwo_rank_list()
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_rank_list_music(self):
        bang_id = 17
        rsp = get_kuwo_rank_list_music(bang_id)
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_rec_rank_list(self):
        rsp = get_kuwo_rec_rank_list()
        self.assertEqual(200, rsp["code"])

    def test_get_kuwo_radio(self):
        rsp = get_kuwo_radio()
        self.assertEqual(200, rsp["code"])