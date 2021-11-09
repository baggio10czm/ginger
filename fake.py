"""
 创建超级管理员的脚本
"""


from app import create_app
from app.models.base import db
from app.models.user import User

app = create_app()
with app.app_context():
    with db.auto_commit():
        # 创建一个超级管理员
        user = User()
        user.nickname = 'Super'
        user.password = '111222'
        user.email = '777@qq.com'
        user.auth = 2
        db.session.add(user)
