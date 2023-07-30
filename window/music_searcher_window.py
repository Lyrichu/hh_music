# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/21 13:48
import os.path

from PySide6.QtWidgets import QLabel, QHeaderView, QAbstractItemView, QCheckBox

from core.core_music_downloader import CoreMusicDownloader
from core.core_music_search import CoreMusicSearch
from window.log_window import *
from window.music_download_window import *
from music_meta.music_meta import MusicPlayStatus

from widgets.custom_widgets import HoverTableWidget

from util.utils import *

resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resource")


class MusicSearcher(QWidget):
    """
    音乐搜索的主类
    """
    # 显示下载单选框的信号
    show_download_checkbox_signal = Signal(int)

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.initUI()
        # 公共线程池
        self.thread_pool = ThreadPoolExecutor(max_workers=10)

    def initSignalConnections(self):
        self.show_download_checkbox_signal.connect(self.core_music_downloader.show_download_checkbox)

    def initUI(self):
        """
        初始化UI
        :return:
        """
        self.setGeometry(100, 100, 500, 500)
        self.initCores()
        self.initResources()
        self.initSignalConnections()

        self.initSearchWidgets()
        self.initResultHintWidgets()
        self.initMusicTable()
        self.initMainLayout()
        self.initSlotConnect()

    def initCores(self):
        """
        初始化一些核心类(如核心搜索类、下载类等等)
        :return:
        """
        # 核心音乐搜索类
        self.core_music_search = CoreMusicSearch(self.main_window)
        # 核心音乐下载类
        self.core_music_downloader = CoreMusicDownloader(self.main_window)

    def initSearchWidgets(self):
        """
        初始化搜索组件
        :return:
        """
        # 搜索栏
        self.search_bar = QWidget()
        self.search_layout = QHBoxLayout(self.search_bar)
        # 搜索输入框
        self.search_input = SearchInput(self)
        self.search_input.setPlaceholderText("搜索歌曲/歌手/专辑...")
        self.search_button = MyPushButton(os.path.join(resource_dir, "icons/search_icon.png"))
        self.search_layout.addWidget(self.search_input)
        self.search_layout.addWidget(self.search_button)

    def initResultHintWidgets(self):
        """
        初始化搜索提示组件(也包括音乐批量下载等功能)
        :return:
        """
        # 用于提示搜索总数
        self.result_label = QLabel()
        self.result_label.setFont(get_custom_font())
        self.result_label.setStyleSheet("QLabel { color : green; }")

        self.batch_download_button = MyPushButton(os.path.join(resource_dir, "icons/batch_download_icon.png"))
        self.batch_download_button.setText("批量下载")

        self.batch_download_cancel_button = MyPushButton(os.path.join(resource_dir, "icons/cancel_icon.png"))
        self.batch_download_cancel_button.setText("取消")
        self.batch_download_cancel_button.setVisible(False)

        self.select_download_all_checkbox = QCheckBox("全选")
        self.select_download_all_checkbox.setVisible(False)

        # 用于展示 已选数量 & 下载进度
        self.selected_count_button = QPushButton()
        self.selected_count_button.setStyleSheet(
            """
            QPushButton {
                background-color: cyan;
                border: none;
            }
        """
        )
        self.selected_count_button.setVisible(False)

        # 开始下载按钮
        self.start_download_button = MyPushButton(os.path.join(resource_dir, "icons/start_icon.png"))
        self.start_download_button.setText("开始")
        self.start_download_button.setVisible(False)

        self.result_hint_bar = QWidget()
        self.result_hint_layout = QHBoxLayout(self.result_hint_bar)

        self.result_hint_layout.addWidget(self.result_label)
        self.result_hint_layout.addWidget(self.batch_download_button)
        self.result_hint_layout.addWidget(self.batch_download_cancel_button)
        self.result_hint_layout.addWidget(self.select_download_all_checkbox)
        self.result_hint_layout.addWidget(self.selected_count_button)
        self.result_hint_layout.addWidget(self.start_download_button)
        # 初始化不可见,有搜索结果后可见
        self.result_hint_bar.setVisible(False)

    @staticmethod
    def createMusicTable(main_window, rows=0, cols=4,
                         headers=["歌曲", "歌手", "专辑", "时长"]):
        """
        创建一个通用的音乐展示table布局
        :param main_window:
        :param rows: 表格初始化行数
        :param cols: 表格初始化列数
        :param headers: 表头标题
        :return:
        """
        music_table = HoverTableWidget(main_window, rows, cols)
        music_table.verticalHeader().setVisible(False)  # hide vertical header
        music_table.horizontalHeader().setVisible(True)  # hide horizontal header initially
        music_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        music_table.setFont(get_custom_font(font_size=10))
        music_table.setShowGrid(False)
        music_table.verticalHeader().setVisible(False)
        music_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # select entire rows
        music_table.setStyleSheet(
            "QTableWidget::item:selected { background-color: gray; }"  # gray background for selected rows
        )
        # 表格是只读的
        music_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        music_table.setVisible(False)
        music_table.setHorizontalHeaderLabels(headers)
        music_table.setRowCount(0)  # clear the table
        return music_table

    def initMusicTable(self):
        """
        初始化搜索音乐结果 表格布局组件
        :return:
        """
        self.music_table = MusicSearcher.createMusicTable(self.main_window)
        self.music_play_status = MusicPlayStatus(self.music_table)

    def initResources(self):
        # 记录已经下载过的歌曲索引
        self.downloaded_music_indexes = set()

    def initSlotConnect(self):
        """
        初始化组件信号slot连接
        :return:
        """
        # Connect buttons to functions
        # 开始搜索音乐
        self.search_button.clicked.connect(self.core_music_search.search_music)
        # 点击 批量下载按钮 显示音乐下载单选框
        self.batch_download_button.clicked.connect(self.core_music_downloader.show_download_checkboxes)
        # 点击 取消按钮, 隐藏 相关组件
        self.batch_download_cancel_button.clicked.connect(self.core_music_downloader.cancel_batch_download_action)
        # 开始批量下载
        self.start_download_button.clicked.connect(self.core_music_downloader.start_batch_download_musics)
        # 全选 checkbox
        self.select_download_all_checkbox.stateChanged.connect(
            self.core_music_downloader.update_all_download_checkboxes)

        def _selected_btn_clicked():
            btn_text = self.selected_count_button.text()
            if btn_text and "已选" not in btn_text:
                self.main_window.open_download_window()

        self.selected_count_button.clicked.connect(_selected_btn_clicked)

    def initMainLayout(self):
        """
        初始化主界面布局
        :return:
        """
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.search_bar)
        self.main_layout.addWidget(self.result_hint_bar)
        self.main_layout.addWidget(self.music_table)
        self.setLayout(self.main_layout)
