"""
 User: Czm
 Date: 2021/11/6
 Time: 14:47
 Describe:
"""
from sqlalchemy import Column, Integer, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.libs.error_code import NotFound, AuthFailed
from app.models.base import Base, db


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24), unique=True)
    # 普通用户=1 管理员=2
    auth = Column(SmallInteger, default=1)
    # 原来教程上是100长度是不够的,加密的密码超过会100会被截取,导致验证密码不正确
    _password = Column('password', String(120))

    # def keys(self):
    #     """
    #         定义模型可访问的属性
    #         具体原理在 v1/user.py 中有说明
    #     """
    #     return ['id', 'email', 'nickname', 'auth']

    @orm.reconstructor
    def __init__(self):
        """
            最终形态: 配合base基类中的 keys、hide、append
            @orm.reconstructor
            这个装饰,可以让模型每次被调用是执行构造函数(默认是不执行的)
        """
        super().__init__()
        self.fields = ['id', 'email', 'nickname', 'auth']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)

    @staticmethod
    def verify(email, password):
        # 虽然用first_or_404可以不用谢 if not use……两行代码
        # 但只能报一个统一的资源无法找到，个人感觉还是不太安全（不管是用户名无效还是密码错误都统一提示）
        # user = User.query.filter_by(email=email).first_or_404()
        user = User.query.filter_by(email=email).first()
        if not user:
            raise NotFound(msg='账户或密码错误!')
        if not user.check_password(password):
            raise AuthFailed(msg='账户或密码错误!')
        # scope名需要跟libs中的scope文件中的权限名相同
        scope = 'AdminScope' if user.auth == 2 else 'UserScope'
        return {'uid': user.id, 'scope': scope}

    def check_password(self, raw):
        if not self._password:
            return False
        return check_password_hash(self._password, raw)
