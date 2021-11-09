"""
 User: Czm
 Date: 2021/11/6
 Time: 16:19
 Describe:
"""
from app.libs.error import APIException


# 400 参数错误 401 未授权 403 禁止访问  404 找不到资源
# 500 服务器未知错误
# 200 请求成功 201 创建、更新成功 204 删除成功
# 301 302 重定向

class Success(APIException):
    code = 201
    msg = 'okay'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = -1


class ServerError(APIException):
    code = 500
    msg = 'sorry, we make a mistake T_T'
    error_code = 999


class ClientTypeError(APIException):
    """
        账户类型参数错误
    """
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(APIException):
    """
        通用参数错误
    """
    code = 400
    msg = 'client is invalid'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = 'the resource are not_found @_@...'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    msg = 'authorization failed'
    error_code = 1005


class Forbidden(APIException):
    code = 403
    msg = '你毫无权限访问'
    error_code = 1004


class DuplicateGift(APIException):
    code = 400
    msg = '你已经赠送过这个礼物了'
    error_code = 2001
