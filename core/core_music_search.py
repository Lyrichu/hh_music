# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/23 01:38
"""
音乐核心搜索功能的实现
"""
import traceback

from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush, QColor
from PySide6.QtWidgets import QMessageBox, QProgressDialog, QTableWidgetItem

from q_thread.q_thread_tasks import SearchWorker
from util.logs import LOGGER
from music_meta.lyric_meta import *
from util.music_tools import search_kuwo_music_by_keywords, get_music_download_url_by_mid
from api.kuwo_music_api import *


class CoreMusicSearch:
    def __init__(self, main_window):
        """
        核心音乐搜索类
        :param main_window:
        """
        self.main_window = main_window

    def search_music(self):
        # 当用户搜索时,显示一个等待条
        self.main_window.search_widget.show_progress_dialog()

        # Start a new q_thread to do the search
        search_worker = SearchWorker(self.main_window.search_widget.search_input.text())
        search_worker.search_res.connect(self.display_music_search_result)
        search_worker.finished.connect(lambda: search_worker.deleteLater())
        search_worker.start()

    def load_music_next_page(self):
        """
        加载下一页的搜索结果
        :return:
        """
        if self.is_loading:
            return
        self.is_loading = True
        self.current_page += 1
        query = self.main_window.search_widget.search_input.text()
        _, next_page_data = search_kuwo_music_by_keywords(query, self.current_page)
        self.main_window.getCurMusicPlayStatus().music_data.extend(next_page_data)
        self.search_backend_task()
        # Update the table
        self.add_music_table_datas(next_page_data, True)
        self.is_loading = False

    def display_music_search_result(self, total, search_results):
        """
        表格形式展示搜索的结果
        :param total: 搜索总数
        :param search_results: 搜索音乐结果
        :return:
        """
        # 关闭 等待条
        self.main_window.search_widget.close_progress_dialog()
        # 处理错误
        if total == 0 or len(search_results) == 0:
            self.main_window.search_widget.task_failed_warning()
        self.main_window.stacked_widget.currentWidget().music_play_status.music_data = search_results
        self.search_backend_task()
        self.main_window.stacked_widget.currentWidget().music_play_status.music_table.setVisible(True)
        self.main_window.stacked_widget.currentWidget().music_play_status.music_table.horizontalHeader().setVisible(
            True)
        self.is_loading = False
        # 当前搜索结果页(默认一页20条结果)
        self.current_page = 1
        self.main_window.search_widget.result_hint_bar.setVisible(True)
        self.main_window.search_widget.result_label.setText(f"共有 {total} 条匹配结果")
        self.add_music_table_datas(search_results)

    def search_backend_task(self):
        """
        搜索时触发的后台任务
        :return:
        """
        self._check_music_data_invalid_parts()
        self._get_music_lyrics()

    def _get_music_lyrics(self):
        """
        后台获取当前歌曲的歌词
        :return:
        """
        def _parse_lyrics(mid, music):
            try:
                rsp = get_kuwo_music_lyric(mid)
                music.lyrics = Lyric.lyrics_from_dict(rsp)
                # LOGGER.info(f"parse lyrics succeed for music:{music.name}")
            except Exception as e:
                LOGGER.error(f"parse lyrics error for music:{music.name}: " + traceback.format_exc())

        if self.main_window.getCurMusicPlayStatus().music_data:
            for i, music in enumerate(self.main_window.getCurMusicPlayStatus().music_data):
                if music.lyrics:
                    continue
                else:
                    mid = music.rid
                    self.main_window.search_widget.thread_pool.submit(
                        lambda mid=mid, music=music: _parse_lyrics(mid, music)
                    )

    def _check_music_data_invalid_parts(self):
        """
        后台检测 music_data 中 无法播放/下载的部分,标记为灰色不可用状态
        :return:
        """
        def _mark_invalid(i, music):
            if self.main_window.is_music_invalid(music.rid):
                self.mark_music_table_row(i, disable=True)
                return
            if music.play_url is None:
                music.play_url = get_music_download_url_by_mid(music.rid)
            if music.play_url is None:
                self.mark_music_table_row(i, disable=True)
                LOGGER.info(f"mark {music.artist}/{music.name} as disable succeed!")

        if self.main_window.getCurMusicPlayStatus().music_data:
            for i, music in enumerate(self.main_window.getCurMusicPlayStatus().music_data):
                if music.play_url:
                    continue
                # 这里注意匿名表达式闭包的问题
                self.main_window.search_widget.thread_pool.submit(lambda i=i, music=music: _mark_invalid(i, music))

    @staticmethod
    def common_add_music_table_datas(music_table, music_datas, append=False):
        """
        通用的music_table 写数据方法
        :param music_table:
        :param music_datas:
        :param append: 是否要追加
        :return:
        """
        if not append:
            music_table.setRowCount(0)
        col_cnt = music_table.columnCount()
        for music in music_datas:
            row = music_table.rowCount()
            music_table.insertRow(row)
            # create QTableWidgetItem and set its text alignment
            # 如果是4列,展示 歌曲/歌手/专辑/时长
            if col_cnt == 4:
                name_item = QTableWidgetItem(music.name)
                name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                music_table.setItem(row, 0, name_item)
                artist_item = QTableWidgetItem(music.artist)
                artist_item.setTextAlignment(Qt.AlignCenter)
                music_table.setItem(row, 1, artist_item)
                album_item = QTableWidgetItem(music.album)
                album_item.setTextAlignment(Qt.AlignCenter)
                music_table.setItem(row, 2, album_item)
                duration_item = QTableWidgetItem(music.songTimeMinutes)
                duration_item.setTextAlignment(Qt.AlignCenter)
                music_table.setItem(row, 3, duration_item)
            else:
                # 如果是3列, 展示 歌曲/专辑/时长
                name_item = QTableWidgetItem(music.name)
                name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                music_table.setItem(row, 0, name_item)
                album_item = QTableWidgetItem(music.album)
                album_item.setTextAlignment(Qt.AlignCenter)
                music_table.setItem(row, 1, album_item)
                duration_item = QTableWidgetItem(music.songTimeMinutes)
                duration_item.setTextAlignment(Qt.AlignCenter)
                music_table.setItem(row, 2, duration_item)

        return music_table

    def add_music_table_datas(self, datas, append=False):
        """
        将当前搜索结果添加到表格展示
        :param datas:
        :param append: 追加还是重新写入
        :return:
        """
        CoreMusicSearch.common_add_music_table_datas(
            self.main_window.getCurMusicPlayStatus().music_table, datas, append)
        # 每当搜索列表更新时，也更新已下载音乐的索引
        self.main_window.search_widget.core_music_downloader.add_downloaded_music_to_indexes()

    def mark_music_table_row(self, row, color="gray",
                             disable=False):
        """
        标记 music_table 搜索结果的某行(标记颜色、禁用等)
        :param row: 行
        :param color: 标记颜色
        :param disable: 是否禁用
        :return:
        """
        music_play_status = self.main_window.getCurMusicPlayStatus()
        for col in range(music_play_status.music_table.columnCount()):
            item = self.main_window.getCurMusicPlayStatus().music_table.item(row, col)
            if disable:
                item.setFlags(item.flags() & ~Qt.ItemIsEnabled)
                music_id = music_play_status.music_data[row].rid
                self.main_window.invalid_play_music_set.add(music_id)
            item.setBackground(QBrush(QColor(color)))

    def unmark_music_table_row(self, row):
        """
        对搜索结果的某一行取消标记
        :param row:
        :param music_table:
        :return:
        """
        # Set the row to be enabled
        for col in range(self.main_window.getCurMusicPlayStatus().music_table.columnCount()):
            item = self.main_window.getCurMusicPlayStatus().music_table.item(row, col)
            item.setFlags(item.flags() | Qt.ItemIsEnabled)
            item.setBackground(QBrush())
