# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 22:26
"""
歌手热门歌曲窗口
"""
from core.core_music_search import CoreMusicSearch
from music_meta.music_meta import MusicPlayStatus
from q_thread.q_thread_tasks import SingerHotMusicWorker
from window.music_searcher_window import MusicSearcher
from window.template_window.base_template_window import BaseTemplateWindow


class SingerHotMusicWindow(BaseTemplateWindow):
    def __init__(self, main_window):
        super().__init__(main_window)
        self.initPlayStatus()
        self.initUI()

    def initUI(self):
        super().initUI()
        # 用于展示歌手热门歌曲
        self.music_table = MusicSearcher.createMusicTable(self.main_window.main_window, 0, 3, ["歌曲", "专辑", "时长"])
        self.layout.addWidget(self.music_table)

    def initPlayStatus(self):
        """
        初始化音乐播放状态
        :return:
        """
        self.music_play_status = MusicPlayStatus()

    def show_window(self):
        self.add_singer_hot_music_to_music_table()
        self.main_window.stacked_widget.setCurrentWidget(self.main_window.singer_hot_music_window)
        self.main_window.main_window.stacked_widget.setCurrentWidget(self.main_window)

    def add_singer_hot_music_to_music_table(self):
        """
        将歌手的热门歌曲添加到 music_table
        :return:
        """
        music_status = self.main_window.main_window.getCurMusicPlayStatus()
        singer_id = music_status.music_data[music_status.play_music_index].artistid
        self.singer_hot_music_worker = SingerHotMusicWorker(singer_id)
        self.singer_hot_music_worker.singer_hot_musics.connect(self._update_music_table)
        # 确保任务完成，线程被销毁
        self.singer_hot_music_worker.finished.connect(lambda: self.singer_hot_music_worker.deleteLater())
        self.singer_hot_music_worker.start()

    def _update_music_table(self, music_datas):
        """
        从后台任务接受数据更新 music_table
        :param music_datas:音乐数据列表
        :return:
        """
        CoreMusicSearch.common_add_music_table_datas(self.music_table, music_datas)
        self.music_table.setVisible(True)
        self.music_play_status = MusicPlayStatus(
            self.music_table,
            music_datas,
            0
        )
        # 启用后台任务
        self.main_window.main_window.search_widget.core_music_search.search_backend_task()
