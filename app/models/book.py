"""
 User: Czm
 Date: 2021/11/8
 Time: 22:27
 Describe:
"""
from sqlalchemy import Column, String, Integer, orm

from app.models.base import Base

__author__ = '七月'


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))

    # def keys(self):
    #     return ['id', 'title', 'author', 'binding', 'publisher', 'price',
    #             'pages', 'pubdate', 'isbn', 'summary', 'image']
    #
    # def hide(self, field):
    #     pass

    @orm.reconstructor
    def __init__(self):
        """
            最终形态: 配合base基类中的 keys、hide、append
            @orm.reconstructor
            这个装饰,可以让模型每次被调用是执行构造函数(默认是不执行的)
        """
        super().__init__()
        self.fields = ['id', 'title', 'author', 'binding',
                       'publisher',
                       'price', 'pages', 'pubdate', 'isbn',
                       'summary',
                       'image']
