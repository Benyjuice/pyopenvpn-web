from flask_login import UserMixin, AnonymousUserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager

class UserModel(UserMixin, db.Model):
    __tablename__='user'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True)
    email = db.Column(db.String(128),unique=True, index=True)
    password_hash = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=False)
    enable = db.Column(db.Boolean, default=True)
    logs = db.relationship('LogModel', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class LogModel(db.Model):
    __tablename__='log'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    trusted_ip = db.Column(db.String(64))
    trusted_port = db.Column(db.String(10))
    bytes_received = db.Column(db.BigInteger)
    bytes_sent = db.Column(db.BigInteger)
    finished = db.Column(db.Boolean)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def loaf_user(user_id):
    return UserModel.query.get(int(user_id))