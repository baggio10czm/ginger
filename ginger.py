from app import create_app
from werkzeug.exceptions import HTTPException
from app.libs.error import APIException
from app.libs.error_code import ServerError

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    """
        全局异常处理:
        e 可能是 APIException,HTTPException
        或 Exception, 但都需要返回JSON格式的数据
    """
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return APIException(msg, code, error_code)
    else:
        # 调试模式可能需要返回详细信息就不抛出 ServerError 了
        if not app.config['DEBUG']:
            # 一般需要写入log日志
            return ServerError()
        else:
            raise e


if __name__ == '__main__':
    app.run(debug=True)

