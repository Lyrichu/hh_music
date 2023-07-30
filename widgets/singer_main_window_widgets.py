# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/29 12:32
"""
歌手主页显示的一些自定义组件
"""
from widgets.custom_widgets import ClickableLabel


class SingerHeaderLabel(ClickableLabel):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.setStyleSheet("color: black;")  # 初始颜色为黑色
        self.setMouseTracking(True)  # 启用鼠标追踪

    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        self.main_window.singer_label_clicked(self)

    def enterEvent(self, event):
        self.setStyleSheet("color: green;")  # 鼠标悬停时变为绿色

    def leaveEvent(self, event):
        if not self.main_window.is_singer_label_selected(self):  # 如果没有被选中，则颜色变回黑色
            self.setStyleSheet("color: black;")
