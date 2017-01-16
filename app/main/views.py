from flask import render_template, session, redirect, url_for, current_app
from flask_login import current_user, login_required
from . import main
from ..models import UserModel as User
from ..models import LogModel as Log


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/user/<id>')
@login_required
def user(id=None):
    if not id:
        user = current_user
    else:
        user = User.query.get_or_404(id)

    current = Log.query.filter_by(finished=False, user=user).first()
    logs = Log.query.filter_by(user=user,finished=True).all()
    return render_template('user.html',user=user,logs = logs, current=current)


@main.route('/user')
@login_required
def user_info():
    return user(current_user.id)


@main.route('/download')
@login_required
def download():
    return render_template('download.html')




