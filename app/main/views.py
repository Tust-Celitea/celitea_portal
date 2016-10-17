from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from flask_sqlalchemy import get_debug_queries
from . import main
from .forms import EditProfileForm, EditProfileAdminForm, PostForm,\
    CommentForm,RegisterForm,InterviewForm
from .. import db
from ..models import *
from ..email import send_email,send_async_email
from ..decorators import admin_required, permission_required,moderate_required
from .group import groups
from werkzeug.utils import secure_filename
import os
import sys
import time

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']


@main.after_app_request
def after_request(response):
    for query in get_debug_queries():
        if query.duration >= current_app.config['FLASKY_SLOW_DB_QUERY_TIME']:
            current_app.logger.warning(
                'Slow query: %s\nParameters: %s\nDuration: %fs\nContext: %s\n'
                % (query.statement, query.parameters, query.duration,
                   query.context))
    return response


@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():
    form = PostForm()
    if current_user.can(Permission.WRITE_ARTICLES) and \
            form.validate_on_submit():
        post = Post(body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        return redirect(url_for('.index'))
    page = request.args.get('page', 1, type=int)
    query = Post.query
    pagination = query.order_by(Post.timestamp.desc()).limit(3).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('index.html', form=form, posts=posts,
                            pagination=pagination)

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    register=Registration()
    interview=Interview()
    if form.validate_on_submit():
        register.email = form.email.data
        register.classnum =form.classnum.data
        register.name=form.name.data
        register.ablity=form.ablity.data
        register.desc=form.desc.data
        register.qq=form.qq.data
        register.phone=form.phone.data
        register.wechat=form.wechat.data
        register.telegram=form.telegram.data
        register.personal_page=form.personal_page.data
        file = request.files['photo']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(str(time.time()).replace(".",""))
            file.save(os.path.join(current_app.config['UPLOAD_DIR'], filename))
            register.photo = filename
            db.session.add(register)
            interview.id=register.id
            interview.status=1
            db.session.add(interview)
            send_email(register.email, '{}的报名确认~'.format(register.name),
                       'mail/registration', reg=register)
            flash('OK，坐下来放松一下呗~')
            return redirect(url_for('.index'))
        else:
            flash("这不是照片 (╯=3=)╯ ┻━┻")
    return render_template('register.html', form=form)

@main.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('user.html', user=user, posts=posts,
                           pagination=pagination,show_followed=True)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        current_user.qq = form.qq.data
        current_user.wechat = form.wechat.data
        current_user.telegram = form.telegram.data
        current_user.blog=form.blog.data
        current_user.weibo=form.weibo.data
        current_user.twitter=form.twitter.data
        current_user.googleplus=form.googleplus.data
        current_user.github=form.github.data
        current_user.zhihu=form.zhihu.data
        db.session.add(current_user)
        for tag in current_user.tags.all():
            db.session.delete(tag)
        for tag in form.tag.data:
            conn=Connection(user_id=current_user.id,user_tag_id=tag)
            db.session.add(conn)
        flash('已更新个人资料,biu~')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.about_me.data = current_user.about_me
    form.qq.data = current_user.qq
    form.wechat.data = current_user.wechat
    form.telegram.data = current_user.telegram
    form.blog.data=current_user.blog
    form.tag.data =[connect.user_tag_id for connect in list(current_user.tags.all())]
    form.weibo.data=current_user.weibo
    form.twitter.data=current_user.twitter
    form.googleplus.data=current_user.googleplus
    form.github.data=current_user.github
    form.zhihu.data=current_user.zhihu
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        db.session.add(user)
        flash('已更新个人资料,biu~')
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)

@main.route('/all')
@login_required
def show_all():
    resp = make_response(redirect(url_for('.index')))
    resp.set_cookie('show_followed', '', max_age=30*24*60*60)
    return resp

@main.route('/manage')
@login_required
@admin_required
def manage():
    return "Administartor zone!"

@main.route('/manage/tag/add/<name>', methods=['GET', 'POST'])
@login_required
@admin_required
def add_tag(name):
    tag=Tag.query.filter_by(name=name).first()
    if not tag:
        tag=Tag(name=name)
        db.session.add(tag)
        flash('已添加标签 "{}" 😋😋'.format(name))
    else:
        flash('"{}" 这个标签已经有啦~ 😋😋'.format(name))
    return redirect(url_for('.index'))

@main.route('/manage/tag/delete/<name>', methods=['GET', 'POST'])
@login_required
@admin_required
def del_tag(name):
    tag=Tag.query.filter_by(name=name).first()
    if tag:
        db.session.delete(tag)
        flash('已删除标签 "{}" 😋😋'.format(name))
    else:
        flash('没有 "{}" 这个标签啦~ 😋😋'.format(name))
    return redirect(url_for('.index'))

@main.route('/tags')
@login_required
def list_tag():
    tags=Tag.query.all()
    return render_template("tags.html",tags=tags)

@main.route('/manage/registrations')
@main.route('/manage/registrations/<status>')
@login_required
@admin_required
def registrations(status="all"):
    statuses={"all":0,"ready":1,"confirmed":2,"rejected":3,"talking":4}
    if not status in statuses:
        abort(404)
    if status=="all":
        reg=Registration.query.order_by("classnum").all()
    else:
        reg=[user for user in Registration.query.order_by("classnum").all() if user.interview.status==statuses[status]]
    return render_template("registrations.html",registrations=reg)

@main.route('/manage/registration/<int:id>',methods=['GET', 'POST'])
@login_required
@admin_required
def registration(id):
    reg_query=Registration.query.order_by("id")
    ids=[0]+[registration.id for registration in reg_query.all()]
    current_reg=reg_query.filter_by(id=id).first_or_404()
    current_interview=Interview.query.filter_by(id=id).first()
    try:
        priv_reg=reg_query.filter_by(id=ids[ids.index(id)-1]).first()
    except IndexError:
        priv_reg=False
    try:
        next_reg=reg_query.filter_by(id=ids[ids.index(id)+1]).first()
    except IndexError:
        next_reg=False
    form=InterviewForm()
    if form.validate_on_submit():
        current_interview.status=form.status.data
        current_interview.level=form.level.data
        current_interview.opinion=form.opinion.data
        db.session.add(current_interview)
        return redirect(url_for('.registrations'))
    form.status.data=current_interview.status
    form.level.data=current_interview.level
    form.opinion.data=current_interview.opinion
    return render_template("registration.html",reg=current_reg,priv_reg=priv_reg,next_reg=next_reg,form=form)

@main.route("/manage/registration/<int:id>/delete")
@login_required
@admin_required

def del_reg(id):
    reg_query=Registration.query.filter_by(id=id).first_or_404()
    db.session.delete(reg_query)
    flash("嗯，这个不好吃~")
    return redirect(url_for('.registrations'))

@main.route('/manage/registrations.csv')
@login_required
@admin_required
def registrations_csv():
    reg=Registration.query.order_by("id").all()
    title="姓名,电子邮件地址,专业和班级,电话号码,QQ,微信,Telegram,个人网站,特长与兴趣,自我介绍"
    str_reg_list=[title]
    for registration in reg:
        str_reg="{},{},{},{},{},{},{},{},{}".format(registration.name,
                                                    registration.email,
                                                    registration.classnum,
                                                    registration.phone,
                                                    registration.qq or "",
                                                    registration.wechat or "",
                                                    registration.telegram or "",
                                                    registration.personal_page or "",
                                                    registration.ablity or "",
                                                    registration.desc or "")
        str_reg_list.append(str_reg)
    response=make_response("\n".join(str_reg_list))
    response.headers["Content-type"] = "text/csv"
    return response
