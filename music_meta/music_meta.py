# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/21 14:16
import json


class Music:
    """
    核心音乐类
    """

    def __init__(self, musicrid, artist, pic, duration, release_date, album, name,
                 barrage, ad_type, mvpayinfo, isstar, rid, score100, ad_subtype, content_type,
                 track, hasLossless, hasmv, albumid, pay, artistid, albumpic,
                 originalsongtype, songTimeMinutes, isListenFee, pic120, online,
                 payInfo, tme_musician_adtype, play_url=None):
        """

        :param musicrid:
        :param artist:
        :param pic:
        :param duration:
        :param release_date:
        :param album:
        :param name:
        :param barrage:
        :param ad_type:
        :param mvpayinfo:
        :param isstar:
        :param rid:
        :param score100:
        :param ad_subtype:
        :param content_type:
        :param track:
        :param hasLossless:
        :param hasmv:
        :param albumid:
        :param pay:
        :param artistid:
        :param albumpic:
        :param originalsongtype:
        :param songTimeMinutes:
        :param isListenFee:
        :param pic120:
        :param online:
        :param payInfo:
        :param tme_musician_adtype:
        :param play_url:
        """
        self.musicrid = musicrid
        self.artist = artist
        self.pic = pic
        self.duration = duration
        self.release_date = release_date
        self.album = album
        self.name = name
        self.barrage = barrage
        self.ad_type = ad_type
        self.mvpayinfo = mvpayinfo
        self.isstar = isstar
        self.rid = rid
        self.score100 = score100
        self.ad_subtype = ad_subtype
        self.content_type = content_type
        self.track = track
        self.hasLossless = hasLossless
        self.hasmv = hasmv
        self.albumid = albumid
        self.pay = pay
        self.artistid = artistid
        self.albumpic = albumpic
        self.originalsongtype = originalsongtype
        self.songTimeMinutes = songTimeMinutes
        self.isListenFee = isListenFee
        self.pic120 = pic120
        self.online = online
        self.payInfo = payInfo
        self.tme_musician_adtype = tme_musician_adtype
        self.play_url = play_url

    @staticmethod
    def from_dict(data: dict):
        """
        从字典数据构造Music类
        :param data:
        :return:
        """
        musicrid = data.get('musicrid', '')
        artist = data.get('artist', '')
        pic = data.get('pic', '')
        duration = data.get('duration', 0)
        release_date = data.get('releaseDate', '')
        album = data.get('album', '')
        name = data.get('name', '')
        barrage = data.get('barrage', '')
        ad_type = data.get('ad_type', '')
        mvpayinfo = data.get('mvpayinfo', {})
        isstar = data.get('isstar', 0)
        rid = data.get('rid', '')
        score100 = data.get('score100', '0')
        ad_subtype = data.get('ad_subtype', '0')
        content_type = data.get('content_type', '0')
        track = data.get('track', 0)
        hasLossless = data.get('hasLossless', False)
        hasmv = data.get('hasmv', 0)
        albumid = data.get('albumid', 0)
        pay = data.get('pay', '')
        artistid = data.get('artistid', 0)
        albumpic = data.get('albumpic', '')
        originalsongtype = data.get('originalsongtype', 0)
        songTimeMinutes = data.get('songTimeMinutes', '')
        isListenFee = data.get('isListenFee', False)
        pic120 = data.get('pic120', '')
        online = data.get('online', 0)
        payInfo = data.get('payInfo', {})
        tme_musician_adtype = data.get('tme_musician_adtype', '0')

        return Music(musicrid, artist, pic, duration, release_date, album, name,
                     barrage, ad_type, mvpayinfo, isstar, rid, score100, ad_subtype, content_type,
                     track, hasLossless, hasmv, albumid, pay, artistid, albumpic,
                     originalsongtype, songTimeMinutes, isListenFee, pic120, online,
                     payInfo, tme_musician_adtype)

    def to_dict(self):
        """
        Music类转化为字典
        :return:
        """
        data = {
            "musicrid": self.musicrid,
            "artist": self.artist,
            "pic": self.pic,
            "duration": self.duration,
            "release_date": self.release_date,
            "album": self.album,
            "name": self.name,
            "barrage": self.barrage,
            "ad_type": self.ad_type,
            "mvpayinfo": self.mvpayinfo,
            "isstar": self.isstar,
            "rid": self.rid,
            "score100": self.score100,
            "ad_subtype": self.ad_subtype,
            "content_type": self.content_type,
            "track": self.track,
            "hasLossless": self.hasLossless,
            "hasmv": self.hasmv,
            "albumid": self.albumid,
            "pay": self.pay,
            "artistid": self.artistid,
            "albumpic": self.albumpic,
            "originalsongtype": self.originalsongtype,
            "songTimeMinutes": self.songTimeMinutes,
            "isListenFee": self.isListenFee,
            "pic120": self.pic120,
            "online": self.online,
            "payInfo": self.payInfo,
            "tme_musician_adtype": self.tme_musician_adtype
        }
        return data

    def from_json(self, json_str: str):
        """
        Create a Music object from a JSON string.
        :param json_str: A JSON string.
        :return: A Music object.
        """
        try:
            data = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError("Invalid JSON string") from e
        return self.from_dict(data)

    def __str__(self):
        return (f"Music ID: {self.musicrid}\n"
                f"Artist: {self.artist}\n"
                f"Cover Image: {self.pic}\n"
                f"Duration: {self.duration} seconds\n"
                f"Release Date: {self.release_date}\n"
                f"Album: {self.album}\n"
                f"Name: {self.name}\n"
                f"Barrage: {self.barrage}\n"
                f"Ad Type: {self.ad_type}\n"
                f"MV Pay Info: {self.mvpayinfo}\n"
                f"Is Star: {self.isstar}\n"
                f"RID: {self.rid}\n"
                f"Score 100: {self.score100}\n"
                f"Ad Subtype: {self.ad_subtype}\n"
                f"Content Type: {self.content_type}\n"
                f"Track: {self.track}\n"
                f"Has Lossless: {self.hasLossless}\n"
                f"Has MV: {self.hasmv}\n"
                f"Album ID: {self.albumid}\n"
                f"Pay: {self.pay}\n"
                f"Artist ID: {self.artistid}\n"
                f"Album Pic: {self.albumpic}\n"
                f"Original Song Type: {self.originalsongtype}\n"
                f"Song Time Minutes: {self.songTimeMinutes}\n"
                f"Is Listen Fee: {self.isListenFee}\n"
                f"Pic 120: {self.pic120}\n"
                f"Online: {self.online}\n"
                f"Pay Info: {self.payInfo}\n"
                f"TME Musician Ad Type: {self.tme_musician_adtype}")

    def __repr__(self):
        return self.__str__()


class MusicWithTime:
    """
    带有时间的音乐组合类
    """

    def __init__(self, music: Music, record_time: str):
        """
        :param music: Music类
        :param record_time: 记录时间
        """
        self.music = music
        self.record_time = record_time

    @staticmethod
    def from_str(s):
        """
        从字符串构造MusicWithTime
        :param s:
        :return:
        """
        d = json.loads(s)
        music = Music.from_dict(d["music"])
        record_time = d["record_time"]
        return MusicWithTime(music, record_time)

    def to_json(self) -> str:
        """
        MusicWithTime 格式化成字符串
        :return:
        """
        d = {
            "music": self.music.to_dict(),
            "record_time": self.record_time
        }
        return json.dumps(d, ensure_ascii=False)


class MusicPlayStatus:
    """
    音乐播放状态类
    """
    def __init__(self, music_table=None, music_data=[], play_music_index=-1, invalid_play_music_indexes=set()):
        """
        :param music_table: 音乐表格数据,一般与music_data 是同步的
        :param music_data: 音乐播放列表数据
        :param play_music_index: 记录当前 播放音乐在 music_data 中的索引,可用于切歌
        :param invalid_play_music_indexes: 记录无法播放的歌曲的索引
        """
        self.music_table = music_table
        self.music_data = music_data
        self.play_music_index = play_music_index
        self.invalid_play_music_indexes = invalid_play_music_indexes
