# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/23 02:15
"""
核心音乐下载类,主要继承一些与下载音乐相关的逻辑
"""
from PySide6.QtWidgets import QMessageBox, QCheckBox

from util.configs import load_music_config
from util.logs import LOGGER
from util.music_tools import get_music_download_url_by_mid, load_user_downloaded_music_names


class CoreMusicDownloader:
    def __init__(self, main_window):
        """
        核心音乐下载类
        :param main_window:
        """
        self.main_window = main_window

    def start_batch_download_musics(self):
        """
        批量下载音乐的任务
        :return:
        """
        urls = []
        music_names = []
        choose_checked_box_num = 0
        music_play_status = self.main_window.getCurMusicPlayStatus()
        for row in range(music_play_status.music_table.rowCount()):
            music = music_play_status.music_data[row]
            checkbox = music_play_status.music_table.cellWidget(row, 0)
            if checkbox and checkbox.isChecked():
                choose_checked_box_num += 1
            # 跳过已经下载的音乐
            if checkbox and checkbox.isChecked() and music.play_url \
                    and row not in self.main_window.search_widget.downloaded_music_indexes:
                urls.append(music.play_url)
                music_names.append(f"{music.artist}_{music.name}.mp3")
        LOGGER.info(f"choose {len(urls)}/{choose_checked_box_num} to download!")
        skip_num = choose_checked_box_num - len(urls)
        if skip_num > 0:
            QMessageBox.warning(self.main_window.search_widget, "跳过下载",
                                f"已为您跳过{skip_num}/{choose_checked_box_num}的音乐下载,因为它们已经被下载了!")
        if self.main_window.music_config is None:
            self.main_window.music_config = load_music_config()
        self.main_window.download_window.start_download(urls, music_names,
                                                        self.main_window.music_config["music_download_dir"],
                                                        self.main_window.music_config["concurrent_download_num"]
                                                        )

    def show_download_checkboxes(self):
        """
        显示所有的下载单选框
        :return:
        """

        # 获取 music play url 可能需要一定的时间, 在单独的线程中处理该任务,防止阻塞主线程
        def _task():
            music_play_status = self.main_window.getCurMusicPlayStatus()
            for row in range(music_play_status.music_table.rowCount()):
                music_id = self.main_window.getPlayStatusMusicByIndex(row).rid
                if self.main_window.is_music_invalid(music_id):
                    continue
                music = music_play_status.music_data[row]
                if music.play_url is None:
                    music.play_url = get_music_download_url_by_mid(music.rid)
                if music.play_url:
                    self.main_window.search_widget.show_download_checkbox_signal.emit(row)
                else:
                    self.main_window.invalid_play_music_set.add(music.rid)
            self.main_window.search_widget.show_download_checkbox_signal.emit(-1)

        self.main_window.search_widget.thread_pool.submit(_task)

    def show_download_checkbox(self, row):
        """
        处理显示单条下载单选框的逻辑
        :param row:
        :return:
        """
        # 说明此时已经完成所有搜索结果单选框的判断
        if row == -1:
            self.main_window.search_widget.batch_download_cancel_button.setVisible(True)
            self.main_window.search_widget.select_download_all_checkbox.setChecked(False)
            self.main_window.search_widget.select_download_all_checkbox.setVisible(True)
            self.main_window.search_widget.start_download_button.setVisible(True)
        else:
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(self.update_selected_count_button)
            self.main_window.getCurMusicPlayStatus().music_table.setCellWidget(row, 0, checkbox)

    def update_selected_count_button(self, state):
        choose_cnt = 0
        total_cnt = 0
        music_table = self.main_window.getCurMusicPlayStatus().music_table
        for row in range(music_table.rowCount()):
            checkbox = music_table.cellWidget(row, 0)
            if checkbox:
                total_cnt += 1
                if checkbox.isChecked():
                    choose_cnt += 1
        self.main_window.search_widget.selected_count_button.setVisible(True)
        self.main_window.search_widget.selected_count_button.setText(f"已选{choose_cnt}/{total_cnt}")

    def update_all_download_checkboxes(self, state):
        """
        更新所有下载单选框的状态(选中/取消)
        :param state:
        :return:
        """
        # 选中/未选中 的 单选框数量
        choose_cnt = 0
        music_table = self.main_window.getCurMusicPlayStatus().music_table
        for row in range(music_table.rowCount()):
            checkbox = music_table.cellWidget(row, 0)
            if checkbox:
                choose_cnt += 1
                checkbox.setChecked(state)
        # 更新 选择数量按钮的文本
        if state:
            self.main_window.search_widget.selected_count_button.setVisible(True)
            self.main_window.search_widget.selected_count_button.setText(f"已选{choose_cnt}")
        else:
            self.main_window.search_widget.selected_count_button.setVisible(False)

    def cancel_batch_download_action(self):
        """
        取消批量下载的行为
        :return:
        """
        # 1.取消 & 隐藏所有的下载框
        music_table = self.main_window.getCurMusicPlayStatus().music_table
        for row in range(music_table.rowCount()):
            checkbox = music_table.cellWidget(row, 0)
            if checkbox:
                checkbox.setChecked(False)
                checkbox.setVisible(False)
        # 2.取消 & 隐藏 全选框/开始下载 等控件
        self.main_window.search_widget.batch_download_cancel_button.setVisible(False)
        self.main_window.search_widget.select_download_all_checkbox.setChecked(False)
        self.main_window.search_widget.select_download_all_checkbox.setVisible(False)
        self.main_window.search_widget.selected_count_button.setVisible(False)
        self.main_window.search_widget.start_download_button.setVisible(False)

    def add_downloaded_music_to_indexes(self):
        # 格式:歌手_歌曲.mp3
        downloaded_music_names = load_user_downloaded_music_names()
        cur_music_names = {f"{music.artist}_{music.name}.mp3": i for i, music in enumerate(self.main_window.stacked_widget.currentWidget().music_play_status.music_data)}
        for music_name in downloaded_music_names:
            if music_name in cur_music_names:
                self.main_window.search_widget.downloaded_music_indexes.add(cur_music_names[music_name])
