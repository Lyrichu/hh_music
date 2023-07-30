# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/27 17:19
"""
歌词展示窗口
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QTextEdit, QHBoxLayout, QSizePolicy

from music_meta.lyric_meta import *
from api.kuwo_music_api import get_kuwo_music_lyric
from util.utils import *


class LyricManager:
    """
    歌词管理器
    """

    def __init__(self, main_window):
        self.main_window = main_window
        # 歌词列表
        self.lyrics = []
        # 当前播放进度对应的歌词行数
        self.current_line = 0
        # 歌词上下展示行数
        self.lyric_part_display_lines = 5

    def set_lyrics(self, lyrics: list[Lyric]):
        self.lyrics = lyrics
        self.current_line = 0

    def update_time(self, time):
        """
        随时间更新歌词,按照如下的格式展示歌词:
        1.用绿色高亮显示当前的歌词
        2.当前歌词上下最多显示5行歌词
        :param time:歌曲播放时间(s)
        :return:
        """
        # 重新遍历所有歌词,设定当前播放行
        for i, lyric in enumerate(self.lyrics):
            if lyric.time > time:
                self.current_line = max(0, i - 2)
                break
        # 如果已经到最后一行歌词了，不处理
        if self.current_line >= len(self.lyrics) - 1:
            return
        if self.lyrics[self.current_line].time < time:
            self.current_line += 1
        start_line = max(0, self.current_line - self.lyric_part_display_lines)
        end_line = min(len(self.lyrics) - 1, self.current_line + self.lyric_part_display_lines)
        lines_to_display = [lyric.line_lyric for lyric in self.lyrics[start_line:end_line + 1]]
        cur_line_index = lines_to_display.index(self.lyrics[self.current_line].line_lyric)
        if len(lines_to_display) > 0:
            # 文本居中对齐
            lines_to_display = [f"<div align='center'>{line}</div>" for line in lines_to_display]
            for i, line in enumerate(lines_to_display):
                # Calculate the transparency based on the distance to the current line
                # 实现效果:离当前歌词行越远,显示越透明,类似淡出的效果
                distance = abs(i - cur_line_index)
                transparency = max(0.3, 1 - distance * 0.1)
                # 当前行时绿色,其他行是黑色，并且需要设置透明度
                color = '#00FF00' if i == cur_line_index else '#000000'  # Use hex color codes
                lines_to_display[i] = f"<span style='color: {color}; opacity: {transparency};'>{line}</span>"
            # Update the lyric display
            self.main_window.lyric_display.setHtml("<br>".join(lines_to_display))

    def reset(self):
        self.current_line = 0


class LyricWindow(QWidget):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle('歌词')
        # 歌词字体大小
        self.lyric_font_size = 12
        # 展示 歌曲封面
        self.music_cover_label = QLabel(self)
        self.music_cover_label.setMinimumSize(250, 250)
        self.music_cover_label.setStyleSheet("background-color: #f8f8f6;")
        self.music_cover_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 展示歌词的区域
        self.lyric_display = QTextEdit(self)
        self.lyric_display.setReadOnly(True)
        self.lyric_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lyric_display.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lyric_display.setFont(get_custom_font(font_size=self.lyric_font_size))
        self.lyric_display.setStyleSheet("background-color: #faeeef;")

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.music_cover_label, 1)
        self.layout.addWidget(self.lyric_display, 1)

        self.lyric_manager = LyricManager(self)

    def prepare_lyrics(self):
        """
        准备歌词数据
        :return:
        """
        music_status = self.main_window.getCurMusicPlayStatus()
        cur_music = music_status.music_data[music_status.play_music_index]
        lyrics = cur_music.lyrics
        if not lyrics:
            rsp = get_kuwo_music_lyric(cur_music.rid)
            lyrics = Lyric.lyrics_from_dict(rsp)
            cur_music.lyrics = lyrics
        self.set_lyrics(lyrics)

    def set_lyrics(self, lyrics):
        """
        设置歌词
        :param lyrics:
        :return:
        """
        self.lyric_manager.set_lyrics(lyrics)

    def update_time(self, time):
        """
        随着音乐播放动态更新歌词
        :param time: 当前歌曲播放时间(s)
        :return:
        """
        self.lyric_manager.update_time(time)

    def update_image(self, pixmap=None):
        """
        更新封面
        :param pixmap:
        :return:
        """
        if pixmap is None:
            pixmap = self.main_window.music_pixmap
        self.music_cover_label.setPixmap(pixmap.scaledToHeight(self.music_cover_label.height()))
