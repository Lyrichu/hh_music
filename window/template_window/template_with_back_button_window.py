# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 22:32
"""
基础的模板类,有一个header_bar,分别有一个返回上一级/返回主页按钮
"""
import os

from PySide6.QtWidgets import QWidget, QHBoxLayout

from widgets.custom_widgets import MyPushButton
from window.template_window.base_template_window import BaseTemplateWindow

resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "resource")


class TemplateWithBackButtonWindow(BaseTemplateWindow):
    def __init__(self, main_window):
        super().__init__(main_window)

    def initUI(self):
        """
        初始化UI
        :return:
        """
        super().initUI()
        # 第一行 返回按钮 -- 回到主页按钮

        header_layout = QHBoxLayout()
        self.header_bar = QWidget()
        self.header_bar.setLayout(header_layout)
        self.back_button = MyPushButton(os.path.join(resource_dir, "icons/back_icon.png"))
        self.back_home_button = MyPushButton(os.path.join(resource_dir, "icons/back_home_icon.png"))

        header_layout.addWidget(self.back_button)
        # 添加一个弹性空间,使得两个按钮分布在最左侧和最右侧
        header_layout.addStretch(1)
        header_layout.addWidget(self.back_home_button)

        self.layout.addWidget(self.header_bar)

    def initSlotConnect(self):
        """
        默认返回按钮，返回上一个窗口;
        主页按钮返回搜索主页
        :return:
        """
        self.back_button.clicked.connect(self.main_window.back_to_prev_window)
        self.back_home_button.clicked.connect(self.main_window.show_search_window)
