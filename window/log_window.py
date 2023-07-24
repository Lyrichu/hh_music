# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/23 08:56
"""
显示日志记录的窗口
"""
import os.path
from threading import Lock

from PySide6.QtCore import QTimer, QRegularExpression
from PySide6.QtGui import QTextCursor, QTextBlockUserData, QTextDocument, QTextCharFormat
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget

from util.logs import get_log_file
from widgets.custom_widgets import *

resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resource")


class HighlightData(QTextBlockUserData):
    """
    TextEdit 高亮显示的区域
    """

    def __init__(self):
        super().__init__()
        # 高亮显示的文本区域列表,格式为[(start1,end1),(start2,end2),...]
        self.ranges = []


class SearchWidget(QLineEdit):
    """
    自定义搜索输入
    """

    def __init__(self, parent):
        super().__init__()
        self.parent = parent

    def keyPressEvent(self, event):
        """
        支持按下回车触发搜索
        :param event:
        :return:
        """
        if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
            self.parent.search("enter")
        else:
            super().keyPressEvent(event)


class LogWindow(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.log_file = get_log_file()
        self.setWindowTitle(f"日志记录({self.log_file})")
        self.initUI()
        self.show_logs()

    def initUI(self):
        """
        初始化UI布局
        :return:
        """
        self.initResource()
        self.initSearchBar()
        self.initLogArea()
        self.initBottomBar()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.search_bar)
        self.layout.addWidget(self.log_view)
        self.layout.addWidget(self.bottom_status_bar)

        central_widget = QWidget()
        central_widget.setLayout(self.layout)
        self.setCentralWidget(central_widget)

    def initSearchBar(self):
        """
        初始化搜索框相关布局
        :return:
        """
        self.search_input = SearchWidget(self)
        self.search_input.setPlaceholderText("搜索关键字")
        self.search_input.textChanged.connect(self.start_search_timer)

        self.search_button = MyPushButton(os.path.join(resource_dir, "icons/search_icon.png"))
        self.search_button.clicked.connect(self.search)

        # 搜索类型
        self.search_type_combo = QComboBox(self)
        self.search_type_combo.addItem("精确匹配")
        self.search_type_combo.addItem("单词匹配")
        self.search_type_combo.addItem("部分匹配(区分大小写)")
        self.search_type_combo.addItem("部分匹配(不区分大小写)")
        self.search_type_combo.addItem("正则匹配")

        self.search_bar = QWidget()
        self.search_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.search_layout = QHBoxLayout(self.search_bar)

        # 创建一个定时器，只有 search_input 用户停止输入一段时间后才会触发搜索，尽量减小卡顿
        self.search_timer = QTimer()
        self.search_timer.setSingleShot(True)  # 让定时器只触发一次
        self.search_timer.timeout.connect(self.search)

        self.search_all_checkbox = QCheckBox(self)
        self.search_all_checkbox.setText("搜索全部")
        self.search_all_checkbox.setChecked(True)
        self.search_all_checkbox.stateChanged.connect(self.search_all_changed)

        self.prev_search_button = MyPushButton(os.path.join(resource_dir, "icons/arrow_up_green.png"))
        self.prev_search_button.setText("上一个")
        self.prev_search_button.clicked.connect(self.search_previous)
        self.prev_search_button.setVisible(False)  # 默认隐藏

        self.next_search_button = MyPushButton(os.path.join(resource_dir, "icons/arrow_down_green.png"))
        self.next_search_button.setText("下一个")
        self.next_search_button.clicked.connect(self.search_next)
        self.next_search_button.setVisible(False)  # 默认隐藏

        self.search_type_combo.currentIndexChanged.connect(self.search)

        self.search_layout.addStretch()
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)
        self.search_layout.addWidget(self.search_type_combo)
        self.search_layout.addWidget(self.search_all_checkbox)
        self.search_layout.addWidget(self.prev_search_button)
        self.search_layout.addWidget(self.next_search_button)
        self.search_layout.addStretch()

    def initLogArea(self):
        """
        初始化日志显示区域相关部件
        :return:
        """
        self.log_view = TextEditWithLineNumber()
        self.log_view.setReadOnly(True)

        # 设置光标宽度为2像素
        self.log_view.setCursorWidth(2)
        # 创建一个新的文本光标，并将其位置设置为文档的开始
        text_cursor = self.log_view.textCursor()
        text_cursor.setPosition(0)
        # 设置文本框的光标为新创建的光标
        self.log_view.setTextCursor(text_cursor)

        self.log_view.cursorPositionChanged.connect(self.update_cursor_position)

    def initBottomBar(self):
        """
        初始化底部栏相关布局
        :return:
        """
        # Create the status bar
        self.bottom_status_bar = QStatusBar(self)
        # 显示 光标所在位置
        self.bottom_cursor_position_label = QLabel(self)

        # 匹配进度
        self.search_process_label = QLabel(self)
        self.search_process_label.setVisible(False)
        # 显示匹配结果
        self.search_result_label = QLabel(self)
        self.search_result_label.setVisible(False)

        # Add the labels to the status bar
        self.bottom_status_bar.addWidget(self.bottom_cursor_position_label)
        self.bottom_status_bar.addPermanentWidget(self.search_process_label)
        self.bottom_status_bar.addPermanentWidget(self.search_result_label)

    def initResource(self):
        """
        初始化一些必要的资源
        :return:
        """
        # 全局搜索匹配个数
        self.global_total_search_match_cnt = 0
        # 当前已经匹配的索引
        self.cur_search_match_index = 0
        # 计算关键词匹配的多线程锁
        self.global_total_search_match_lock = Lock()
        # 记录log_view 上一次的光标信息
        self.log_view_pre_cursor = None

    def show_logs(self):

        # Read the log file and add to the log view
        with open(self.log_file, 'r') as f:
            lines = f.readlines()

            # Iterate over the lines in reverse order
            for line in reversed(lines):
                # Highlight the line if it contains "ERROR" or "error"
                fmt = QTextCharFormat()
                if "ERROR" in line or "error" in line:
                    fmt.setBackground(QColor("red"))
                self.log_view.setCurrentCharFormat(fmt)

                self.log_view.appendPlainText(line)

        # Reset the format for the next append
        self.log_view.setCurrentCharFormat(QTextCharFormat())
        # Scroll to top
        self.log_view.moveCursor(QTextCursor.Start)

    def _search_one_by_cursor(self, cursor, keyword, search_back=False):
        """
        通过 cursor 寻找下一个关键词
        :param cursor:
        :param keyword:
        :return:
        """
        search_type = self.search_type_combo.currentText()
        # Determine how to search based on the combo box selection
        find_flag = None
        if search_type == "部分匹配(区分大小写)":
            find_flag = QTextDocument.FindFlag.FindCaseSensitively
        elif search_type == "部分匹配(不区分大小写)":
            find_flag = None
        elif search_type == "精确匹配":
            find_flag = QTextDocument.FindFlag.FindWholeWords | QTextDocument.FindFlag.FindCaseSensitively
        elif search_type == "单词匹配":
            find_flag = QTextDocument.FindFlag.FindWholeWords

        if find_flag is None and search_back:
            find_flag = QTextDocument.FindFlag.FindBackward
        elif find_flag is not None and search_back:
            find_flag |= QTextDocument.FindFlag.FindBackward

        if search_type == "正则匹配":
            reg_exp = QRegularExpression(keyword)
            if search_back:
                cursor = self.log_view.document().find(reg_exp, cursor, QTextDocument.FindFlag.FindBackward)
            else:
                cursor = self.log_view.document().find(reg_exp, cursor)
        else:
            if find_flag:
                cursor = self.log_view.document().find(keyword, cursor, find_flag)
            else:
                cursor = self.log_view.document().find(keyword, cursor)

        return cursor

    def search_all_changed(self, checked):
        """
        追踪全选框的状态变化
        :param checked: 是否选中
        :return:
        """
        if checked:
            self.search_all()
            self.next_search_button.setVisible(False)
            self.prev_search_button.setVisible(False)
            self.search_process_label.setVisible(False)
        else:
            self.clear_highlights()
            self.prev_search_button.setVisible(True)
            self.next_search_button.setVisible(True)
            self.reset_global_search_match_cnt()
            # 重置 cursor
            self.log_view.setTextCursor(QTextCursor(self.log_view.document()))

    def hightlight_by_cursor(self, cursor, color=Qt.yellow):
        """
        指定 cursor 位置所在文本高亮
        :param cursor:
        :param color:
        :return:
        """
        _format = QTextCharFormat()
        # 设置高亮颜色,如果没有，则重置为默认值
        if color:
            _format.setBackground(color)
        if not cursor.isNull():
            cursor.setCharFormat(_format)

    def get_global_search_match_cnt(self, cursor, keyword):
        total_cnt = 0
        while not cursor.isNull() and not cursor.atEnd():
            cursor = self._search_one_by_cursor(cursor, keyword)
            if not cursor.isNull():
                total_cnt += 1
        return total_cnt

    def highlight_all_match_keywords(self, keyword, color=Qt.yellow):
        """
        高亮所有匹配到的关键词
        :param keyword: 搜索关键字
        :param color: 高亮颜色
        :return:
        """
        # Create a new cursor that spans the entire document
        cursor = QTextCursor(self.log_view.document())
        self.log_view.setTextCursor(cursor)
        # Loop over all occurrences of the text
        total_cnt = 0
        while not cursor.isNull() and not cursor.atEnd():
            cursor = self._search_one_by_cursor(cursor, keyword)
            if not cursor.isNull():
                total_cnt += 1
                self.hightlight_by_cursor(cursor, color)
        self.update_search_result(total_cnt)

    def clear_highlights(self):
        """
        清除日志文本的所有高亮
        :return:
        """
        # Create a new cursor that spans the entire document
        cursor = QTextCursor(self.log_view.document())
        format = QTextCharFormat()
        # Do not set any format options - this will clear all previous formatting

        # Set the format for the entire document
        cursor.select(QTextCursor.Document)
        cursor.setCharFormat(format)
        self.search_result_label.clear()
        self.search_result_label.setVisible(False)
        self.log_view_pre_cursor = None

    def reset_global_search_match_cnt(self):
        """
        重置全局关键词匹配个数
        :return:
        """
        with self.global_total_search_match_lock:
            keyword = self.search_input.text()
            cursor = QTextCursor(self.log_view.document())
            self.global_total_search_match_cnt = self.get_global_search_match_cnt(cursor, keyword)
            self.cur_search_match_index = 0

    def start_search_timer(self):
        # Start or restart the timer whenever the text is changed
        self.search_timer.start(300)

    def search(self, search_way=None):
        """
        核心搜索逻辑,支持搜索全部/上一个/下一个
        :param search_way: 搜索方案(全部还是部分)
        :return:
        """
        if self.search_all_checkbox.isChecked():
            self.search_all()
        else:
            if search_way:
                self.search_next()
            else:
                # hint
                self.reset_global_search_match_cnt()
                self.search_next(True)

    def search_all(self):
        """
        搜索全部
        :return:
        """
        # 获取搜索关键词
        keyword = self.search_input.text()
        if not keyword:
            self.clear_highlights()
            return
        # Clear any existing highlights
        self.clear_highlights()
        # 高亮搜索关键词
        self.highlight_all_match_keywords(keyword)

    def search_next(self, reset=False):
        """
        搜索下一个匹配
        :param reset: 是否需要从头匹配
        :return:
        """
        keyword = self.search_input.text()
        if reset:
            cursor = QTextCursor(self.log_view.document())
        else:
            cursor = self.log_view.textCursor()
        cursor = self._search_one_by_cursor(cursor, keyword)
        if not cursor.isNull():
            self.log_view.setTextCursor(cursor)
            self.hightlight_by_cursor(cursor)

        self.update_pre_cursor(cursor)

        with self.global_total_search_match_lock:
            self.cur_search_match_index += 1
            if self.cur_search_match_index > self.global_total_search_match_cnt:
                self.cur_search_match_index = self.global_total_search_match_cnt
            self.search_process_label.setVisible(True)
            self.search_process_label.setText(
                f"匹配到第{self.cur_search_match_index}/{self.global_total_search_match_cnt}个")

    def search_previous(self, reset=False):
        """
        搜索上一个匹配
        :return:
        """
        keyword = self.search_input.text()
        if reset:
            cursor = QTextCursor(self.log_view.document())
        else:
            cursor = self.log_view.textCursor()
        cursor = self._search_one_by_cursor(cursor, keyword, True)
        if not cursor.isNull():
            self.log_view.setTextCursor(cursor)
            self.hightlight_by_cursor(cursor)

        self.update_pre_cursor(cursor)

        with self.global_total_search_match_lock:
            if self.cur_search_match_index > 1:
                self.cur_search_match_index -= 1
            self.search_process_label.setVisible(True)
            self.search_process_label.setText(
                f"匹配到第{self.cur_search_match_index}/{self.global_total_search_match_cnt}个")

    def update_pre_cursor(self, cursor):
        """
        更新上一个cursor
        :param cursor:
        :return:
        """
        if self.log_view_pre_cursor and not self.log_view_pre_cursor.isNull():
            self.hightlight_by_cursor(self.log_view_pre_cursor, None)
        self.log_view_pre_cursor = cursor

    def update_cursor_position(self):
        """
        更新光标区域并显示当前位置
        :return:
        """
        cursor = self.log_view.textCursor()
        line = cursor.blockNumber() + 1
        column = cursor.columnNumber() + 1
        self.bottom_cursor_position_label.setText(f"{line}行{column}列")

    def update_search_result(self, count):
        """
        更新搜索匹配结果
        :param count:
        :return:
        """
        self.search_result_label.setVisible(True)
        self.search_result_label.setText(f"匹配到{count}个")
