"""
 User: Czm
 Date: 2021/11/8
 Time: 11:10
 Describe:重写wtforms的一些方法,使它可抛出异常
"""
from flask import request
from wtforms import Form
from app.libs.error_code import ParameterException


class BaseForm(Form):
    def __init__(self):
        # 在内部调用,在外部就不用每次都传了
        # data = request.json
        # 用get_json 如果传过来的json是空的也不会报错
        data = request.get_json(silent=True)
        # 获取url?后面的参数
        args = request.args.to_dict()
        super(BaseForm, self).__init__(data=data, **args)

    def validate_for_api(self):
        # 调用父类的validate方法进行参数验证
        valid = super(BaseForm, self).validate()
        if not valid:
            # 返回 form.errors 的错误信息
            raise ParameterException(msg=self.errors)
        # 返回form 外部就可以链式调用(简化代码)
        return self
