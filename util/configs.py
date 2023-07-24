# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/24 10:00
"""
配置相关
"""
import json
import os
import shutil

resource_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "resource")


def _get_user_music_config_path():
    """
    获取用户配置文件
    :return:
    """
    return os.path.join(os.path.expanduser("~"), ".hh_music.config")


def _get_default_music_config_path():
    """
    默认配置文件路径
    :return:
    """
    return "../config/hh_music_default.config"


def _cp_music_config_file():
    """
    如果用户配置文件不存在,则拷贝默认配置文件到用户配置文件
    :return:
    """
    user_config_path = _get_user_music_config_path()
    default_config_path = _get_default_music_config_path()
    if not os.path.exists(user_config_path):
        shutil.copy(default_config_path, user_config_path)
    return user_config_path


def load_music_config():
    """
    加载音乐相关配置
    :return:
    """
    user_config_path = _cp_music_config_file()
    with open(user_config_path, "r", encoding="utf-8") as fin:
        return json.load(fin)


def save_music_config(**kwargs):
    """
    保存配置文件到用户配置,只覆盖已有的参数
    :param kwargs:
    :return:
    """
    user_config = load_music_config()
    for k, v in kwargs.items():
        if k in user_config:
            user_config[k] = v
    user_config_path = _get_user_music_config_path()
    with open(user_config_path, "w", encoding="utf-8") as fout:
        json.dump(user_config, fout, ensure_ascii=False, indent=4)
