# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 22:26
"""
歌手全部音乐窗口
"""
from collections import defaultdict
from threading import Lock

from core.core_music_search import CoreMusicSearch
from music_meta.music_meta import MusicPlayStatus
from q_thread.q_thread_tasks import SingerMusicWorker
from window.music_searcher_window import MusicSearcher
from window.template_window.base_template_window import BaseTemplateWindow


class SingerMusicWindow(BaseTemplateWindow):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.initResources()
        self.initPlayStatus()
        self.initUI()

    def initUI(self):
        super().initUI()
        # 展示歌手全部歌曲
        self.music_table = MusicSearcher.createMusicTable(self.main_window.main_window, 0, 3, ["歌曲", "专辑", "时长"])
        self.layout.addWidget(self.music_table)

    def initPlayStatus(self):
        """
        初始化音乐播放状态
        :return:
        """
        # 用来防止重复加载数据
        self.is_loading = False
        self.music_play_status = MusicPlayStatus()

    def initResources(self):
        # 音乐缓存数据
        self.music_cache = defaultdict(dict)

    def show_window(self):
        # 避免重复加载
        singer_id = self.main_window.main_window.getCurMusic().artistid
        if singer_id not in self.music_cache or "music_play_status" not in self.music_cache[singer_id]:
            self.show_progress_dialog()
            # 注意新的歌手需要重置 music_table
            self.append_singer_music_to_music_table(True)
        else:
            self.music_play_status = self.music_cache[singer_id]["music_play_status"]
            self.music_table = self.music_play_status.music_table
            # 重置搜索结果
            self._update_music_table(self.music_play_status.music_data, True)
            total_cnt = self.music_cache[singer_id]["total_musics"]
            self.update_singer_music_header_label(total_cnt)

        self.main_window.stacked_widget.setCurrentWidget(self)

    def append_singer_music_to_music_table(self, reset=False):
        """
        将歌手的歌曲追加到 music_table
        :param reset: 是否需要重置 music_table(比如当切换到新的歌手时)
        :return:
        """
        if self.is_loading:
            return
        self.is_loading = True
        singer_id = self.main_window.main_window.getCurMusic().artistid
        if "current_page" not in self.music_cache[singer_id]:
            current_page = 1
            self.music_cache[singer_id]["current_page"] = current_page
        else:
            current_page = self.music_cache[singer_id]["current_page"]
        singer_music_worker = SingerMusicWorker(singer_id, current_page)
        singer_music_worker.singer_musics.connect(lambda music_datas: self._update_music_table(music_datas, reset))
        singer_music_worker.total_musics.connect(self.update_singer_music_header_label)
        # 确保任务完成，线程被销毁
        singer_music_worker.finished.connect(lambda: singer_music_worker.deleteLater())
        singer_music_worker.start()
        self.is_loading = False

    def update_singer_music_header_label(self, total_cnt):
        """

        :param total_cnt:
        :return:
        """
        self.main_window.singer_header_music_label.setText(f"歌曲{total_cnt}")
        self.add_singer_total_musics_to_cache(total_cnt)

    def _update_music_table(self, music_datas, reset=False):
        """
        从后台任务接受数据更新 music_table,注意这里是追加音乐数据
        :param music_datas:音乐数据列表
        :param reset: 是否重置 music_table
        :return:
        """
        if len(music_datas) == 0:
            self.close_progress_dialog()
            self.task_failed_warning()
            return
        CoreMusicSearch.common_add_music_table_datas(self.music_table, music_datas, not reset)
        self.music_table.setVisible(True)
        if self.music_play_status.music_table is None or reset:
            self.music_play_status = MusicPlayStatus(
                self.music_table,
                music_datas,
                0
            )
        else:
            self.music_play_status.music_data.extend(music_datas)
            # 更新页数
            self.update_current_page_to_cache()
        # 启用后台任务
        self.main_window.main_window.search_widget.core_music_search.search_backend_task()
        # 添加到缓存
        self.add_music_play_status_to_cache()
        self.close_progress_dialog()

    def add_music_play_status_to_cache(self):
        """
        缓存播放状态
        """
        singer_id = self.main_window.main_window.getCurMusic().artistid
        self.music_cache[singer_id]["music_play_status"] = self.music_play_status

    def update_current_page_to_cache(self):
        """
        更新缓存歌手当前音乐加载页数
        """
        singer_id = self.main_window.main_window.getCurMusic().artistid
        self.music_cache[singer_id]["current_page"] += 1

    def add_singer_total_musics_to_cache(self, total_musics):
        """
        缓存歌手音乐总数
        """
        singer_id = self.main_window.main_window.getCurMusic().artistid
        self.music_cache[singer_id]["total_musics"] = total_musics
