# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 17:37
"""
mv类
"""
import dataclasses
import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class Mv:
    duration: Optional[int] = None
    artist: Optional[str] = None
    mvPlayCnt: Optional[int] = None
    name: Optional[str] = None
    online: Optional[str] = None
    artistid: Optional[int] = None
    songTimeMinutes: Optional[str] = None
    id: Optional[str] = None
    pic: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

    def to_dict(self):
        return dataclasses.asdict(self)
