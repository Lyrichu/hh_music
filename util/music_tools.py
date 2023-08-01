# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/24 10:09
"""
音乐工具类
"""
import glob
import os
import traceback

import requests

from music_meta.music_meta import MusicWithTime, Music
from util.configs import load_music_config
from util.utils import deprecated
from util.logs import LOGGER
from api.kuwo_music_api import *


def search_kuwo_music_by_keywords(keywords, pn=1, rn=20, add_play_url=False):
    """
    通过关键词搜索酷我音乐
    :param keywords: 关键词
    :param pn: 页数
    :param rn: 一页返回数量
    :param add_play_url: 是否要额外加载音乐下载链接
    :return:
    """
    try:
        json_data = get_kuwo_music_by_search(keywords, pn, rn)
        if json_data["code"] != 200:
            return 0, []
        total = int(json_data["data"]["total"])
        return total, get_music_search_list(json_data, add_play_url)
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        return 0, []


@deprecated
def search_kuwo_music_by_keywords1(keywords, pn=1, rn=20, add_play_url=False):
    """
    通过关键词搜索酷我音乐(早期接口,已废弃,请通过api模块的接口调用)
    :param keywords: 关键词
    :param pn: 页数
    :param rn: 一页返回数量
    :param add_play_url: 是否要额外加载音乐下载链接
    :return:
    """
    try:
        kuwo_music_search_url = "https://kuwo.cn/api/www/search/searchMusicBykeyWord?" \
                                f"key={keywords}&pn={pn}&rn={rn}" \
                                f"&httpsStatus=1&reqId=fe306351-066d-11ee-a729-c7b3050f31b5"
        music_config = load_music_config()
        headers = music_config.get("headers", None)
        proxies = music_config.get("proxies", None)
        rsp = requests.get(url=kuwo_music_search_url, headers=headers, proxies=proxies)
        json_data = rsp.json()
        if json_data["code"] != 200:
            return 0, []
        total = int(json_data["data"]["total"])
        return total, get_music_search_list(json_data, add_play_url)
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        return 0, []


def get_music_download_url_by_mid(mid):
    """
    通过mid 获取 酷我音乐 下载链接
    :param mid:
    :return:
    """
    try:
        json_data = get_kuwo_music_play_url(mid)
        if json_data["code"] != 200:
            return None
        else:
            return json_data["data"]["url"]
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        return None


@deprecated
def get_music_download_url_by_mid1(mid):
    """
    通过mid 获取 酷我音乐 下载链接(早期接口,已废弃,请通过api模块的接口调用)
    :param mid:
    :return:
    """
    try:
        kuwo_music_info_url = f"https://kuwo.cn/api/v1/www/music/playUrl?mid={mid}&type=music&httpsStatus=1&reqId=8b6a0650-36fd-11ec-970b-9d2518c9e2df"
        music_config = load_music_config()
        headers = music_config.get("headers", None)
        rsp = requests.get(kuwo_music_info_url, timeout=10, headers=headers)
        json_data = rsp.json()
        if json_data["code"] != 200:
            return None
        else:
            return json_data["data"]["url"]
    except Exception as e:
        LOGGER.error(traceback.format_exc())
        return None


def _get_user_music_history_play_list_file():
    """
    获取用户历史播放列表保存文件
    :return:
    """
    user_config = load_music_config()
    music_history_play_list_file = user_config["music_history_play_list_file"]
    if music_history_play_list_file == "":
        music_history_play_list_file = os.path.join(os.path.expanduser("~"),
                                                    ".hh_music_history_play_list.data")
    return music_history_play_list_file


def load_user_downloaded_music_names():
    """
    获取用户已经下载的音乐文件名称列表
    :return:
    """
    user_config = load_music_config()
    music_download_dir = user_config["music_download_dir"]
    if music_download_dir == "":
        music_download_dir = os.path.expanduser("~")
        user_config["music_download_dir"] = music_download_dir
    music_files = glob.glob(os.path.join(music_download_dir, "*.mp3"))
    return [os.path.basename(f) for f in music_files]


def load_user_history_music_play_list_from_file():
    """
    从文件获取用户音乐收听历史列表(由远及近)
    :return:
    """
    his_play_list = []
    music_history_play_list_file = _get_user_music_history_play_list_file()
    if os.path.exists(music_history_play_list_file):
        with open(music_history_play_list_file, "r", encoding="utf-8") as fin:
            for line in fin:
                his_play_list.append(MusicWithTime.from_str(line.strip()))
    return his_play_list


def write_to_user_history_music_play_list_file(play_list: list[MusicWithTime]):
    """
    历史播放列表写入本地文件,每行为一个 json,MusicWithTime格式
    :param play_list:
    :return:
    """
    music_history_play_list_file = _get_user_music_history_play_list_file()
    with open(music_history_play_list_file, "w") as fout:
        for data in play_list:
            fout.write(f"{data.to_json()}\n")


def get_music_search_list(data: dict, add_play_url=False) -> list[Music]:
    """
    从 data 获取 Music 列表
    :param data:
    :param add_play_url:
    :return:
    """
    if data["code"] != 200:
        return []
    musics = []
    for info in data["data"]["list"]:
        music = Music.from_dict(info)
        if add_play_url:
            play_url = get_music_download_url_by_mid(music.rid)
            music.play_url = play_url
        musics.append(music)
    return musics
