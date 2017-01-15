from . import admin
from .forms import AddUserForm
from ..decorator import admin_required
from .utils import utils
from flask import render_template
from ..models import UserModel
from app import db
from flask import flash, request

@admin.route('/')
@admin_required
def index():
    type = request.args.get('type')
    if not type:
        type = 'user_list'

    if type == 'user_list':
        users = UserModel.query.order_by(UserModel.id).all()
        return  render_template('admin/user_list.html', title='用户列表', users=users)
    # tool = utils()
    # users = tool.get_user()
    # print(users)
    # return render_template('admin/index.html', users=users)

@admin.route('/add_user', methods=['GET','POST'])
@admin_required
def add_user():
    form = AddUserForm()

    if form.validate_on_submit():
        if UserModel.query.filter_by(username=form.username.data).first():
            flash('User: %s already exist.' % form.username.data)
            return render_template('admin/add_user.html', form=form)

        user = UserModel(username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User: %s add successful, now can login via openvpn or web' % user.username)

    return render_template('admin/add_user.html', form=AddUserForm())