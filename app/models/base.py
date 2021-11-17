"""
 User: Czm
 Date: 2021/11/1
 Time: 13:36
"""
from contextlib import contextmanager
from datetime import datetime

from flask import current_app
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import SmallInteger, Column, Integer

from app.libs.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self, throw=None):
        try:
            yield
            self.session.commit()
        except Exception as e:
            db.session.rollback()
            # %r 用来做 debug 比较好，因为它会显示变量的原始数据
            current_app.logger.exception('%r' % e)
            if throw:
                raise e


class Query(BaseQuery):
    """
    重写基类的方法,避免每个filter_by都需要传 status=1
    但这样的写法确实不太懂...
    """
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)

    def get_or_404(self, ident, description=None):
        """ 重写 get 404 方法返回自定义的错误 """
        rv = self.get(ident)
        if rv is None:
            raise NotFound()
        return rv

    def first_or_404(self, description=None):
        """ 重写 first 404 方法返回自定义的错误 """
        rv = self.first()
        if rv is None:
            raise NotFound()
        return rv


# query_class 重写覆盖
db = SQLAlchemy(query_class=Query)


class Base(db.Model):
    # 模型基类 不需要生成数据表 __abstract__
    __abstract__ = True
    create_time = Column('create_time', Integer)
    # 支持软删除
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    def __getitem__(self, item):
        """
            使对象可支持['']访问
            具体原理在 v1/user.py 中有说明
            getattr 拿到对象属性名对应的值
        """
        return getattr(self, item)

    def set_attrs(self, attrs_dict):
        for key, value in attrs_dict.items():
            # 判断对象是否包含某个属性
            if hasattr(self, key) and key != 'id':
                setattr(self, key, value)

    @property
    def create_datetime(self):
        if self.create_time:
            # 时间戳转换成时间对象,后续就可以用 strftime('%Y-%m-%d') 转成日期
            return datetime.fromtimestamp(self.create_time)
        else:
            return None

    # 软删除,使代码更加语义化
    def delete(self):
        self.status = 0

    def keys(self):
        """ 增加此方法可让下面的字段增、减有效 """
        return self.fields

    def hide(self, *keys):
        """ 隐藏字段可链式调用.append  """
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        """ 增加字段可链式调用.hide  """
        for key in keys:
            self.fields.append(key)
        return self
