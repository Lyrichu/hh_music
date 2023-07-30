# -*- coding:utf-8 -*-
# author:lyrichu@foxmail.com
# @Time: 2023/7/28 22:49
"""
歌手基本信息
"""

import dataclasses
import json
from dataclasses import dataclass
from typing import Optional


@dataclass
class Singer:
    name: Optional[str] = None
    country: Optional[str] = None
    pic: Optional[str] = None
    musicNum: Optional[int] = None
    pic120: Optional[str] = None
    isStar: Optional[int] = None
    content_type: Optional[str] = None
    pic70: Optional[str] = None
    id: Optional[int] = None
    pic300: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)

    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(**data)

    def to_dict(self):
        return dataclasses.asdict(self)
