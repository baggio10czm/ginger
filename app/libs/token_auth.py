"""
 User: Czm
 Date: 2021/11/8
 Time: 15:23
 Describe:
"""
from collections import namedtuple
from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer,BadSignature, SignatureExpired

from app.libs.error_code import AuthFailed, Forbidden
from app.libs.scope import is_in_scope

# 用 HTTPTokenAuth 貌似更简单,只需传token
# Authorization 对应的是 BearerToken
# auth = HTTPTokenAuth()
auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'ac_type', 'scope'])


# @auth.verify_token
@auth.verify_password
def verify_password(token, password):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        # 用g变量保存,方面全局调用(方便、安全)
        g.user = user_info
        return True


def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise AuthFailed(msg='token无效', error_code=1002)
    except SignatureExpired:
        raise AuthFailed(msg='token过期', error_code=1003)
    uid = data['uid']
    ac_type = data['type']
    scope = data['scope']
    # 判断用户是否用权限访问改api
    allow = is_in_scope(scope, request.endpoint)
    if not allow:
        raise Forbidden()
    # 用namedtuple 保存在g里的数据可用.的方式访问(方便)
    return User(uid, ac_type, scope)
