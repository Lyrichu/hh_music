# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 22:26
"""
歌手热门专辑窗口
"""
from collections import defaultdict

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView

from music_meta.album_meta import Album
from q_thread.q_thread_tasks import AlbumsWorker
from widgets.album_widgets import AlbumCoverWidget
from window.template_window.base_template_window import BaseTemplateWindow


class SingerAlbumWindow(BaseTemplateWindow):
    def __init__(self, main_window, albums: list[Album] = None):
        super().__init__(main_window)
        self.albums = albums
        self.album_table = None
        self.initResources()
        self.initUI()

    def initUI(self):
        super().initUI()

    def initResources(self):
        super().initResources()
        # 缓存不同歌手的 album_table,key 为 singer_id
        self.album_table_cache = defaultdict(dict)
        # album_cover 的 pixmap缓存,key为 album_id
        self.album_cover_cache = {}

    def init_album_table(self, albums):
        """
        初始化专辑表格展示界面
        :param albums: 专辑列表
        :return:
        """
        if len(albums) == 0:
            self.close_progress_dialog()
            self.task_failed_warning()
            return
        self.update_album_header_label(len(albums))
        if self.album_table is None:
            self.album_table = QTableWidget()
            self.layout.addWidget(self.album_table)
        else:
            # 清空表格
            self.album_table.setRowCount(0)
        # 一行展示4个专辑
        cols = 4
        rows = len(albums) // cols
        if len(albums) % cols > 0:
            rows += 1
        self.album_table.setRowCount(rows)
        self.album_table.setColumnCount(cols)
        for row in range(rows):
            for col in range(cols):
                index = row * cols + col
                if index >= len(albums):
                    break
                album = albums[index]
                # Create custom widget with album cover, name, and date
                album_widget = AlbumCoverWidget(self, album)
                # Create table widget item to hold custom widget
                table_widget_item = QTableWidgetItem()
                self.album_table.setItem(row, col, table_widget_item)
                self.album_table.setCellWidget(row, col, album_widget)
                # Adjust row height
                self.album_table.setRowHeight(row, 300)
                self.album_table.setShowGrid(False)

            # Remove cell selection highlighting
        self.album_table.setSelectionMode(QTableWidget.NoSelection)
        self.album_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.album_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 隐藏数字列
        self.album_table.verticalHeader().setVisible(False)
        self.album_table.horizontalHeader().setVisible(False)
        self.album_table.setStyleSheet("background-color: #e0e7c8;")

        # Resize columns to fit content
        self.album_table.resizeColumnsToContents()
        singer_id = self.main_window.main_window.getCurMusic().artistid
        # 添加到缓存
        self.album_table_cache[singer_id]["albums"] = albums
        self.close_progress_dialog()

    def update_album_header_label(self, albums_cnt):
        """
        更新 singer_main_window 的 singer_header_album_label
        显示具体的专辑数量
        :param albums_cnt:
        :return:
        """
        self.main_window.singer_header_album_label.setText(f"专辑{albums_cnt}")

    def show_window(self):
        # 首先加载歌手的全部专辑
        singer_id = self.main_window.main_window.getCurMusic().artistid
        if singer_id not in self.album_table_cache:
            self.show_progress_dialog()
            album_worker = AlbumsWorker(singer_id)
            album_worker.albums.connect(self.init_album_table)
            album_worker.finished.connect(lambda: album_worker.deleteLater())
            album_worker.start()
        else:
            albums = self.album_table_cache[singer_id]["albums"]
            self.init_album_table(albums)

        self.main_window.stacked_widget.setCurrentWidget(self)
