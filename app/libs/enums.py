"""
 User: Czm
 Date: 2021/11/6
 Time: 14:03
 Describe:
"""
from enum import Enum


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201

