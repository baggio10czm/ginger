"""
 User: Czm
 Date: 2021/11/6
 Time: 16:31
 Describe:重写HTTPException的一些方法
"""
from flask import request, json
from werkzeug.exceptions import HTTPException


class APIException(HTTPException):
    code = 500
    msg = 'sorry, we make a mistake T_T'
    error_code = 999

    def __init__(self, msg=None, code=None, error_code=None,
                 headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)

    def get_body(self, environ=None, scope=None):
        """
            重写get_body方法
        """
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None, scope=None):
        """
            重写get_headers方法
            返回json格式的数据
        """
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        """
            得到没有参数的完整url
        """
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
