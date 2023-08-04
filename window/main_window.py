# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/23 16:50
import os
from concurrent.futures import ThreadPoolExecutor

from PySide6.QtCore import QTimer, QEvent
from PySide6.QtGui import QAction
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtNetwork import QNetworkAccessManager
from PySide6.QtWidgets import QWidget, QVBoxLayout, QStackedWidget, QSlider, QLabel, QSizePolicy, QHBoxLayout

from const.music_playing_constants import *
from core.core_auto_play import CoreAutoPlay
from core.core_music_player import CoreMusicPlayer, CoreMusicAdvancePlayer
from music_meta.music_meta import MusicWithTime, MusicPlayStatus, Music
from window.music_searcher_window import MusicSearcher
from window.recent_play_window import RecentPlayWindow
from util.configs import save_music_config
from util.utils import *
from util.music_tools import load_user_history_music_play_list_from_file, write_to_user_history_music_play_list_file
from widgets.custom_widgets import *
from window.log_window import LogWindow
from window.music_download_window import DownloadWindow
from window.lyric_window import LyricWindow
from window.singer_window.singer_main_window import SingerMainWindow

resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resource")


class MainWindow(QMainWindow):
    def __init__(self):
        """
        主窗口类
        """
        super().__init__()
        self.setWindowTitle("HH🎵播放器")
        self.setGeometry(100, 100, 500, 500)

        self.initCores()
        self.initMenus()
        self.initUI()
        self.initSeperateWindows()
        self.initResource()
        self.initPlayStatus()
        self.initSlotConnect()

        self.show_search_window()

    def show_recent_play_window(self):
        """
        展示最近播放窗口
        :return:
        """
        # 首先准备好历史播放数据
        self.recent_play_window.add_recent_play_list_to_music_table()
        self.current_windows_list.append(self.stacked_widget.currentWidget())
        # 然后再切换到最近播放窗口
        self.stacked_widget.setCurrentWidget(self.recent_play_window)

    def show_search_window(self):
        """
        展示搜索窗口
        :return:
        """
        self.current_windows_list.append(self.stacked_widget.currentWidget())
        self.stacked_widget.setCurrentWidget(self.search_widget)

    def show_lyric_window(self):
        """
        展示歌词窗口
        :return:
        """
        if self.stacked_widget.currentWidget() is not self.lyric_window:
            # 如果当前不是歌词窗口,则切换到歌词窗口
            # 准备歌词
            self.lyric_window.prepare_lyrics()
            self.lyric_window.update_image()
            self.current_windows_list.append(self.stacked_widget.currentWidget())
            self.stacked_widget.setCurrentWidget(self.lyric_window)
        else:
            # 如果已经是歌词窗口了,则返回到搜索窗口
            self.show_search_window()

    def show_singer_main_window(self):
        """
        展示歌手详情窗口
        :return:
        """
        self.current_windows_list.append(self.stacked_widget.currentWidget())
        # 准备好歌手详情数据
        self.singer_main_window.show_singer_hot_music_window()

    def back_to_prev_window(self):
        if len(self.current_windows_list) == 0:
            self.show_search_window()
        else:
            prev_window = self.current_windows_list.pop()
            prev_window.show_window()

    def initUI(self):
        """
        初始化UI 界面
        :return:
        """
        # 整体式垂直布局
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)
        # 这一部分作为活动窗口,可以在不同的窗口之间切换
        self.initStackedWidget()
        # 底部播放栏作为固定窗口(包括bottom_bar和 music_play_slider)
        self.initBottomLayout()

        self.main_layout.addWidget(self.stacked_widget)
        self.main_layout.addWidget(self.music_play_slider)
        self.main_layout.addWidget(self.bottom_bar)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        self.setCentralWidget(self.main_widget)

    def initSeperateWindows(self):
        # 单独的窗口
        self.download_window = DownloadWindow(self)
        self.log_window = LogWindow(self)

    def initStackedWidget(self):
        """
        初始化可以切换的窗口
        :return:
        """
        # 管理切换的窗口
        self.stacked_widget = QStackedWidget()
        self.layout().addWidget(self.stacked_widget)
        # 搜索窗口
        self.search_widget = MusicSearcher(self)
        # 最近播放窗口
        self.recent_play_window = RecentPlayWindow(self)
        # 显示歌词的窗口
        self.lyric_window = LyricWindow(self)
        # 显示歌手详情的窗口
        self.singer_main_window = SingerMainWindow(self)

        self.stacked_widget.addWidget(self.search_widget)
        self.stacked_widget.addWidget(self.recent_play_window)
        self.stacked_widget.addWidget(self.lyric_window)
        self.stacked_widget.addWidget(self.singer_main_window)

    def initCores(self):
        """
        初始化一些核心类(如核心播放类、下载类等等)
        :return:
        """
        # 核心音乐播放器
        self.core_music_player = CoreMusicPlayer(self)
        # 高级音乐播放器
        self.core_music_advance_player = CoreMusicAdvancePlayer(self)
        # 自动播放相关
        self.core_auto_play = CoreAutoPlay(self)

    def initMenus(self):
        """
        初始化菜单栏
        :return:
        """
        download_action = QAction('下载器', self)
        download_action.triggered.connect(self.open_download_window)
        download_menu = self.menuBar().addMenu('下载')
        download_menu.addAction(download_action)

        log_action = QAction("日志记录", self)
        log_action.triggered.connect(self.open_log_window)
        log_menu = self.menuBar().addMenu("日志")
        log_menu.addAction(log_action)

    def initBottomLayout(self):
        # 初始音乐播放化进度条
        self.music_play_slider = QSlider(Qt.Horizontal)
        self.music_play_slider.setMinimum(0)
        self.music_play_slider.setMaximum(100)  # Suppose the maximum value is 100
        self.music_play_slider.setValue(0)
        self.music_play_slider.setVisible(False)

        # 最近播放
        self.recent_play_list_button = MyPushButton(os.path.join(resource_dir, "icons/recent_play_icon.png"))
        self.recent_play_list_button.setText("最近播放")

        # Create bottom bar widgets
        # 封面
        self.cover_label = ClickableLabel(self)
        # 歌曲
        self.title_label = QLabel()
        # 歌手
        self.artist_label = ClickableLabel(self)
        # 上一首按钮
        self.prev_button = MyPushButton(os.path.join(resource_dir, 'icons/prev_icon.png'))
        # 播放按钮
        self.play_button = MyPushButton(os.path.join(resource_dir, 'icons/music_play_icon.png'))
        # 下一首按钮
        self.next_button = MyPushButton(os.path.join(resource_dir, 'icons/next_icon.png'))
        # 播放顺序按钮
        self.play_order_button = MyPushButton(os.path.join(resource_dir, "icons/play_song_in_order.png"))
        # 音乐播放进度(文本动态更新)
        self.music_play_progress_label = QLabel()
        # 音量调节滑块
        self.volume_button = MyPushButton(os.path.join(resource_dir, 'icons/volume_icon.png'))
        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)  # set initial volume to 50
        self.volume_slider.setVisible(False)  # hide volume slider initially

        # 保存底部播放栏相关布局
        self.bottom_bar = QWidget()
        # 水平可扩展/垂直不可扩展
        self.bottom_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # 水平布局
        self.bottom_layout = QHBoxLayout(self.bottom_bar)
        # 添加一个可伸缩布局,这样整个控件可以始终居中显示
        self.bottom_layout.addStretch()
        # 最近播放
        self.bottom_layout.addWidget(self.recent_play_list_button)
        # 专辑封面
        self.bottom_layout.addWidget(self.cover_label)
        # 歌曲名称
        self.bottom_layout.addWidget(self.title_label)
        # 歌手名称
        self.bottom_layout.addWidget(self.artist_label)
        # 上一首按钮
        self.bottom_layout.addWidget(self.prev_button)
        # 播放按钮
        self.bottom_layout.addWidget(self.play_button)
        # 下一首按钮
        self.bottom_layout.addWidget(self.next_button)
        # 播放顺序按钮
        self.bottom_layout.addWidget(self.play_order_button)
        # 音乐播放进度(文本展示)
        self.bottom_layout.addWidget(self.music_play_progress_label)
        # 音量按钮
        self.bottom_layout.addWidget(self.volume_button)
        # 音量滑块
        self.bottom_layout.addWidget(self.volume_slider)
        # 在布局的末尾添加一个水平弹性空间
        self.bottom_layout.addStretch()
        # 初始化的时候默认不显示
        self.bottom_bar.setVisible(False)

    def initSlotConnect(self):
        # 监听窗口的切换
        self.stacked_widget.currentChanged.connect(self.onStackedWindowCurChanged)
        # 上一首
        self.prev_button.clicked.connect(self.core_music_player.play_prev_music)
        # 播放按钮
        self.play_button.clicked.connect(self.core_music_player.play_music)
        # 下一首
        self.next_button.clicked.connect(self.core_music_player.play_next_music)
        # 音量滑块
        self.volume_button.clicked.connect(self.core_music_player.toggle_volume_slider)
        # 调整音量
        self.volume_slider.valueChanged.connect(self.core_music_player.set_volume)
        # 歌曲封面,点击之后展示歌词窗口
        self.cover_label.clicked.connect(self.show_lyric_window)
        # 歌手,点击之后展示歌手详情窗口
        self.artist_label.clicked.connect(self.show_singer_main_window)
        # 播放器的播放进度改变时
        self.player.positionChanged.connect(self.core_auto_play.update_music_play_position)
        # 自动播放下一首
        self.player.mediaStatusChanged.connect(self.core_music_player.auto_play_next)
        # 调整音乐播放顺序
        self.play_order_button.clicked.connect(self.core_music_player.change_play_order)
        # 用户滑动进度条可以快进/后退 到指定位置
        self.music_play_slider.sliderMoved.connect(self.core_auto_play.music_play_slider_changed)
        # 定时器 使得 播放进度条可以每秒自动更新
        self.music_play_slider_timer = QTimer()
        self.music_play_slider_timer.timeout.connect(self.core_auto_play.update_music_play_slider_position)
        # Start timer
        self.music_play_slider_timer.start(1000)  # update every 1 second
        # 显示最近播放
        self.recent_play_list_button.clicked.connect(self.show_recent_play_window)

    def initResource(self):
        """
        初始化一些必要的资源
        :return:
        """
        # 线程池
        self.thread_pool = ThreadPoolExecutor(max_workers=20)
        # 网络资源管理器
        self.music_cover_downloader = QNetworkAccessManager(self)
        self.music_cover_downloader.finished.connect(self.core_auto_play.update_music_cover)
        # 歌曲封面 pixmap
        self.music_pixmap = None
        # 初始化播放器
        self.player = QMediaPlayer()
        # 音频输出
        self.audioOutput = QAudioOutput()
        # 初始化音量
        self.core_music_player.set_volume()
        self.player.setAudioOutput(self.audioOutput)
        # 记录播放顺序
        self.play_order = MusicPlayingOrder.PLAY_IN_ORDER
        # 记录当前正在播放的Music
        self.cur_playing_music = None
        # 记录不合法(一般是无法播放)的音乐
        self.invalid_play_music_set = set()
        # 维护窗口的切换顺序,方便返回上一个窗口
        self.current_windows_list = []

    def initPlayStatus(self):
        """
        初始化音乐播放、下载 等 相关配置
        :return:
        """
        # 音乐的配置文件字典
        self.music_config = None
        # 全局历史播放列表
        self.his_play_list: list[MusicWithTime] = load_user_history_music_play_list_from_file()

    def open_download_window(self):
        """
        打开下载器窗口
        :return:
        """
        self.download_window.show()

    def open_log_window(self):
        """
        打开日志记录窗口
        :return:
        """
        self.log_window.show()

    def onStackedWindowCurChanged(self, index):
        """
        监听 stackedWindow 发生变化
        :return:
        """
        curWindow = self.stacked_widget.currentWidget()
        LOGGER.info(f"Window changed to {curWindow}")

    def getCurMusicPlayStatus(self) -> MusicPlayStatus:
        """
        获取当前的音乐播放状态
        :return:
        """
        curWindow = self.stacked_widget.currentWidget()
        if curWindow in [self.search_widget, self.recent_play_window]:
            return curWindow.music_play_status
        elif curWindow is self.singer_main_window:
            singer_cur_window = self.singer_main_window.stacked_widget.currentWidget()
            if singer_cur_window is self.singer_main_window.singer_hot_music_window:
                return self.singer_main_window.singer_hot_music_window.music_play_status
            else:
                return self.singer_main_window.singer_music_window.music_play_status
        return self.search_widget.music_play_status

    def getCurMusic(self) -> Music:
        """
        获取当前正在播放的音乐
        :return:
        """
        return self.cur_playing_music

    def getPlayStatusMusicByIndex(self, index):
        """
        获取当前播放列表的音乐(可能不是正在播放的音乐)
        :return:
        """
        music_play_status = self.getCurMusicPlayStatus()
        return music_play_status.music_data[index]

    def is_music_invalid(self, music_id):
        return music_id in self.invalid_play_music_set

    def changeEvent(self, event):
        """
        监听窗口的改变
        :param event:
        :return:
        """
        if event.type() == QEvent.WindowStateChange:
            # 进入全屏
            enter_fullscreen = self.windowState() & Qt.WindowFullScreen
            # 退出全屏
            exit_fullscreen = event.oldState() & Qt.WindowFullScreen and not self.windowState() & Qt.WindowFullScreen
            if enter_fullscreen or exit_fullscreen:
                # 动态更改歌曲封面
                self.lyric_window.update_image()
                # 更改歌词字体大小/展示行数
                if enter_fullscreen:
                    self.lyric_window.lyric_font_size = 14
                    self.lyric_window.lyric_manager.lyric_part_display_lines = 10
                else:
                    self.lyric_window.lyric_font_size = 12
                    self.lyric_window.lyric_manager.lyric_part_display_lines = 5
                #self.lyric_window.lyric_display.setFont(get_custom_font(font_size=self.lyric_window.lyric_font_size))

    def closeEvent(self, event):
        """
        主窗口被关闭时会调用
        :param event:
        :return:
        """
        # 在这里添加你的清理代码
        # 保存 music_config
        if self.music_config:
            save_music_config(**self.music_config)
        # 保存 his_play_list
        if self.his_play_list:
            write_to_user_history_music_play_list_file(self.his_play_list)
        event.accept()  # 关闭窗口
