# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/8/2 15:42
"""
mv 相关的自定义组件
"""
from PySide6.QtCore import QPoint, Qt, QLineF, QUrl
from PySide6.QtGui import QPixmap, QPen, QBrush, QPolygon, QPainter
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PySide6.QtWidgets import QLabel

from music_meta.mv_meta import Mv
from widgets.custom_widgets import ClickableLabel, HoverColorNameLabel
from window.mv_play_window import MvPlayWindow
from window.template_window.base_template_window import BaseTemplateWindow


class MvCoverWidgets(BaseTemplateWindow):
    """
    mv展示组件,包括mv封面，信息文字等
    """

    def __init__(self, main_window, mv: Mv, mv_cover_size=(200, 200)):
        """
        :param main_window:
        :param mv: Mv类
        :param mv_cover_size: mv封面大小
        """
        super().__init__(main_window)
        self.main_window = main_window
        self.mv = mv
        self.mv_cover_size = mv_cover_size
        self.mv_window = MvPlayWindow(self, self.mv)
        self.initUI()
        self.initSlotConnect()

    def initUI(self):
        super().initUI()
        # mv 封面
        self.mv_cover_label = MvCoverLabel(self, self.mv.pic, self.mv_cover_size)
        self.mv_cover_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # mv 名字
        self.mv_name_label = HoverColorNameLabel(self, self.mv.name)
        self.mv_name_label.setMaximumWidth(self.mv_cover_size[0])
        self.mv_name_label.setTextFormat(Qt.TextFormat.RichText)  # 设置文本格式为 RichText
        self.mv_name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # mv 时长
        self.mv_duration_label = QLabel(f"时长:{self.mv.songTimeMinutes}")
        self.mv_duration_label.setMaximumWidth(self.mv_cover_size[0])
        self.mv_duration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # mv 播放次数
        self.mv_play_cnt_label = QLabel(f"播放次数:{self.mv.mvPlayCnt}")
        self.mv_play_cnt_label.setMaximumWidth(self.mv_cover_size[0])
        self.mv_play_cnt_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.layout.addWidget(self.mv_cover_label)
        self.layout.addWidget(self.mv_name_label)
        self.layout.addWidget(self.mv_duration_label)
        self.layout.addWidget(self.mv_play_cnt_label)

    def initSlotConnect(self):
        self.mv_cover_label.clicked.connect(self.show_mv_window)
        self.mv_name_label.clicked.connect(self.show_mv_window)

    def show_mv_window(self):
        """
        展示mv窗口
        :return:
        """
        self.mv_window.load_mv_url_async()
        self.mv_window.show()


class MvCoverLabel(ClickableLabel):
    def __init__(self, main_window, cover_url, mv_size=(200, 200)):
        """
        mv封面
        :param main_window: 
        :param cover_url: mv封面 url
        :param mv_size label 尺寸
        """
        super().__init__(main_window)
        self.main_window = main_window
        self.cover_url = cover_url
        self.mv_size = mv_size
        self.setFixedSize(*self.mv_size)
        self.mv_pixmap = QPixmap()
        self.setPixmap(self.mv_pixmap)
        self.mouse_over_circle = False
        # 原始pixmap 是否已经准备好了
        self.is_mv_pixmap_ready = False
        self.setMouseTracking(True)
        # 用于加载mv封面
        self.network_manager = QNetworkAccessManager()
        # 首先尝试从缓存加载
        if self.main_window.mv.id in self.main_window.main_window.mv_cover_cache:
            pixmap = self.main_window.main_window.mv_cover_cache[self.main_window.mv.id]
            self.setPixmap(pixmap)
            self.mv_pixmap = pixmap
            self.is_mv_pixmap_ready = True
        else:
            self.set_mv_pixmap()

    def draw_circle_and_triangle(self, painter, circle_color):
        center = self.mv_pixmap.rect().center()
        radius = min(self.mv_pixmap.width(), self.mv_pixmap.height()) * 0.2

        # 绘制圆形
        pen = QPen(circle_color)
        brush = QBrush(circle_color)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawEllipse(center, radius, radius)

        # 计算三角形的顶点位置
        side_length = radius * 0.6
        triangle = QPolygon([
            center + QPoint(-side_length / 2, side_length / 2),
            center + QPoint(side_length / 2, side_length / 2),
            center + QPoint(0, -side_length / 2)
        ])

        # 绘制黑色三角形
        pen = QPen(Qt.black)
        brush = QBrush(Qt.black)
        painter.setPen(pen)
        painter.setBrush(brush)
        painter.drawPolygon(triangle)

    def create_hover_pixmap(self, circle_color=Qt.white):
        hover_pixmap = self.mv_pixmap.copy()
        painter = QPainter(hover_pixmap)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_circle_and_triangle(painter, circle_color)

        painter.end()
        return hover_pixmap

    def update_hover_pixmap(self):
        if self.mouse_over_circle:
            circle_color = Qt.green
        else:
            circle_color = Qt.white

        self.hover_pixmap = self.create_hover_pixmap(circle_color)
        self.setPixmap(self.hover_pixmap)

    def mouseMoveEvent(self, event):
        if not self.is_mv_pixmap_ready:
            return
        center = self.mv_pixmap.rect().center()
        radius = min(self.mv_pixmap.width(), self.mv_pixmap.height()) * 0.2

        # 计算鼠标位置与圆心的距离
        distance_to_center = QLineF(center, event.pos()).length()

        # 如果鼠标在圆形内部，更改鼠标在圆形上的状态
        if distance_to_center <= radius:
            self.mouse_over_circle = True
        else:
            self.mouse_over_circle = False

        self.update_hover_pixmap()

    def enterEvent(self, event):
        super().enterEvent(event)
        if not self.is_mv_pixmap_ready:
            return
        self.mouse_over_circle = False
        self.update_hover_pixmap()
        self.setStyleSheet("border: 3px solid green;")

    def leaveEvent(self, event):
        if not self.is_mv_pixmap_ready:
            return
        self.mouse_over_circle = False
        self.setPixmap(self.mv_pixmap)
        self.setStyleSheet("")

    def set_mv_pixmap(self):
        request = QNetworkRequest(QUrl(self.cover_url))
        reply = self.network_manager.get(request)
        reply.finished.connect(lambda: self.on_download_mv_cover_finished(reply))

    def on_download_mv_cover_finished(self, reply):
        """
        当通过url加载完成mv封面时
        :param reply
        :return:
        """
        data = reply.readAll()
        self.mv_pixmap.loadFromData(data)
        pixmap = self.mv_pixmap.scaled(*self.mv_size, Qt.KeepAspectRatio)
        self.setPixmap(pixmap)
        # 添加到缓存
        self.main_window.main_window.mv_cover_cache[self.main_window.mv.id] = pixmap
        self.mv_pixmap = pixmap
        self.is_mv_pixmap_ready = True
