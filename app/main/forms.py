from flask_wtf import FlaskForm as Form
from wtforms import StringField, TextAreaField, BooleanField, SelectField,\
    SubmitField,RadioField , SelectMultipleField, FileField
from wtforms.validators import Required, Length, Email, Regexp, NoneOf, DataRequired
from wtforms import ValidationError
from .pagedown import PageDownField
from ..models import *



class NameForm(Form):
    name = StringField('汝是谁?', validators=[Required()])
    submit = SubmitField('OK')

class RegistrationForm(Form):
    name=StringField('汝是谁?', validators=[Required(),Length(0, 64)])
    email=StringField('电子邮件地址', validators=[Required(),Length(0, 64), Email()])
    classnum=StringField('学号', validators=[Required(),Length(8)])
    gender=SelectField('性别',validators=[Required()])
    phone=StringField('电话号码', validators=[Required(),Length(11,11)])
    qq = StringField('QQ', validators=[Length(0, 64)])
    wechat = StringField('微信', validators=[Length(0, 64)])
    telegram=StringField('Telegram (用户名，不含"@")', validators=[Length(0, 64)])
    personal_page=StringField('Blog', validators=[Length(0, 64)])
    ablity=TextAreaField('汝都擅长些啥咧？')
    desc=TextAreaField('介绍下汝自己呗~')
    photo=FileField('不留张照片？')
    submit = SubmitField('就这样?')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.gender.choices = [(1,"男"),(2,"女")]

class EditProfileForm(Form):
    name = StringField('真实姓名', validators=[Length(0, 64)])
    about_me = TextAreaField('介绍下汝自己呗~')
    tag = SelectMultipleField('标签', coerce=int)
    qq = StringField('QQ', validators=[Length(0, 64)])
    wechat = StringField('微信', validators=[Length(0, 64)])
    telegram=StringField('Telegram (用户名，不含"@")', validators=[Length(0, 64)])
    blog=StringField('Blog', validators=[Length(0, 64)])
    weibo=StringField('新浪微博 (个性域名地址，不含"http://weibo.com/")', validators=[Length(0, 64)])
    twitter=StringField('Twitter (用户名，不含"@")', validators=[Length(0, 64)])
    googleplus=StringField('Google+ (个人资料链接)', validators=[Length(0, 64)])
    github=StringField('Github 用户名', validators=[Length(0, 64)])
    zhihu=StringField('知乎 (个性域名 URL，不含"https://zhihu.com/people")', validators=[Length(0, 64)])
    submit = SubmitField('就这样?')

    def __init__(self,*args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.tag.choices = [(tag.id, tag.name)
                             for tag in Tag.query.order_by(Tag.id).all()]



class EditProfileAdminForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    username = StringField('用户名', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          ' (╯・∧・)╯ ┻━┻ 用户名只能包含字母，数字和下划线。 ')])
    confirmed = BooleanField('已确认')
    role = SelectField('角色', coerce=int)
    name = StringField('真实姓名', validators=[Length(0, 64)])
    location = RadioField('主要小组', coerce=int)
    about_me = TextAreaField('介绍')
    submit = SubmitField('提交')

    def __init__(self, user, *args, **kwargs):
        super(EditProfileAdminForm, self).__init__(*args, **kwargs)
        self.role.choices = [(role.id, role.name)
                             for role in Role.query.order_by(Role.name).all()]
        self.location.choices = [(group.id, group.name)
                             for group in Group.query.order_by(Group.name).all()]
        self.user = user

    def validate_email(self, field):
        if field.data != self.user.email and \
                User.query.filter_by(email=field.data).first():
            raise ValidationError('(ノ｀Д´)ノ┻━┻ 这个邮箱注册过啦~')

    def validate_username(self, field):
        if field.data != self.user.username and \
                User.query.filter_by(username=field.data).first():
            raise ValidationError('(ノ｀Д´)ノ┻━┻ 这个用户名注册过啦~')


class PostForm(Form):
    body = PageDownField("", validators=[Required()])
    submit = SubmitField('咱写好了')


class CommentForm(Form):
    body = StringField('汝不说些啥?', validators=[Required()])
    submit = SubmitField('好啦好啦,我说就是了~')

class InterviewForm(Form):
    status = RadioField('面试状态', coerce=int,validators=[Required()])
    level = SelectField('评价等级', coerce=int,validators=[Required()])
    opinion = TextAreaField('评价描述')
    submit = SubmitField('提交')

    def __init__(self, *args, **kwargs):
        super(InterviewForm, self).__init__(*args, **kwargs)
        self.status.choices=[(status.id, status.text)
                             for status in Interview_status.query.order_by(Interview_status.id).all()]
        self.level.choices=[(i,"☆"* i) for i in range(6)]
