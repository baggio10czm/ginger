"""
 User: Czm
 Date: 2021/11/5
 Time: 17:28
 Describe:涉及安全等重要的配置
"""

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:111222@localhost:3306/ginger'
SECRET_KEY = 'asgeq215xzvdyhDEWTDSHFGK548Czm346VBMGF4'
# ‘SQLALCHEMY_TRACK_MODIFICATIONS’ 这项配置在未来的版本中会被默认为禁止状态，
# 把它设置为True即可取消warning。
SQLALCHEMY_TRACK_MODIFICATIONS = False
