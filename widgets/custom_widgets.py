# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/22 23:25
"""
一些自定义的组件放到这里
"""
import os
import threading

import requests
from PySide6.QtCore import QSize, Qt, QRect, Signal
from PySide6.QtGui import QIcon, QMouseEvent, QPainter, QColor, QTextFormat, QPainterPath
from PySide6.QtWidgets import *

from util.configs import load_music_config
from util.logs import LOGGER
from util.music_tools import get_music_download_url_by_mid

resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resource")


class MyPushButton(QPushButton):
    """
    自定义 QPushButton
    """

    def __init__(self, icon_path, parent=None):
        super().__init__(parent)
        self.setStyleSheet("QPushButton {border: none;}")
        icon = QIcon(icon_path)
        self.setIcon(icon)

    def resizeEvent(self, event):
        self.setIconSize(QSize(24, 24))
        super().resizeEvent(event)


class ClickableLabel(QLabel):
    """
    自定义可点击的QLabel
    """
    clicked = Signal()

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setEnabled(True)

    def mousePressEvent(self, event):
        self.clicked.emit()


from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPixmap
from PySide6.QtWidgets import QLabel


class CircularImageLabel(QLabel):
    """
    可以展示圆形图像的QLabel
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = QPixmap()

    def setPixmap(self, pixmap):
        self.pixmap = pixmap
        self.update()  # 更新视图

    def paintEvent(self, event):
        if not self.pixmap.isNull():  # 检查 pixmap 是否为空
            painter = QPainter(self)
            painter.setRenderHint(QPainter.Antialiasing, True)
            path = QPainterPath()
            path.addEllipse(0, 0, self.width(), self.height())
            painter.setClipPath(path)
            painter.drawPixmap(0, 0, self.pixmap.scaled(self.width(), self.height(), Qt.KeepAspectRatioByExpanding))


class HoverTableWidget(QTableWidget):
    """
    自定义表格组件
    """

    def __init__(self, main_window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_window = main_window
        self.verticalScrollBar().valueChanged.connect(self.check_scroll_position)
        self.setMouseTracking(True)  # enable mouse tracking
        self.play_button = QToolButton(self)  # create play button
        # set play button icon, replace with your icon file path
        self.play_button.setIcon(QIcon(os.path.join(resource_dir, 'icons/play_icon.png')))
        self.play_button.setVisible(False)  # hide play button initially
        self.play_button.clicked.connect(
            self.main_window.core_music_advance_player.play_music_by_music_table)

        # 创建下载按钮，设置图标和样式
        self.download_button = QToolButton(self)
        self.download_button.setIcon(QIcon(os.path.join(resource_dir, 'icons/not_download_icon.png')))
        self.download_button.setVisible(False)
        # 下载按钮的点击事件
        self.download_button.clicked.connect(self.download_music)

        self.current_hover_row = -1  # no row is hovered initially

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        """
        鼠标滚动事件
        :param event:
        :return:
        """
        item = self.itemAt(event.position().toPoint())
        if item is not None:
            self.selectRow(item.row())  # select the row under the cursor
            if item.column() == 0:  # if mouse is over the first column
                self.current_hover_row = item.row()
                self.show_play_button(item.row())  # show play button
                self.show_download_button(item.row())
            else:
                self.play_button.setVisible(False)  # hide play button
                self.download_button.setVisible(False)
        else:
            self.clearSelection()  # clear selection if not over a row
            self.play_button.setVisible(False)  # hide play button
            self.download_button.setVisible(False)
        super().mouseMoveEvent(event)

    def leaveEvent(self, event: QMouseEvent) -> None:
        """
        鼠标离开事件
        :param event:
        :return:
        """
        self.play_button.setVisible(False)  # hide play button when mouse leaves the table
        super().leaveEvent(event)

    def show_play_button(self, row):
        """
        实现的效果是:当鼠标移动到表格某一行第一列(歌曲列) 时,显示 播放 & 下载按钮
        :param row:
        :return:
        """
        # 如果当前行不可播放,则不显示 播放按钮
        music_id = self.main_window.getPlayStatusMusicByIndex(row).rid
        if self.main_window.is_music_invalid(music_id):
            self.play_button.setVisible(False)
            return
        rect = self.visualItemRect(self.item(row, 0))  # get the rect of the cell
        button_size = self.play_button.sizeHint()  # get the size of the play button
        # calculate x coordinate for the play button
        x = rect.right() - button_size.width() - self.download_button.sizeHint().width()
        # calculate y coordinate for the play button
        y = rect.top() + self.horizontalHeader().height() + (
                rect.height() - button_size.height()) // 2
        # set the geometry of the play button
        self.play_button.setGeometry(x, y, button_size.width(),
                                     button_size.height())
        # show the play button
        self.play_button.setVisible(True)

    def show_download_button(self, row):
        """
        展示 下载按钮
        :param row:
        :return:
        """
        music_id = self.main_window.getPlayStatusMusicByIndex(row).rid
        if self.main_window.is_music_invalid(music_id):
            self.download_button.setVisible(False)
            return
        rect = self.visualItemRect(self.item(row, 0))
        button_size = self.download_button.sizeHint()
        x = rect.right() - button_size.width()
        y = rect.top() + self.horizontalHeader().height() + (
                rect.height() - button_size.height()) // 2
        # 设置按钮位置和大小
        self.download_button.setGeometry(x, y, button_size.width(), button_size.height())
        # 已下载/未下载 音乐 使用不同的 图标
        if row in self.main_window.search_widget.downloaded_music_indexes:
            self.download_button.setIcon(QIcon(os.path.join(resource_dir, "icons/downloaded_icon.png")))
        else:
            self.download_button.setIcon(QIcon(os.path.join(resource_dir, "icons/not_download_icon.png")))
        self.download_button.setVisible(True)

    def check_scroll_position(self, value):
        """
        处理滑动条到最底端需要额外加载数据的情况
        :param value:
        :return:
        """
        # 处于搜索界面时
        if self.main_window.stacked_widget.currentWidget() is self.main_window.search_widget:
            if value == self.verticalScrollBar().maximum():
                self.main_window.search_widget.core_music_search.load_music_next_page()
        # 处于歌手全部歌曲界面时
        elif self.main_window.stacked_widget.currentWidget() is self.main_window.singer_main_window \
                and self.main_window.singer_main_window.stacked_widget.currentWidget() is self.main_window.singer_main_window.singer_music_window:
            if value == self.verticalScrollBar().maximum():
                self.main_window.singer_main_window.singer_music_window.append_singer_music_to_music_table()

    def download_music(self):
        """
        下载音乐
        :return:
        """
        row = self.current_hover_row
        music_play_status = self.main_window.getCurMusicPlayStatus()
        music = music_play_status.music_data[row]  # 获取音乐信息
        if self.main_window.is_music_invalid(music.rid):
            return
        if music.play_url is None:
            music.play_url = get_music_download_url_by_mid(music.rid)
        if music.play_url is None:
            QMessageBox.warning(self, "下载错误", "此歌曲无法下载!")
            self.main_window.invalid_play_music_set.add(music.rid)
            # Set the current row to be disabled
            self.main_window.search_widget.core_music_search.mark_music_table_row(row, "gray", True)
            return
        url = music.play_url  # 获取音乐的 url
        if self.main_window.music_config is None:
            self.main_window.music_config = load_music_config()
        music_download_dir = self.main_window.music_config["music_download_dir"]
        if music_download_dir == "":
            # 使用 QFileDialog 让用户选择保存的目录
            music_download_dir = QFileDialog.getExistingDirectory(self, '选择你保存音乐的目录', '~',
                                                                  QFileDialog.ShowDirsOnly)
            if music_download_dir:
                self.main_window.music_config["music_download_dir"] = music_download_dir
            else:
                music_download_dir = os.path.expanduser("~")
                self.main_window.music_config["music_download_dir"] = music_download_dir

        # 使用新线程下载文件，防止阻塞主线程
        def download_thread():
            response = requests.get(url, timeout=30)
            save_path = os.path.join(music_download_dir, f"{music.artist}_{music.name}.mp3")
            with open(save_path, 'wb') as f:
                f.write(response.content)
            self.main_window.search_widget.downloaded_music_indexes.add(row)
            LOGGER.info(f"Download from {url} to {save_path} succeed!")

        threading.Thread(target=download_thread).start()


class SearchInput(QLineEdit):
    """
    自定义搜索输入
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.parent.core_music_search.search_music()
        else:
            super().keyPressEvent(event)


class LineNumberArea(QWidget):
    """
    显示行号的区域
    """

    def __init__(self, editor):
        super().__init__(editor)
        self.myeditor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.myeditor.lineNumberAreaPaintEvent(event)


class TextEditWithLineNumber(QPlainTextEdit):
    """
    带有行号显示的自定义TextEdit
    """

    def __init__(self):
        super().__init__()

        self.lineNumberArea = LineNumberArea(self)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)

    def lineNumberAreaWidth(self):
        digits = 1
        max_value = max(1, self.blockCount())
        while max_value >= 10:
            max_value /= 10
            digits += 1
        space = 3 + self.fontMetrics().horizontalAdvance('9') * digits
        return space

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)

        painter.fillRect(event.rect(), Qt.lightGray)

        block = self.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.setPen(Qt.black)
                painter.drawText(0, top, self.lineNumberArea.width(), self.fontMetrics().height(),
                                 Qt.AlignCenter, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            blockNumber += 1

    def highlightCurrentLine(self):
        extraSelections = []
        if not self.isReadOnly():
            selection = QTextEdit.ExtraSelection()

            lineColor = QColor(Qt.yellow).lighter(160)

            selection.format.setBackground(lineColor)
            selection.format.setProperty(QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extraSelections.append(selection)
        self.setExtraSelections(extraSelections)
