# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 17:05
"""
专辑类
"""
import dataclasses
import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class Album:
    content_type: Optional[str] = None
    albuminfo: Optional[str] = None
    artist: Optional[str] = None
    releaseDate: Optional[str] = None
    album: Optional[str] = None
    albumid: Optional[int] = None
    pay: Optional[int] = None
    artistid: Optional[int] = None
    pic: Optional[str] = None
    isstar: Optional[int] = None
    lang: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

    def to_dict(self):
        return dataclasses.asdict(self)
