# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 22:26
"""
歌手全部音乐窗口
"""
from window.template_window.base_template_window import BaseTemplateWindow


class SingerMusicWindow(BaseTemplateWindow):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.initUI()

    def initUI(self):
        super().initUI()
