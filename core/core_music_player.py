# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/23 00:17
"""
实现音乐播放的核心逻辑,如播放、暂停、上一首、下一首等
"""
import os

from PySide6.QtCore import QCoreApplication, QUrl
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtWidgets import QMessageBox

from music_meta.music_meta import MusicWithTime
from util.music_tools import get_music_download_url_by_mid
from util.utils import get_cur_record_time

resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resource")


class CoreMusicPlayer:
    """
    核心音乐播放类,包括暂停、播放、上一首、下一首等基本功能
    """

    def __init__(self, main_window):
        self.main_window = main_window

    def play_music(self):
        """
        播放音乐的逻辑
        :return:
        """
        if self.main_window.player.isPlaying():
            self.pause_music()
            # 更改播放图标为暂停
            self.main_window.play_button.setIcon(QIcon(os.path.join(resource_dir, "icons/music_pause_icon.png")))
        else:
            self.main_window.player.play()
            # 更改播放图标为播放
            self.main_window.play_button.setIcon(QIcon(os.path.join(resource_dir, "icons/music_play_icon.png")))

    def pause_music(self):
        """
        暂停音乐
        :return:
        """
        self.main_window.player.pause()

    def next_music(self):
        """
        下一首
        :return:
        """
        # 自动跳过已经判定为无法播放的歌曲
        music_play_status = self.main_window.getCurMusicPlayStatus()
        index = music_play_status.play_music_index + 1
        while index in music_play_status.invalid_play_music_indexes:
            index += 1
        if index >= len(music_play_status.music_data):
            index = 0
        self.main_window.core_music_advance_player.play_music_by_index(index)

    def prev_music(self):
        """
        上一首
        :return:
        """
        music_play_status = self.main_window.getCurMusicPlayStatus()
        index = music_play_status.play_music_index - 1
        while index in music_play_status.invalid_play_music_indexes:
            index -= 1
        if index < 0:
            index = len(music_play_status.music_data) - 1
        self.main_window.core_music_advance_player.play_music_by_index(index)

    def toggle_volume_slider(self):
        """
        设置音量可见
        :return:
        """
        self.main_window.volume_slider.setVisible(not self.main_window.volume_slider.isVisible())

    def set_volume(self, volume=50):
        """
        设置音量为给定的值
        :param volume: 音量数值
        :return:
        """
        self.main_window.audioOutput.setVolume(volume)

    def auto_play_next(self, status):
        """
        自动播放下一首
        :param status:
        :return:
        """
        if status == QMediaPlayer.EndOfMedia:
            self.next_music()


class CoreMusicAdvancePlayer:
    """
    高级音乐播放功能,如从搜索结果跳入播放、根据索引位置播放等等
    """

    def __init__(self, main_window):
        self.main_window = main_window

    def play_music_by_index(self, index):
        """
        播放 music_data 中的 第 index 首歌
        :param index:
        :return:
        """
        if self.main_window.player.isPlaying():
            self.main_window.player.stop()
            QCoreApplication.processEvents()  # process all pending events
        # 上一个正在播放的行取消标记
        music_play_status = self.main_window.getCurMusicPlayStatus()
        if music_play_status.play_music_index >= 0 and \
                music_play_status.play_music_index not in music_play_status.invalid_play_music_indexes:
            self.main_window.search_widget.core_music_search.unmark_music_table_row(music_play_status.play_music_index)
        music = music_play_status.music_data[index]
        music_play_status.play_music_index = index
        if index not in music_play_status.invalid_play_music_indexes and music.play_url is None:
            music.play_url = get_music_download_url_by_mid(music.rid)
        if music.play_url:
            url = QUrl(music.play_url)  # replace with your actual url
            self.main_window.player.setSource(url)
            self.main_window.player.play()
            self.main_window.play_button.setIcon(QIcon(os.path.join(resource_dir, "icons/music_play_icon.png")))
            self.main_window.core_auto_play.update_music_play_slider()
            self.main_window.core_auto_play.update_bottom_bar()
            self.main_window.search_widget.core_music_search.mark_music_table_row(index, "pink", False)
            # 添加到全局播放记录
            self.main_window.his_play_list.append(MusicWithTime(music, get_cur_record_time()))
        else:
            QMessageBox.warning(self.main_window, "播放错误", "此歌曲无法播放!")
            music_play_status.invalid_play_music_indexes.add(index)
            # Set the current row to be disabled
            self.main_window.search_widget.core_music_search.mark_music_table_row(index, "gray", True)

    def play_music_by_music_table(self):
        """
        从搜索结果来的播放
        :return:
        """
        self.play_music_by_index(
            self.main_window.getCurMusicPlayStatus().music_table.current_hover_row)
