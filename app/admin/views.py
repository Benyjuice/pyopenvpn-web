from . import admin
from ..decorator import admin_required
from .utils import utils
from flask import render_template

@admin.route('/')
@admin_required
def index():
    tool = utils()
    users = tool.get_user()
    print(users)
    return render_template('admin/index.html', users=users)