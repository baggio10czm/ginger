"""
 User: Czm
 Date: 2021/11/5
 Time: 21:34
 Describe:
"""


class Redprint:
    def __init__(self, name):
        self.name = name
        self.mound = []

    def route(self, rule, **options):
        """
            装饰器route
            保存传入的值,留在下面注册中使用
        """
        def decorator(f):
            self.mound.append((f, rule, options))
            return f
        return decorator

    def register(self, bp, url_prefix=None):
        """
            红图注册在蓝图时,就不一定需要填写url_prefix了
            默认用"/" + name的值
        """
        if url_prefix is None:
            url_prefix = "/" + self.name
        for f, rule, options in self.mound:
            # 如果endpoint有值就取值,如果没有就用默认值 f.__name__(视图函数)
            # 为了更好地权限控制 + 模块名 self.name
            endpoint = self.name + '+' + options.pop("endpoint", f.__name__)
            bp.add_url_rule(f'{url_prefix}/{rule}', endpoint, f, **options)
