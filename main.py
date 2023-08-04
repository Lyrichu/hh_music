# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/24 09:35
import os
import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from window.main_window import MainWindow

resource_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resource")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowIcon(QIcon(os.path.join(resource_dir, "icons/music_app_icon.png")))
    with open(os.path.join(resource_dir, "styles/stylesheet.qss")) as f:
        window.setStyleSheet(f.read())
    window.show()
    sys.exit(app.exec())
