# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 23:57
"""
基础的模板窗口类
"""
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QProgressDialog, QMessageBox


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

    def show_window(self):
        pass

    def task_failed_warning(self):
        """
        任务失败时,弹出一个对话框提醒用户
        :return:
        """
        QMessageBox.warning(self, "额出错了...", "请稍后重试~")

    def show_progress_dialog(self):
        """
        加载可能需要一段时间,显示一个等待条
        :return:
        """
        self.search_progress_dialog = \
            QProgressDialog("(*^▽^*)努力加载ing...", "Cancel", 0, 0, self)
        self.search_progress_dialog.setCancelButton(None)  # remove cancel button
        self.search_progress_dialog.setWindowModality(Qt.ApplicationModal)
        self.search_progress_dialog.show()

    def close_progress_dialog(self):
        """
        关闭等待进度条
        :return:
        """
        self.search_progress_dialog.close()
