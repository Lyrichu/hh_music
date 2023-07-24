# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/22 13:44
import os.path
import traceback
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

import requests
from PySide6.QtCore import QThread, QObject, Signal
from PySide6.QtWidgets import *

from util.logs import LOGGER
from widgets.custom_widgets import MyPushButton

resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resource")


class DownloadWorker(QObject):
    # (status,url)
    finished_signal = Signal(bool, str)

    def __init__(self, url, download_path):
        super().__init__()
        self.url = url
        self.download_path = download_path

    def run(self):
        # Do the download here
        status = self.download_single_file(self.url, self.download_path)
        # Emit the signal when the task is finished
        self.finished_signal.emit(status, self.url)

    def download_single_file(self, url, save_path):
        try:
            rsp = requests.get(url, timeout=10)
            with open(save_path, "wb") as fout:
                fout.write(rsp.content)
            LOGGER.info(f"save {url} to {save_path} succeed!")
            return True
        except Exception as e:
            LOGGER.error(traceback.format_exc())
            return False


class DownloadManager(QThread):
    # (succeed_tasks,failed_tasks,total_tasks,url,url_succeed)
    progress_signal = Signal(int, int, int, str, bool)

    def __init__(self, url_list, names_list, download_dir, max_workers=10):
        super().__init__()
        self.url_list = url_list
        self.names_list = names_list
        self.download_dir = download_dir
        self.succeed_taks = 0
        self.failed_tasks = 0
        self.total_tasks = len(url_list)
        self.max_workers = max_workers
        self.lock = Lock()

    def run(self):
        assert len(self.url_list) == len(self.names_list)
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for url, name in zip(self.url_list, self.names_list):
                download_path = os.path.join(self.download_dir, name)
                # Create a DownloadThread instance for each file
                worker = DownloadWorker(url, download_path)
                # Connect the signal to a slot function
                worker.finished_signal.connect(self.update_progress)
                # Start the q_thread
                executor.submit(worker.run)

    def update_progress(self, status, url):
        with self.lock:
            if status:
                self.succeed_taks += 1
            else:
                self.failed_tasks += 1
        # Emit the signal with the number of finished tasks
        self.progress_signal.emit(self.succeed_taks, self.failed_tasks, self.total_tasks, url, status)


class DownloadWindow(QMainWindow):
    def __init__(self, main_window):
        super(DownloadWindow, self).__init__(main_window)
        self.main_window = main_window
        self.setWindowTitle("下载任务管理器")

        # Add a label and progress bar
        self.cur_task_label = QLabel("当前任务:", self)
        self.cur_download_all_button = MyPushButton(os.path.join(resource_dir, "icons/all_tasks_icon.png"))
        self.cur_download_all_label = QLabel(self)
        self.cur_download_succeed_button = MyPushButton(os.path.join(resource_dir, "icons/succeed_icon.png"))
        self.cur_download_succeed_label = QLabel(self)
        self.cur_download_failed_button = MyPushButton(os.path.join(resource_dir, "icons/failed_icon.png"))
        self.cur_download_failed_label = QLabel(self)
        self.cur_task_download_progress_bar = QProgressBar(self)

        # Create a layout and add the label and progress bar to it
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.cur_task_label)
        self.layout.addWidget(self.cur_download_all_button)
        self.layout.addWidget(self.cur_download_all_label)
        self.layout.addWidget(self.cur_download_succeed_button)
        self.layout.addWidget(self.cur_download_succeed_label)
        self.layout.addWidget(self.cur_download_failed_button)
        self.layout.addWidget(self.cur_download_failed_label)
        self.layout.addWidget(self.cur_task_download_progress_bar)

        # Create a widget and set it as the central widget
        self.widget = QWidget(self)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def update_progress(self, succeed, failed, total, url, url_succeed):
        """
        更新下载相关进度
        :param succeed: 下载成功个数
        :param failed: 下载失败个数
        :param total: 总体个数
        :param url: 当前完成下载的 url
        :param url_succeed: 当前 url 是否成功
        :return:
        """
        # Calculate the progress percentage and update the progress bar
        progress_percentage = ((succeed + failed) / total) * 100
        self.cur_task_download_progress_bar.setValue(progress_percentage)
        self.cur_download_all_label.setText(str(total))
        self.cur_download_succeed_label.setText(str(succeed))
        self.cur_download_failed_label.setText(str(failed))

        # 更新主窗口
        all_urls = [music.play_url for music in self.main_window.getCurMusicPlayStatus().music_data]
        if url_succeed and url in all_urls:
            i = all_urls.index(url)
            self.main_window.search_widget.downloaded_music_indexes.add(i)
        # 更新主窗口下载进度
        self.main_window.search_widget.selected_count_button.setText(f"{succeed + failed}/{total}")

    def start_download(self, url_list, names_list, download_dir, max_workers=10):
        # Create a DownloadManager instance
        self.download_manager = DownloadManager(url_list, names_list,
                                                download_dir, max_workers)
        # Connect the signal to a slot function
        self.download_manager.progress_signal.connect(self.update_progress)
        # Start the manager q_thread
        self.download_manager.start()
