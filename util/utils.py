# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/21 15:07
import os
import time
from functools import wraps
import warnings

from PySide6.QtGui import QFont, QFontDatabase

resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resource")


def deprecated(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        warnings.warn(f"{func.__name__} is deprecated and will be removed in a future version.", DeprecationWarning)
        return func(*args, **kwargs)

    return wrapper


def format_duration(seconds):
    """Convert duration from seconds to MM:ss format."""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes:02d}:{seconds:02d}"


def get_cur_record_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_custom_font(font_path="font/ZiYuYongSongTi-2.ttf", font_size=12):
    font_id = QFontDatabase.addApplicationFont(os.path.join(resource_dir, font_path))
    # 获取字体名称
    font_families = QFontDatabase.applicationFontFamilies(font_id)
    # 使用字体
    font = QFont(font_families[0], font_size)
    return font
