# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/22 23:36
"""
这里保存一些继承自 QThread/QRunnable 的 工作类
"""
import traceback

from PySide6.QtCore import QThread, Signal

from api.kuwo_music_api import *
from music_meta.album_meta import Album
from music_meta.music_meta import Music
from music_meta.mv_meta import Mv
from music_meta.singer_meta import Singer
from util.logs import LOGGER
from util.music_tools import search_kuwo_music_by_keywords


class SearchWorker(QThread):
    """
    音乐搜索的工作类
    """
    # (搜索总数,当前音乐列表)
    search_res = Signal(int, list)
    finished = Signal()

    def __init__(self, keyword):
        super().__init__()
        self.keyword = keyword

    def search_music(self, keyword):
        """
        根据关键词搜索音乐列表
        :param keyword:
        :return:
        """
        return search_kuwo_music_by_keywords(keyword)

    def run(self):
        # Call the search function here and get the result
        result = self.search_music(self.keyword)
        # Emit the signal when the search is finished
        self.search_res.emit(*result)


class SingerMusicWorker(QThread):
    """
    获取歌手的全部歌曲,可能需要分页加载以获取全部数据
    """
    singer_musics = Signal(list)
    total_musics = Signal(int)
    finished = Signal()

    def __init__(self, singer_id, pn=1, rn=30):
        """
        :param singer_id: 歌手id
        :param pn: 页数
        :param rn: 一页个数
        """
        super().__init__()
        self.singer_id = singer_id
        self.pn = pn
        self.rn = rn

    def run(self):
        try:
            rsp = get_kuwo_all_singer_music(self.singer_id, pn=self.pn, rn=self.rn)
            music_datas = [Music.from_dict(d) for d in rsp["data"]["list"]]
            total = rsp["data"]["total"]
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            music_datas = []
            total = 0
        self.singer_musics.emit(music_datas)
        self.total_musics.emit(total)
        self.finished.emit()


class SingerInfoWorker(QThread):
    singer_info = Signal(Singer)
    finished = Signal()

    def __init__(self, singer_name):
        """
        通过歌手名字查询歌手基本信息
        :param singer_name: 歌手名字
        """
        super().__init__()
        self.singer_name = singer_name

    def run(self) -> None:
        try:
            rsp = get_kuwo_artist_by_search_keyword(self.singer_name)
            singer = Singer.from_dict(rsp["data"]["list"][0])
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            singer = None
        self.singer_info.emit(singer)
        self.finished.emit()


class AlbumsWorker(QThread):
    albums = Signal(list)
    finished = Signal()

    def __init__(self, singer_id, pn=1, rn=500):
        """
        获取歌手的专辑列表
        :param singer_id:
        :param pn:
        :param rn: 这里 rn 之所以取一个比较大的值，
        是因为一般歌手的专辑数量不多,可以不用分页加载,
        所以干脆一次性加载完成
        """
        super().__init__()
        self.singer_id = singer_id
        self.pn = pn
        self.rn = rn

    def run(self) -> None:
        try:
            rsp = get_kuwo_all_singer_album(self.singer_id, pn=self.pn, rn=self.rn)
            if rsp["code"] != 200:
                LOGGER.error(f"load_singer_albums from singer_id = {self.singer_id} error:{rsp}")
                albums = []
            else:
                album_datas = rsp["data"]["albumList"]
                albums = [Album.from_dict(data) for data in album_datas]
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            albums = []
        self.albums.emit(albums)
        self.finished.emit()


class MvsWorker(QThread):
    mvs = Signal(list)
    finished = Signal()

    def __init__(self, singer_id, pn=1, rn=3000):
        """
        获取歌手的mv列表
        :param singer_id:
        :param pn:
        :param rn: 取一个比较大的值直接一次性加载完(偷懒做法,MV数量可能很多,最好还是分页加载)
        """
        super().__init__()
        self.singer_id = singer_id
        self.pn = pn
        self.rn = rn

    def run(self) -> None:
        try:
            rsp = get_kuwo_all_singer_mv(self.singer_id, pn=self.pn, rn=self.rn)
            if rsp["code"] != 200:
                LOGGER.error(f"load_singer_mvs from singer_id = {self.singer_id} error:{rsp}")
                mvs = []
            else:
                mv_datas = rsp["data"]["mvlist"]
                mvs = [Mv.from_dict(data) for data in mv_datas]
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            mvs = []
        self.mvs.emit(mvs)
        self.finished.emit()


class MvUrlWorker(QThread):
    """
    从mid加载 mv 的 url
    """
    mv_url = Signal(str)
    finished = Signal

    def __init__(self, mid):
        super().__init__()
        self.mid = mid

    def run(self) -> None:
        try:
            rsp = get_kuwo_mv_play_url(self.mid)
            if rsp["code"] != 200:
                mv_url = None
            else:
                mv_url = rsp["data"]["url"]
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            mv_url = None
        self.mv_url.emit(mv_url)
        self.finished.emit()
