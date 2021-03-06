"""
 User: Czm
 Date: 2021/11/6
 Time: 14:09
 Describe:
"""
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseForm as Form


class ClientForm(Form):
    """
        通用的用户验证
        wtforms 抛出的异常不会终止代码往下执行
        在validators/base中重写了wtforms一些方法
        使wtforms可抛出异常
    """
    account = StringField(validators=[DataRequired(message="账户必须填写!"), length(
        min=5, max=32
    )])
    secret = StringField()
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            # 判断是否是枚举内的值,对传入值的判断和限制
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        # 返回枚举类型,方便使用
        self.type.data = client


class UserEmailForm(ClientForm):
    """
        使用邮箱用户验证
    """
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        DataRequired(),
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,22}$')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       length(min=2, max=22)])

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError()


class BookSearchForm(Form):
    q = StringField(validators=[DataRequired()])


class TokenForm(Form):
    token = StringField(validators=[DataRequired()])
