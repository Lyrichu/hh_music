# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/27 11:11
"""
酷我音乐 api 相关配置常量,接口文档参考:https://qiuyaohong.github.io/kuwoMusicApi
"""
from enum import Enum

# 服务端口
KUWO_API_SERVER_PORT = 7002

# http 请求超时时间
KUWO_HTTP_REQ_TIMEOUT_SECONDS = 10

# music 播放链接接口
KUWO_API_HTTP_INTERFACE_MUSIC_PLAY_URL = "/kuwo/url?mid={mid}&type=music&br={br}"
# mv 播放链接接口
KUWO_API_HTTP_INTERFACE_MV_PLAY_URL = "/kuwo/url?mid={mid}&type=mv"

# 歌词接口
KUWO_API_HTTP_INTERFACE_LYRIC = "/kuwo/lrc?musicId={musicId}"

# 默认搜索接口(通过关键词搜索歌曲)
KUWO_API_HTTP_INTERFACE_SEARCH = "/kuwo/search/searchMusicBykeyWord?key={key}&pn={pn}&rn={rn}"
# 搜索提示
KUWO_API_HTTP_INTERFACE_SEARCH_KEY = "/kuwo/search/searchKey?key={key}&pn={pn}&rn={rn}"

KUWO_API_HTTP_INTERFACE_SEARCH_MUSIC_BY_KEYWORD = KUWO_API_HTTP_INTERFACE_SEARCH
# 通过关键词搜索专辑
KUWO_API_HTTP_INTERFACE_SEARCH_ALBUM_BY_KEYWORD = "/kuwo/search/searchAlbumBykeyWord?key={key}&pn={pn}&rn={rn}"
# 通过关键词搜索MV
KUWO_API_HTTP_INTERFACE_SEARCH_MV_BY_KEYWORD = "/kuwo/search/searchMvBykeyWord?key={key}&pn={pn}&rn={rn}"
# 通过关键词搜索歌单
KUWO_API_HTTP_INTERFACE_SEARCH_PLAY_LIST_BY_KEYWORD = "/kuwo/search/searchPlayListBykeyWord?key={key}&pn={pn}&rn={rn}"
# 通过关键词搜索歌手
KUWO_API_HTTP_INTERFACE_SEARCH_ARTIST_BY_KEYWORD = "/kuwo/search/searchArtistBykeyWord?key={key}&pn={pn}&rn={rn}"

# 轮播图
KUWO_API_HTTP_INTERFACE_BANNER = "/kuwo/banner"

# 评论
KUWO_API_HTTP_INTERFACE_COMMENT = "/kuwo/comment?sid={sid}&type={type}&page={page}&rows={rows}&digest={digest}"

# 推荐歌单
KUWO_API_HTTP_INTERFACE_REC_PLAY_LIST = "/kuwo/rec_gedan?rn={rn}&pn={pn}"

# 歌单音乐
KUWO_API_HTTP_INTERFACE_PLAY_LIST_MUSIC = "/kuwo/musicList?pid={pid}&rn={rn}&pn={pn}"

# 默认歌单
KUWO_API_HTTP_INTERFACE_DEFAULT_PLAY_LIST = "/kuwo/playList?order={order}&rn={rn}&pn={pn}"

# 歌手专辑歌单
KUWO_API_HTTP_INTERFACE_ALBUM_PLAY_LIST = "/kuwo/albumInfo?albumId={albumId}&{rn}&pn={pn}"

# 歌单分类tag
KUWO_API_HTTP_INTERFACE_PLAY_LIST_TAG = "/kuwo/getTagList"

# 某个tag的歌单
KUWO_API_HTTP_INTERFACE_PLAY_LIST_WITH_TAG = "/kuwo/playList/getTagPlayList?id={id}&{rn}&pn={pn}"

# 全部歌手
KUWO_API_HTTP_INTERFACE_ALL_SINGER = "/kuwo/singer?category={category}&rn={rn}&pn={pn}&prefix={prefix}"

# 歌手单曲
KUWO_API_HTTP_INTERFACE_ALL_SINGER_MUSIC = "/kuwo/singer/music?artistid={artistid}&rn={rn}&pn={pn}"

# 歌手专辑
KUWO_API_HTTP_INTERFACE_ALL_SINGER_ALBUM = "/kuwo/singer/album?artistid={artistid}&rn={rn}&pn={pn}"

# 歌手MV
KUWO_API_HTTP_INTERFACE_ALL_SINGER_MV = "/kuwo/singer/mv?artistid={artistid}&rn={rn}&pn={pn}"

# 歌手推荐
KUWO_API_HTTP_INTERFACE_REC_SINGER = "/kuwo/rec_singer?category={category}&rn={rn}&pn={pn}"

# 音乐信息
KUWO_API_HTTP_INTERFACE_MUSIC_INFO = "/kuwo/musicInfo?mid={mid}"

# 排行榜单
KUWO_API_HTTP_INTERFACE_RANK_LIST = "/kuwo/rank"

# 某个排行榜上的音乐
KUWO_API_HTTP_INTERFACE_RANK_LIST_MUSIC = "/kuwo/rank/musicList?bangId={bangId}&pn={pn}&rn={rn}"

# 推荐榜单
KUWO_API_HTTP_INTERFACE_REC_RANK_LIST = "/kuwo/rank/rec_bangList"

# 主播电台
KUWO_API_HTTP_INTERFACE_RADIO = "/kuwo/radio"


# 一些枚举常量
class KuwoMusicBr(Enum):
    """
    播放音质：可选 128kmp3、192kmp3、320kmp3
    """
    BR_128KMP3 = "128kmp3"
    BR_192KMP3 = "192kmp3"
    BR_320KMP3 = "320kmp3"


class KuwoMusicCommentType(Enum):
    """
    酷我音乐评论类型
    """
    HOT_COMMENT = "get_rec_comment"
    NEW_COMMENT = "get_comment"


class KuwoMusicCommentDigest(Enum):
    """
    酷我音乐评论来源
    """
    MUSIC = 15
    RANK = 2
    MV = 7
    PLAY_LIST = 8


class KuwoMusicDefaultPlayListOrder(Enum):
    """
    酷我音乐默认歌单类型
    """
    NEW = "new"  # 最新
    HOT = "hot"  # 最热


class KuwoMusicAllSingerCategory(Enum):
    """
    酷我音乐全部歌手类别
    """
    ALL = 0  # 全部
    CHINESE_MALE = 1  # 华语男
    CHINESE_FEMALE = 2  # 华语女
    CHINESE_GROUP = 3  # 华语组合
    JP_KR_MALE = 4  # 日韩男
    JP_KR_FEMALE = 5  # 日韩女
    JP_KR_GROUP = 6  # 日韩组合
    EU_US_MALE = 7  # 欧美男
    EU_US_FEMALE = 8  # 欧美女
    EU_US_GROUP = 9  # 欧美组合
    OTHERS = 10  # 其他


class KuwoMusicRecSingerCategory(Enum):
    """
    酷我音乐推荐歌手类别
    """
    CHINESE = 11  # 华语
    EU_US = 13  # 欧美
    JP_KR = 12  # 日韩
    GROUP = 16  # 组合


