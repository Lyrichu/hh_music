# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/24 09:35
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from window.main_window import MainWindow


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowIcon(QIcon("resource/icons/music_app_icon.png"))
    window.show()
    app.exec()