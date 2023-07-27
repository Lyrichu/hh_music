# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/27 00:31
from enum import Enum


class MusicPlayingOrder(Enum):
    PLAY_IN_ORDER = 1  # 顺序播放
    PLAY_IN_CYCLE = 2  # 单曲循环
    PLAY_IN_RANDOM = 3  # 随机播放
