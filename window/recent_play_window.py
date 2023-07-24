# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/23 17:46
"""
最近播放窗口
"""
import os.path

from PySide6.QtWidgets import QWidget, QVBoxLayout

from widgets.custom_widgets import *

from window.music_searcher_window import MusicSearcher
from core.core_music_search import CoreMusicSearch
from music_meta.music_meta import MusicPlayStatus

resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resource")


class RecentPlayWindow(QWidget):
    def __init__(self, main_window):
        """
        最近播放列表窗口
        :param main_window:
        """
        super().__init__()
        self.main_window = main_window
        self.initUI()
        self.initSlotConnect()
        self.initPlayStatus()

    def initUI(self):
        """
        初始化UI
        :return:
        """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # 第一行 返回按钮 -- "最近收听"      -- 回到主页按钮
        # 第二行 music_table 形式展示的收听历史,按照时间逆序

        header_layout = QHBoxLayout()
        self.header_bar = QWidget()
        self.header_bar.setLayout(header_layout)

        self.back_button = MyPushButton(os.path.join(resource_dir, "icons/back_icon.png"))
        self.back_button.setText("返回")

        self.recent_play_label = QLabel("最近收听🎵")
        self.back_home_button = MyPushButton(os.path.join(resource_dir, "icons/back_home_icon.png"))
        self.back_home_button.setText("返回主页")

        header_layout.addWidget(self.back_button)
        header_layout.addWidget(self.recent_play_label)
        header_layout.addWidget(self.back_home_button)

        self.music_table = MusicSearcher.createMusicTable(self.main_window)

        self.layout.addWidget(self.header_bar)
        self.layout.addWidget(self.music_table)

    def initPlayStatus(self):
        """
        初始化音乐播放状态
        :return:
        """
        self.music_play_status = MusicPlayStatus()

    def initSlotConnect(self):
        self.back_button.clicked.connect(self.main_window.show_search_window)
        self.back_home_button.clicked.connect(self.main_window.show_search_window)

    def add_recent_play_list_to_music_table(self):
        """
        将用户收听历史添加到 music_table 展示
        :return:
        """
        # 历史收听列表倒序
        recent_play_list = list(reversed(self.main_window.his_play_list))
        music_datas = [m.music for m in recent_play_list]
        CoreMusicSearch.common_add_music_table_datas(self.music_table, music_datas)
        self.music_table.setVisible(True)

        self.music_play_status = MusicPlayStatus(
            self.music_table,
            music_datas,
            0
        )
