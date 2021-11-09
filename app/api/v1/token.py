"""
 User: Czm
 Date: 2021/11/8
 Time: 12:22
 Describe:
"""
from flask import current_app, jsonify

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import AuthFailed
from app.libs.redprint import Redprint
from app.models.user import User
from app.libs.token_auth import auth
from app.validators.forms import ClientForm, TokenForm
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

api = Redprint('token')


@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    identity = promise[ClientTypeEnum(form.type.data)](
        form.account.data,
        form.secret.data
    )
    # 验证通过,生成令牌
    expiration = current_app.config['TOKEN_EXPIRATION']
    token = generate_auth_token(identity['uid'],
                                form.type.data,
                                identity['scope'],
                                expiration)
    data = {
        'token': token.decode('ascii')
    }
    return jsonify(data), 201


@api.route('/secret', methods=['POST'])
@auth.login_required
def get_token_info():
    """ 获取令牌信息,验证token是否有效 """
    form = TokenForm().validate_for_api()
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(form.token.data, return_header=True)
    except SignatureExpired:
        raise AuthFailed(msg='token 已过期', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token 无效', error_code=1002)

    r = {
        'scope': data[0]['scope'],
        'create_at': data[1]['iat'],  # token 创建时间
        'expire_in': data[1]['exp'],  # token 有效期
        'uid': data[0]['uid']
    }
    return jsonify(r)


def generate_auth_token(uid, ac_type, scope=None, expiration=7200):
    """
        生成令牌
        uid 用户id    ac_type用户登录类型
        scope 作用域  expiration 过期时间(秒)
    """
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
    # token中保存用户id和登录类型
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'scope': scope
    })
