# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/8/1 22:30
"""
专辑相关的自定义组件
"""

from PySide6.QtCore import Qt, QUrl, QEvent
from PySide6.QtGui import QPixmap
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QVBoxLayout, QLabel, QWidget

from music_meta.album_meta import Album
from widgets.custom_widgets import ClickableLabel, HoverColorNameLabel


class AlbumCoverWidget(QWidget):
    """
    专辑封面组件
    """

    def __init__(self, main_window, album: Album,
                 album_cover_size=(200, 200)):
        """
        :param main_window: 父窗口
        :param album: Album专辑类
        :param album_cover_size: 专辑封面大小(宽,高)
        """
        super().__init__(main_window)
        self.main_window = main_window
        self.album = album
        self.album_cover_size = album_cover_size
        self.network_manager = QNetworkAccessManager()

        self.initUI()
        # 先尝试从 cache 中 读取
        if self.album.albumid in self.main_window.album_cover_cache:
            pixmap = self.main_window.album_cover_cache[self.album.albumid]
            self.album_cover_label.setPixmap(pixmap)
        # 获取不到则进行网络请求
        else:
            self.set_album_pixmap()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.album_name_label = HoverColorNameLabel(self, self.album.album)
        self.album_name_label.setMaximumWidth(self.album_cover_size[0])
        self.album_name_label.setTextFormat(Qt.TextFormat.RichText)  # 设置文本格式为 RichText
        self.album_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.release_date_label = QLabel(self.album.releaseDate)
        self.release_date_label.setMaximumWidth(self.album_cover_size[0])
        self.release_date_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.album_cover_pixmap = QPixmap()
        self.album_cover_label = QLabel()
        self.album_cover_label.setFixedSize(*self.album_cover_size)
        self.album_cover_label.enterEvent = self.album_cover_entered
        self.album_cover_label.leaveEvent = self.album_cover_leaved
        self.album_cover_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(self.album_cover_label)
        layout.addWidget(self.album_name_label)
        layout.addWidget(self.release_date_label)

    def set_album_pixmap(self):
        request = QNetworkRequest(QUrl(self.album.pic))
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self.on_download_album_cover_finished(reply))

    def on_download_album_cover_finished(self, reply):
        """
        当通过url加载完成专辑封面时
        :param reply
        :return:
        """
        data = reply.readAll()
        self.album_cover_pixmap.loadFromData(data)
        pixmap = self.album_cover_pixmap.scaled(*self.album_cover_size, Qt.KeepAspectRatio)
        self.album_cover_label.setPixmap(pixmap)
        # 添加到缓存
        self.main_window.album_cover_cache[self.album.albumid] = pixmap

    def album_cover_entered(self, event):
        """
        当鼠标进入专辑封面时,显示边框 表示选中
        :param event:
        :return:
        """
        self.album_cover_label.setStyleSheet("border: 3px solid green;")

    def album_cover_leaved(self, event):
        """
        鼠标离开专辑封面时，取消选中
        :param event:
        :return:
        """
        self.album_cover_label.setStyleSheet("")
