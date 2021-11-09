"""
 User: Czm
 Date: 2021/11/6
 Time: 14:05
 Describe:
"""
# from flask import request

from app.libs.enums import ClientTypeEnum
from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.models.user import User
from app.validators.forms import ClientForm, UserEmailForm

api = Redprint('client')


@api.route('/register', methods=['POST'])
def create_client():
    # data=data 是json格式的数据传入的方式
    # data=request.json 在BaseForm内部传入了
    # form = ClientForm(data=data)
    # ClientForm 返回self 就可以链式调用
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[form.type.data]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data,
                           form.account.data,
                           form.secret.data)
