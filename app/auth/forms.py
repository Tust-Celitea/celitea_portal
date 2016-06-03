from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(Form):
    email = StringField('电子邮件地址', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('密码', validators=[Required()])
    remember_me = BooleanField('在本次会话中保存登录状态')
    submit = SubmitField('登录')


class RegistrationForm(Form):
    email = StringField('电子邮件地址', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          ' (╯・∧・)╯ ┻━┻ 用户名只能包含字母，数字和下划线。 ')])
    password = PasswordField('密码', validators=[
        Required(), EqualTo('password2', message='(╯=﹁"﹁=)╯ ┻━┻ 两次输入的密码不一样')])
    password2 = PasswordField('重复密码', validators=[Required()])
    submit = SubmitField('注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('(ノ｀Д´)ノ┻━┻ 这个邮箱注册过啦~<br />或许汝需要试试 <a href="/auth/login">登录</a>?')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('(ノ｀Д´)ノ┻━┻ 这个用户名注册过啦~')


class ChangePasswordForm(Form):
    old_password = PasswordField('旧密码', validators=[Required()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='(╯=﹁"﹁=)╯ ┻━┻ 两次输入的密码不一样')])
    password2 = PasswordField('重复一遍新密码', validators=[Required()])
    submit = SubmitField('更改密码 | ω・`)')


class PasswordResetRequestForm(Form):
    email = StringField('邮件地址', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('发送密码重置邮件,Biu~')


class PasswordResetForm(Form):
    email = StringField('邮件地址', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('新密码', validators=[
        Required(), EqualTo('password2', message='(╯=﹁"﹁=)╯ ┻━┻ 两次输入的密码不一样')])
    password2 = PasswordField('重复一遍新密码', validators=[Required()])
    submit = SubmitField('更改密码 | ω・`)')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('咦?这个邮件地址咱好像不认识 😂 ')


class ChangeEmailForm(Form):
    email = StringField('新的邮件地址', validators=[Required(), Length(1, 64),
                                                 Email()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('更改邮件地址| ω・`)')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('(ノ｀Д´)ノ┻━┻ 这个邮箱注册过啦~')
