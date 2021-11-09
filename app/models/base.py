"""
 User: Czm
 Date: 2021/11/1
 Time: 13:36
"""
from contextlib import contextmanager
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy, BaseQuery
from sqlalchemy import SmallInteger, Column, Integer

from app.libs.error_code import NotFound


class SQLAlchemy(_SQLAlchemy):
    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            # 最好在所有db.session.commit()的地方+ try……except
            self.session.rollback()
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
            ['']时可以获取对于的属性值
            具体原理在 v1/user.py 中有说明
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
        for key in keys:
            self.fields.remove(key)
        return self

    def append(self, *keys):
        for key in keys:
            self.fields.append(key)
        return self