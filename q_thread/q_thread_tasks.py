# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/22 23:36
"""
这里保存一些继承自 QThread/QRunnable 的 工作类
"""
from PySide6.QtCore import QThread, Signal

from api.kuwo_music_api import *
from music_meta.music_meta import Music
from music_meta.singer_meta import Singer
from util.music_tools import search_kuwo_music_by_keywords


class SearchWorker(QThread):
    """
    音乐搜索的工作类
    """
    # (搜索总数,当前音乐列表)
    finished_signal = Signal(int, list)

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
        self.finished_signal.emit(*result)


class SingerHotMusicWorker(QThread):
    """
    获取歌手的热门歌曲任务
    """
    singer_hot_musics = Signal(list)
    finished = Signal()

    def __init__(self, singer_id):
        super().__init__()
        self.singer_id = singer_id

    def run(self):
        rsp = get_kuwo_all_singer_music(self.singer_id)
        music_datas = [Music.from_dict(d) for d in rsp["data"]["list"]]
        self.singer_hot_musics.emit(music_datas)
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
        rsp = get_kuwo_artist_by_search_keyword(self.singer_name)
        singer = Singer.from_dict(rsp["data"]["list"][0])
        self.singer_info.emit(singer)
        self.finished.emit()
