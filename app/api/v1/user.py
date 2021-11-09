"""
 User: Czm
 Date: 2021/11/5
 Time: 17:35
 Describe:
"""
from flask import jsonify, g

from app import db
from app.libs.error_code import DeleteSuccess, AuthFailed
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User

api = Redprint('user')


class Test:
    name = 'Czm'
    age = 36

    def __init__(self):
        self.name = 'Czm,YYY,CMX,CJQ'
        self.age = 33

    def keys(self):
        """ dict(实例对象)时会调用此方法 """
        return 'name', 'age'

    def __getitem__(self, item):
        """
            dict(实例对象)时会用['']访问对象里变量.
            当实例对象被['']调用时会执行此方法
        """
        return getattr(self, item)


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    scope = g.user.scope
    if not scope:
        raise AuthFailed()
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user)


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    """
        不能让用户传id进来删除防止"超权"(一个用户可以获取其他用户信息)
        故此要使用在创建token时保存的g变量获取当前用户id来操作
        ……query.get_or_404(uid) 不能解决重复软删除的问题
        在基类模型base中 重写的filter_by方法包括了 status=1
        的条件,所以使用这个就可以解决 重复软删除的问题
    """
    # user = User.query.get_or_404(uid)
    uid = g.user.uid
    user = User.query.filter_by(id=uid).first_or_404()

    # 返回数据常规做法
    # r = {
    #     'nickname': user.nickname,
    #     'email': user.email
    # }
    # return jsonify(r)

    # 在app.py:
    # 类变量无法用__dict__获取,需要在构造函数里赋值(实例变量)
    # dict()可拿到类变量和实例变量
    # 所以 要想拿到user模型中想要的字段 只需要重写keys 和 __getitem__方法就好
    # return jsonify(Test())
    return jsonify(user)


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    """
        不能让用户传id进来删除防止"超权"(一个用户可以把其他人都删了)
        故此要使用在创建token时保存的g变量获取当前用户id来操作
    """
    uid = g.user.uid
    with db.auto_commit():
        """
            ……query.get_or_404(uid) 不能解决重复软删除的问题
            在基类模型base中 重写的filter_by方法包括了 status=1
            的条件,所以使用这个就可以解决 重复软删除的问题
        """
        # user = User.query.get_or_404(uid)
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route('/<int:uid>', methods=['DELETE'])
@auth.login_required
def super_delete_user(uid):
    """
        超级管理员 可删除所有用户
    """
    scope = g.user.scope
    if not scope:
        raise AuthFailed()
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()
