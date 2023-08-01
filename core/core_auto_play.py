# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/23 01:16
"""
处理音乐自动播放相关的逻辑,如进度条更新、自动展示歌曲封面等等
"""
from PySide6.QtCore import QUrl, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtNetwork import QNetworkRequest

from util.utils import format_duration


class CoreAutoPlay:
    def __init__(self, main_window):
        """
        核心音乐自动播放类
        :param main_window: 主窗口
        """
        self.main_window = main_window

    def update_music_play_position(self, position):
        """
        更新音乐播放到指定位置
        :param position:
        :return:
        """
        # position 是当前播放位置，单位是毫秒，转换成秒需要除以1000
        current_position = position // 1000
        # 将秒数转换成 MM:ss 的格式
        formatted_position = format_duration(current_position)
        # 更新 duration_item 的显示
        music_data = self.main_window.getCurMusicPlayStatus().music_data
        play_music_index = self.main_window.getCurMusicPlayStatus().play_music_index
        if len(music_data) == 0:
            return
        total_time = music_data[play_music_index].songTimeMinutes
        self.main_window.music_play_progress_label.setText(f"{formatted_position}/{total_time}")

    def download_cover(self, url):
        """
        下载音乐封面
        :param url:
        :return:
        """
        self.main_window.music_cover_downloader.get(QNetworkRequest(QUrl(url)))

    def update_music_cover(self, reply):
        """
        更新专辑封面
        :param reply:
        :return:
        """
        data = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(data)
        self.main_window.music_pixmap = pixmap
        scaled_pixmap = pixmap.scaledToHeight(self.main_window.play_button.sizeHint().height(), Qt.SmoothTransformation)
        self.main_window.cover_label.setPixmap(scaled_pixmap)
        self.main_window.lyric_window.update_image(pixmap)

    def update_music_play_slider(self):
        """
        更新音乐播放进度条的位置
        :return:
        """
        music_play_status = self.main_window.getCurMusicPlayStatus()
        self.main_window.music_play_slider.setVisible(True)
        self.main_window.music_play_slider.setMaximum(music_play_status.music_data[music_play_status.play_music_index].duration * 1000)
        self.main_window.music_play_slider.setMinimum(0)
        self.main_window.music_play_slider.setValue(0)

    def music_play_slider_changed(self, value):
        """
        监听音乐播放滑块的移动
        :param value:
        :return:
        """
        # This method is called when the slider's value is changed
        # You should update the music player's position here
        self.main_window.player.setPosition(value)
        # 同步更新歌词,注意这里需要重置歌词的当前行
        self.main_window.lyric_window.update_time(value / 1000)

    def update_music_play_slider_position(self):
        """
        更新音乐播放滑块的位置
        :return:
        """
        # This method is called every 1 second
        # You should update the slider's value here
        if self.main_window.player.isPlaying():
            self.main_window.music_play_slider.setValue(self.main_window.player.position())
            # 同时通知更新歌词,注意传入的单位需要转化成秒
            self.main_window.lyric_window.update_time(self.main_window.player.position() / 1000)

    def update_bottom_bar(self):
        """
        更新音乐底部播放栏(bottom_bar)的状态
        :return:
        """
        self.main_window.bottom_bar.setVisible(True)
        music = self.main_window.getCurMusic()
        self.download_cover(music.pic)
        self.main_window.title_label.setText(music.name)
        self.main_window.artist_label.setText(music.artist)
        self.main_window.music_play_progress_label.setText(
            f"{format_duration(0)}/{music.songTimeMinutes}")  # replace 0 with current playback position
