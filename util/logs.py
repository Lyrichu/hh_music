# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/24 10:00
"""
日志相关
"""
import os
import sys

from loguru import logger

from util.configs import load_music_config


def get_log_dir():
    """
    获取日志目录
    :return:
    """
    music_config = load_music_config()
    logs_dir = music_config.get("base_dir", None)
    if not logs_dir:
        logs_dir = os.path.expanduser("~")
        music_config["base_dir"] = logs_dir
    return logs_dir


def get_log_file():
    """
    获取日志文件
    :return:
    """
    logs_dir = get_log_dir()
    return os.path.join(logs_dir, ".hh_music.log")


def get_logger():
    # Set up the logger
    logger.remove()
    _format = "{time:YYYY-MM-DD HH:mm:ss} {level} {file} {line}: {message}"
    logger.add(sys.stdout, format=_format, level="INFO")  # logs to stdout
    log_file = get_log_file()
    logger.add(log_file, rotation="500 MB", format=_format)  # logs to a file
    return logger


LOGGER = get_logger()
