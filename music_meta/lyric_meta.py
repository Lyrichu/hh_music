# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/27 17:31
"""
歌词类
"""


class Lyric:
    def __init__(self, time: float, line_lyric: str):
        """
        歌词
        :param time:歌词时间
        :param line_lyric:时间对应歌词
        """
        self.time = time
        self.line_lyric = line_lyric

    @staticmethod
    def lyrics_from_dict(data_dict):
        """
        从 dict 解析 得到 list[Lyric]
        :return: list[Lyric]
        """
        lrc_list = data_dict["data"]["lrclist"]
        lyrics = []
        for lrc in lrc_list:
            lyrics.append(Lyric(float(lrc["time"]), lrc["lineLyric"]))
        return lyrics
