"""
 User: Czm
 Date: 2021/11/5
 Time: 17:18
 Describe:
"""
from app.app import Flask
from app.models.base import db


# def register_blueprints(app):
#     from app.api.v1 import create_blueprint_v1
#     app.register_blueprint(create_blueprint_v1())

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.setting')
    app.config.from_object('app.config.secure')

    # 注册蓝图
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')

    # 注册db
    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app
