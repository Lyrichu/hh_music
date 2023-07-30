# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 23:57
"""
基础的模板窗口类
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout


class BaseTemplateWindow(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def initUI(self):
        """
        初始化UI
        :return:
        """
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def initSlotConnect(self):
        pass

    def initResources(self):
        pass
