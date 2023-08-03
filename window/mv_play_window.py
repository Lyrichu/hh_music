# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/8/3 16:09
"""
mv 视频播放窗口
"""
import os

from PySide6.QtCore import Qt, QUrl, QTimer
from PySide6.QtGui import QIcon
from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import QMainWindow, QSlider, QLabel, QWidget, QSizePolicy, QHBoxLayout, QVBoxLayout

from q_thread.q_thread_tasks import *
from util.utils import format_duration
from widgets.custom_widgets import MyPushButton

resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resource")


class MvPlayWindow(QMainWindow):
    def __init__(self, main_window, mv: Mv):
        super().__init__(main_window)
        self.main_window = main_window
        self.resize(800, 600)
        self.setWindowTitle(mv.name)
        self.mv = mv
        self.initUI()
        self.initMvPlayStatus()
        self.initSlotConnect()

    def initUI(self):
        # 视频播放组件
        self.video_widget = QVideoWidget()
        self.video_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # 初始mv播放化进度条
        self.mv_play_slider = QSlider(Qt.Horizontal)
        self.mv_play_slider.setMinimum(0)
        self.mv_play_slider.setMaximum(100)
        self.mv_play_slider.setValue(0)

        # 播放按钮
        self.play_button = MyPushButton(os.path.join(resource_dir, 'icons/music_play_icon.png'))
        # 文本播放进度
        self.mv_play_progress_label = QLabel()
        # 音量条
        self.volume_button = MyPushButton(os.path.join(resource_dir, 'icons/volume_icon.png'))
        self.volume_slider = QSlider(Qt.Vertical)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)  # set initial volume to 50
        # 初始不可见,点击音量按钮可见
        self.volume_slider.setVisible(False)

        # 保存底部播放栏相关布局
        self.play_status_bar = QWidget()
        # 水平可扩展/垂直不可扩展
        self.play_status_bar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        # 水平布局
        self.play_status_layout = QHBoxLayout(self.play_status_bar)
        self.play_status_layout.addWidget(self.play_button)
        self.play_status_layout.addWidget(self.mv_play_progress_label)
        # 中间可以灵活伸缩
        self.play_status_layout.addStretch()
        self.play_status_layout.addWidget(self.volume_button)
        self.play_status_layout.addWidget(self.volume_slider)

        # 最底部mv信息相关
        self.mv_info_label = QLabel()
        self.mv_info_label.setText(f"""
        <h2>{self.mv.name}</h2><br>
        <div>艺术家:{self.mv.artist}</div><br>
        <div>时长:{self.mv.songTimeMinutes}</div><br>
        <div>播放次数:{self.mv.mvPlayCnt}</div><br>
        """)
        self.mv_info_label.setTextFormat(Qt.TextFormat.RichText)

        # 主布局
        self.main_layout = QVBoxLayout()
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)

        self.main_layout.addWidget(self.video_widget, 20)
        self.main_layout.addWidget(self.mv_play_slider, 1)
        self.main_layout.addWidget(self.play_status_bar, 2)
        self.main_layout.addWidget(self.mv_info_label, 2)

        self.setCentralWidget(self.main_widget)

    def initMvPlayStatus(self):
        """
        初始化MV播放相关
        :return:
        """
        # Media player
        self.media_player = QMediaPlayer()
        # 音频输出
        self.audioOutput = QAudioOutput()
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setAudioOutput(self.audioOutput)
        self.is_mv_url_ready = False

    def initSlotConnect(self):
        self.play_button.clicked.connect(self.on_play_button_clicked)
        # 定时器 使得 播放进度条可以每秒自动更新
        self.mv_play_slider_timer = QTimer()
        self.mv_play_slider_timer.timeout.connect(self.update_mv_play_slider)
        # Start timer
        self.mv_play_slider_timer.start(1000)  # update every 1 second
        # mv的播放进度改变时
        self.media_player.positionChanged.connect(self.update_mv_play_position)
        # 音量滑块
        self.volume_button.clicked.connect(self.toggle_volume_slider)
        # 调整音量
        self.volume_slider.valueChanged.connect(self.set_volume)
        # 用户滑动进度条可以快进/后退 到指定位置
        self.mv_play_slider.sliderMoved.connect(self.mv_play_slider_changed)

    def on_play_button_clicked(self):
        """
        当点击mv播放按钮时
        :return:
        """
        if self.media_player.isPlaying():
            self.media_player.pause()
            self.play_button.setIcon(QIcon(os.path.join(resource_dir, 'icons/music_pause_icon.png')))
        else:
            self.media_player.play()
            self.play_button.setIcon(QIcon(os.path.join(resource_dir, 'icons/music_play_icon.png')))

    def update_mv_play_position(self, position):
        """
        更新mv播放到指定位置
        :param position:
        :return:
        """
        # position 是当前播放位置，单位是毫秒，转换成秒需要除以1000
        current_position = position // 1000
        # 将秒数转换成 MM:ss 的格式
        formatted_position = format_duration(current_position)
        total_time = self.mv.songTimeMinutes
        self.mv_play_progress_label.setText(f"{formatted_position}/{total_time}")

    def update_mv_play_slider(self):
        """
        更新mv播放进度条
        :return:
        """
        if self.media_player.isPlaying():
            self.mv_play_slider.setValue(self.media_player.position())

    def toggle_volume_slider(self):
        """
        设置音量可见
        :return:
        """
        self.volume_slider.setVisible(not self.volume_slider.isVisible())

    def set_volume(self, volume=50):
        """
        设置音量为给定的值
        :param volume: 音量数值
        :return:
        """
        self.audioOutput.setVolume(volume)

    def mv_play_slider_changed(self, value):
        """
        监听mv播放滑块的移动
        :param value:
        :return:
        """
        self.media_player.setPosition(value)

    def set_mv_source(self, url):
        self.is_mv_url_ready = True
        self.media_player.setSource(QUrl(url))
        self.media_player.play()
        # 更新进度条的大小
        self.mv_play_slider.setMaximum(self.mv.duration * 1000)
        self.mv_play_slider.setValue(0)
        # 关闭音乐的播放
        self.main_window.main_window.main_window.main_window.core_music_player.pause_music()

    def load_mv_url_async(self):
        # 避免重复加载
        if self.is_mv_url_ready:
            return
        # 异步加载 mv url
        mv_url_worker = MvUrlWorker(self.mv.id)
        mv_url_worker.mv_url.connect(self.set_mv_source)
        mv_url_worker.finished.connect(lambda: mv_url_worker.deleteLater())
        mv_url_worker.start()

    def closeEvent(self, event):
        """
        主窗口被关闭时会调用
        :param event:
        :return:
        """
        # 在这里添加你的清理代码
        # 关闭mv的播放
        self.media_player.pause()
        # 窗口关闭时,恢复音乐的播放
        core_music_player = self.main_window.main_window.main_window.main_window.core_music_player
        if not core_music_player.main_window.player.isPlaying():
            core_music_player.play_music()
