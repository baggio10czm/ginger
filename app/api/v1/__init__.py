"""
 User: Czm
 Date: 2021/11/5
 Time: 17:15
 Describe:
"""
from flask import Blueprint
from app.api.v1 import user, book, client, token, gift


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    # 红图注册在蓝图里
    user.api.register(bp_v1)
    book.api.register(bp_v1)
    client.api.register(bp_v1)
    token.api.register(bp_v1)
    gift.api.register(bp_v1)

    return bp_v1
