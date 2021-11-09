"""
 User: Czm
 Date: 2021/11/8
 Time: 18:58
 Describe:
"""


class Scope:
    """
        使用set自动去重
        api 接口视图函数
        module 模块名
        forbidden 排除的接口视图函数
    """
    allow_api = {}
    allow_module = {}
    forbidden = {}

    def __add__(self, other):
        self.allow_api = self.allow_api | other.allow_api
        self.allow_module = self.allow_module | other.allow_module
        self.forbidden = self.forbidden | other.forbidden

        # 返回自己可链式调用
        return self


class UserScope(Scope):
    allow_api = {'v1.user+get_user', 'v1.user+delete_user', 'v1.token+get_token_info'}


class AdminScope(Scope):
    allow_api = {'v1.user+super_get_user', 'v1.user+super_delete_user'}

    def __init__(self):
        self + UserScope()


class SuperAdminScope(Scope):
    allow_module = {'v1.user'}

    def __init__(self):
        self + AdminScope() + UserScope()


def is_in_scope(scope, endpoint):
    # globals() 函数会以字典类型返回当前位置的全部全局变量。
    # 比如用户的权限是'AdminScope' 就等于 AdminScope()
    scope = globals()[scope]()

    # endpoint 因为视图是挂载在蓝图上的,所以会带有 v1.xxx
    # 为了在 endpoint 中拿到模块名,
    # 需要在定义红图那里加上模块名self.name并用'+'分隔
    # 判断访用户是否有权限:
    # 先判断是否在排除名单
    # 在判断是否在对象的allow_api里
    # 最后判断是否在允许的模块中
    module = endpoint.split('+')[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if module in scope.allow_module:
        return True
    else:
        return False
