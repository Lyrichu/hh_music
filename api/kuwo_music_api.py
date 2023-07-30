# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/27 11:07
"""
酷我音乐 api,参考 https://github.com/QiuYaohong/kuwoMusicApi 在服务器部署了服务
各个接口通过 http 的方式调用
"""
import requests
from const.kuwo_api_constants import *
from const.server_constants import *


def get_kuwo_music_play_url(mid, br: KuwoMusicBr = KuwoMusicBr.BR_128KMP3.value):
    """
    music 播放链接接口
    :param mid: 歌曲id
    :param br: 播放音质
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_MUSIC_PLAY_URL}".format(
        mid=mid, br=br
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_mv_play_url(mid):
    """
    mv 播放链接接口
    :param mid: 歌曲id
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_MV_PLAY_URL}".format(
        mid=mid
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_music_lyric(mid):
    """
    歌词接口
    :param mid: 歌曲id
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_LYRIC}".format(
        musicId=mid
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_music_by_search(key, pn=1, rn=30):
    """
    默认搜索接口(通过关键词搜索歌曲)
    :param key: 关键词
    :param pn: 页数
    :param rn: 一页数量
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_SEARCH}".format(
        key=key, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_music_search_hint(key, pn=1, rn=30):
    """
    关键词获取 搜索提示
    :param key: 关键词
    :param pn: 页数
    :param rn: 一页数量
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_SEARCH_KEY}".format(
        key=key, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_music_by_search_keyword(key, pn=1, rn=30):
    """
    通过关键词搜索歌曲
    :param key: 关键词
    :param pn: 页数
    :param rn: 一页数量
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_SEARCH_MUSIC_BY_KEYWORD}".format(
        key=key, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_album_by_search_keyword(key, pn=1, rn=30):
    """
    通过关键词搜索专辑
    :param key: 关键词
    :param pn: 页数
    :param rn: 一页数量
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_SEARCH_ALBUM_BY_KEYWORD}".format(
        key=key, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_mv_by_search_keyword(key, pn=1, rn=30):
    """
    通过关键词搜索mv
    :param key: 关键词
    :param pn: 页数
    :param rn: 一页数量
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_SEARCH_MV_BY_KEYWORD}".format(
        key=key, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_play_list_by_search_keyword(key, pn=1, rn=30):
    """
    通过关键词搜索歌单
    :param key: 关键词
    :param pn: 页数
    :param rn: 一页数量
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_SEARCH_PLAY_LIST_BY_KEYWORD}".format(
        key=key, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_artist_by_search_keyword(key, pn=1, rn=30):
    """
    通过关键词搜索歌手
    :param key: 关键词
    :param pn: 页数
    :param rn: 一页数量
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_SEARCH_ARTIST_BY_KEYWORD}".format(
        key=key, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_banner():
    """
    酷我音乐轮播图
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_BANNER}"
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_comment(sid,
                     comment_type: KuwoMusicCommentType = KuwoMusicCommentType.HOT_COMMENT.value,
                     page=1,
                     rows=30,
                     digest=KuwoMusicCommentDigest.MUSIC.value
                     ):
    """
    酷我获取评论接口
    :param sid: 评论id
    :param comment_type: 评论类型
    :param page:页数
    :param rows:每页条数
    :param digest:评论来源
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_COMMENT}".format(
        sid=sid, type=comment_type, page=page, rows=rows, digest=digest
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_rec_play_list(rn=1, pn=5):
    """
    推荐歌单
    :param rn: 页数
    :param pn: 每页个数
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_REC_PLAY_LIST}".format(
        rn=rn, pn=pn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_play_list_music(pid, rn=1, pn=30):
    """
    获取歌单音乐列表
    :param pid: 歌单id
    :param rn: 页数
    :param pn: 每页个数
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_PLAY_LIST_MUSIC}".format(
        pid=pid, rn=rn, pn=pn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_default_play_list(order=KuwoMusicDefaultPlayListOrder.HOT.value, pn=1, rn=30):
    """
    获取歌单音乐列表
    :param order: 歌单类型: 最新/最热
    :param pn: 页数
    :param rn: 每页个数
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_DEFAULT_PLAY_LIST}".format(
        order=order, rn=rn, pn=pn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_album_play_list(album_id, pn=1, rn=30):
    """
    歌手专辑歌单
    :param album_id: 专辑id
    :param pn: 页数
    :param rn: 每页个数
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_ALBUM_PLAY_LIST}".format(
        albumId=album_id, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_play_list_tag():
    """
    获取歌单分类tag
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_PLAY_LIST_TAG}"
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_play_list_with_tag(pid, pn=1, rn=30):
    """
    获取带有某个tag的歌单详情
    :param pid: 歌单id
    :param pn: 页数
    :param rn: 一页个数
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_PLAY_LIST_WITH_TAG}".format(
        id=pid, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_all_singer(category: KuwoMusicAllSingerCategory = KuwoMusicAllSingerCategory.ALL.value, pn=1, rn=100,
                        prefix='A'):
    """
    全部歌手
    :param category: 歌手类型
    :param pn: 页数
    :param rn: 每页个数
    :param prefix:歌手名字首字母:A-Z
    :return:
    """
    A_Z = [chr(i) for i in range(ord('A'), ord('A') + 26)]
    prefix = prefix if prefix in A_Z else 'A'
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_ALL_SINGER}".format(
        category=category, pn=pn, rn=rn, prefix=prefix
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_all_singer_music(artist_id, pn=1, rn=30):
    """
    获取歌手的全部单曲
    :param artist_id:歌手id
    :param pn:页数
    :param rn:一页个数
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_ALL_SINGER_MUSIC}".format(
        artistid=artist_id, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_all_singer_album(artist_id, pn=1, rn=30):
    """
    获取歌手的全部专辑
    :param artist_id:歌手id
    :param pn:页数
    :param rn:一页个数
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_ALL_SINGER_ALBUM}".format(
        artistid=artist_id, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_all_singer_mv(artist_id, pn=1, rn=30):
    """
    获取歌手的全部mv
    :param artist_id:歌手id
    :param pn:页数
    :param rn:一页个数
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_ALL_SINGER_MV}".format(
        artistid=artist_id, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_rec_singer(category: KuwoMusicRecSingerCategory = KuwoMusicRecSingerCategory.CHINESE, pn=1, rn=6):
    """
    歌手推荐
    :param category: 歌手类型
    :param pn: 页数
    :param rn: 一页个数
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_REC_SINGER}".format(
        category=category, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_music_info(mid):
    """
    获取音乐信息
    :param mid: 音乐id
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_MUSIC_INFO}".format(
        mid=mid
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_rank_list():
    """
    排行榜单
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_RANK_LIST}"
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_rank_list_music(bang_id, pn=1, rn=30):
    """
    某个排行榜上的音乐
    :param bang_id: 榜单id
    :param pn: 页数
    :param rn: 一页个数
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_RANK_LIST_MUSIC}".format(
        bangId=bang_id, pn=pn, rn=rn
    )
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_rec_rank_list():
    """
    推荐榜单
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_REC_RANK_LIST}"
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()


def get_kuwo_radio():
    """
    主播电台
    :return:
    """
    url = f"http://{UK_SERVER_HOST}:{KUWO_API_SERVER_PORT}{KUWO_API_HTTP_INTERFACE_RADIO}"
    return requests.get(url, timeout=KUWO_HTTP_REQ_TIMEOUT_SECONDS).json()