from flask import render_template, session, redirect, url_for
from flask_login import current_user, login_required
from . import main
from ..models import UserModel as User


@main.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@main.route('/user')
@login_required
def user_info(id=None):
    return render_template('user.html',user=current_user)


@main.route('/user/<id>')
def user(id=None):
    if not id:
        user = current_user
    else:
        user = User.query.get_or_404(id)

    return render_template('user.html',user=user,logs = user.logs)

