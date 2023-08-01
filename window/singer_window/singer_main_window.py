# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 22:25
"""
歌手主页窗口
"""
from collections import defaultdict

from PySide6.QtCore import QUrl
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QHBoxLayout, QWidget, QStackedWidget

from q_thread.q_thread_tasks import *
from widgets.custom_widgets import *
from widgets.singer_main_window_widgets import SingerHeaderLabel
from window.singer_window.singer_album_window import SingerAlbumWindow
from window.singer_window.singer_hot_music_window import SingerHotMusicWindow
from window.singer_window.singer_music_window import SingerMusicWindow
from window.singer_window.singer_mv_window import SingerMvWindow
from window.template_window.template_with_back_button_window import TemplateWithBackButtonWindow


class SingerMainWindow(TemplateWithBackButtonWindow):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.initUI()
        self.initSlotConnect()
        self.initResources()

    def initResources(self):
        super().initResources()
        # 默认选中歌手热门歌曲label
        self.singer_selected_label = self.singer_header_hot_label
        self.singer_avatar_downloader = QNetworkAccessManager(self)
        self.singer_avatar_downloader.finished.connect(self.update_singer_avatar)
        self.singer_data_cache = defaultdict(dict)

    def initUI(self):
        super().initUI()
        # 歌手基本信息栏
        singer_info_layout = QHBoxLayout()
        self.singer_info_bar = QWidget()
        self.singer_info_bar.setLayout(singer_info_layout)
        # 保存歌手头像
        self.singer_avatar_label = CircularImageLabel()
        self.singer_avatar_label.setFixedSize(50, 50)
        # 保存歌手简介
        self.singer_desc_label = QLabel()
        singer_info_layout.addWidget(self.singer_avatar_label)
        singer_info_layout.addStretch()
        singer_info_layout.addWidget(self.singer_desc_label)

        # 歌手详情header_bar,分为精选/歌曲/专辑/视频 4个栏目
        singer_header_layout = QHBoxLayout()
        self.singer_header_bar = QWidget()
        self.singer_header_bar.setLayout(singer_header_layout)
        # 精选
        self.singer_header_hot_label = SingerHeaderLabel(self)
        self.singer_header_hot_label.setText("精选")
        # 歌曲
        self.singer_header_music_label = SingerHeaderLabel(self)
        self.singer_header_music_label.setText("歌曲")
        # 专辑
        self.singer_header_album_label = SingerHeaderLabel(self)
        self.singer_header_album_label.setText("专辑")
        # 视频
        self.singer_header_mv_label = SingerHeaderLabel(self)
        self.singer_header_mv_label.setText("视频")
        singer_header_layout.addWidget(self.singer_header_hot_label)
        singer_header_layout.addWidget(self.singer_header_music_label)
        singer_header_layout.addWidget(self.singer_header_album_label)
        singer_header_layout.addWidget(self.singer_header_mv_label)

        # 活动窗口
        self.initStackedWidget()

        # 添加到 layout
        self.layout.addWidget(self.singer_info_bar)
        self.layout.addWidget(self.singer_header_bar)
        self.layout.addWidget(self.stacked_widget)

    def initSlotConnect(self):
        super().initSlotConnect()
        self.singer_header_hot_label.clicked.connect(self.show_singer_hot_music_window)
        self.singer_header_music_label.clicked.connect(self.show_singer_music_window)
        self.singer_header_album_label.clicked.connect(self.show_singer_album_window)
        self.singer_header_mv_label.clicked.connect(self.show_singer_mv_window)

    def initStackedWidget(self):
        self.stacked_widget = QStackedWidget()
        self.singer_hot_music_window = SingerHotMusicWindow(self)
        self.singer_music_window = SingerMusicWindow(self)
        self.singer_album_window = SingerAlbumWindow(self)
        self.singer_mv_window = SingerMvWindow(self)

        self.stacked_widget.addWidget(self.singer_hot_music_window)
        self.stacked_widget.addWidget(self.singer_music_window)
        self.stacked_widget.addWidget(self.singer_album_window)
        self.stacked_widget.addWidget(self.singer_mv_window)

    def show_singer_hot_music_window(self):
        self.init_singer_info()
        self.singer_hot_music_window.show_window()

    def show_singer_music_window(self):
        self.init_singer_info()
        self.singer_music_window.show_window()

    def show_singer_album_window(self):
        self.init_singer_info()
        self.singer_album_window.show_window()

    def show_singer_mv_window(self):
        self.init_singer_info()
        self.singer_mv_window.show_window()

    def init_singer_info(self):
        singer_id = self.main_window.getCurMusic().artistid
        singer_name = self.main_window.getCurMusic().artist
        if not self.singer_data_cache[singer_id].get("info", None):
            self.singer_info_worker = SingerInfoWorker(singer_name)
            self.singer_info_worker.singer_info.connect(
                lambda singer_info: self.update_singer_info(singer_id, singer_info))
            self.singer_info_worker.finished.connect(lambda: self.singer_info_worker.deleteLater())
            self.singer_info_worker.start()

    def update_singer_info(self, singer_id, singer_info):
        """
        更新歌手信息
        :return:
        """
        self.singer_data_cache[singer_id]["info"] = singer_info
        singer_desc = f"歌手:{singer_info.name}<br>国家:{singer_info.country}<br>歌曲总数:{singer_info.musicNum}"
        self.singer_desc_label.setText(singer_desc)
        # 下载歌手头像链接
        self.singer_avatar_downloader.get(QNetworkRequest(QUrl(singer_info.pic)))

    def update_singer_avatar(self, reply):
        """
        更新歌手头像
        :param reply:
        :return:
        """
        data = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.singer_avatar_label.setPixmap(pixmap)

    def is_singer_label_selected(self, label):
        """
        判断 label 是否被选中
        :param label:
        :return:
        """
        return label is self.singer_selected_label

    def singer_label_clicked(self, label):
        if self.is_singer_label_selected(label):
            return
        if self.singer_selected_label is not None:  # 如果有被选中的 label，则将其颜色变回黑色
            self.singer_selected_label.setStyleSheet("color: black;")
        self.singer_selected_label = label  # 更新被选中的 label
        self.singer_selected_label.setStyleSheet("color: green;")  # 将新选中的 label 颜色变为绿色

    def show_window(self):
        self.main_window.show_singer_main_window()
