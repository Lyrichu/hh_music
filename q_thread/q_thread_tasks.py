# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/22 23:36
"""
这里保存一些继承自 QThread/QRunnable 的 工作类
"""
from PySide6.QtCore import QThread, Signal

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

