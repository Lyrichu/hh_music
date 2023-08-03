# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 22:26
"""
歌手MV窗口
"""
from collections import defaultdict

from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView

from music_meta.mv_meta import Mv
from q_thread.q_thread_tasks import MvsWorker
from widgets.mv_widgets import MvCoverWidgets
from window.template_window.base_template_window import BaseTemplateWindow


class SingerMvWindow(BaseTemplateWindow):
    def __init__(self, main_window, mvs: list[Mv] = None):
        super().__init__(main_window)
        self.mvs = mvs
        self.mv_table = None
        self.initResources()
        self.initUI()

    def initUI(self):
        super().initUI()

    def initResources(self):
        super().initResources()
        # 缓存不同歌手的 mv_table,key 为 singer_id
        self.mv_table_cache = defaultdict(dict)
        # mv_cover 的 pixmap缓存,key为 mv_id
        self.mv_cover_cache = {}

    def init_mv_table(self, mvs):
        """
        初始化mv表格展示界面
        :param mvs: mv列表
        :return: 
        """
        if len(mvs) == 0:
            self.close_progress_dialog()
            self.task_failed_warning()
            return
        self.update_mv_header_label(len(mvs))
        if self.mv_table is None:
            self.mv_table = QTableWidget()
            self.layout.addWidget(self.mv_table)
        else:
            # 清空表格
            self.mv_table.setRowCount(0)
        # 一行展示4个mv
        cols = 4
        rows = len(mvs) // cols
        if len(mvs) % cols > 0:
            rows += 1
        self.mv_table.setRowCount(rows)
        self.mv_table.setColumnCount(cols)
        for row in range(rows):
            for col in range(cols):
                index = row * cols + col
                if index >= len(mvs):
                    break
                mv = mvs[index]
                mv_widget = MvCoverWidgets(self, mv)
                # Create table widget item to hold custom widget
                table_widget_item = QTableWidgetItem()
                self.mv_table.setItem(row, col, table_widget_item)
                self.mv_table.setCellWidget(row, col, mv_widget)
                # Adjust row height
                self.mv_table.setRowHeight(row, 300)
                self.mv_table.setShowGrid(False)

            # Remove cell selection highlighting
        self.mv_table.setSelectionMode(QTableWidget.NoSelection)
        self.mv_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.mv_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # 隐藏数字列
        self.mv_table.verticalHeader().setVisible(False)
        self.mv_table.horizontalHeader().setVisible(False)
        self.mv_table.setStyleSheet("background-color: #e0e7c8;")

        # Resize columns to fit content
        self.mv_table.resizeColumnsToContents()
        singer_id = self.main_window.main_window.getCurMusic().artistid
        # 添加到缓存
        self.mv_table_cache[singer_id]["mvs"] = mvs
        self.close_progress_dialog()

    def update_mv_header_label(self, mvs_cnt):
        """
        更新歌手mv显示数量
        :param mvs_cnt: 歌手mv数量
        :return:
        """
        self.main_window.singer_header_mv_label.setText(f"视频{mvs_cnt}")

    def show_window(self):
        # 首先加载歌手的全部mv
        singer_id = self.main_window.main_window.getCurMusic().artistid
        if singer_id not in self.mv_table_cache:
            self.show_progress_dialog()
            mv_worker = MvsWorker(singer_id)
            mv_worker.mvs.connect(self.init_mv_table)
            mv_worker.finished.connect(lambda: mv_worker.deleteLater())
            mv_worker.start()
        else:
            mvs = self.mv_table_cache[singer_id]["mvs"]
            self.init_mv_table(mvs)

        self.main_window.stacked_widget.setCurrentWidget(self)
