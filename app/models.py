from flask_login import UserMixin, AnonymousUserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from . import login_manager
from datetime import datetime


class UserModel(UserMixin, db.Model):
    __tablename__='user'
    __table_args__ = {'sqlite_autoincrement': True}

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(128), unique=True, index=True)
    email = db.Column(db.String(128),unique=True, index=True)
    password_hash = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=False)
    enable = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    logs = db.relationship('LogModel', backref='user')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permission):
        # 判断用户是否具备某权限
        return self.role is not None and (self.role.permissions & permission) == permission

    def is_administrator(self):
        # 判断用户是否具备管理员权限
        return self.can(Permission.LINK | Permission.OTHER)


class LogModel(db.Model):
    __tablename__='log'
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.BigInteger, primary_key=True)
    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    trusted_ip = db.Column(db.String(64))
    trusted_port = db.Column(db.String(10))
    bytes_received = db.Column(db.BigInteger)
    bytes_sent = db.Column(db.BigInteger)
    finished = db.Column(db.Boolean, default=False)


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def loaf_user(user_id):
    return UserModel.query.get(int(user_id))


class Permission:
    '''
    Permission Table
    '''

    ## Link to server via openvpn
    LINK = 0x01

    ## Other permission
    OTHER = 0x80


class RoleModel(db.Model):
    '''
    User Roles Table
    '''
    __tablename__='role'
    id = db.Column(db.Integer, primary_key=True)
    # 该用户角色名称
    name = db.Column(db.String(164))
    # 该用户角色是否为默认
    default = db.Column(db.Boolean, default=False, index=True)
    # 该用户角色对应的权限
    permissions = db.Column(db.Integer)
    # 该用户角色和用户的关系
    # 角色为该用户角色的所有用户
    users = db.relationship('UserModel', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        """
        创建用户角色
        """
        roles = {
            # 定义了两个用户角色(User, Admin)
            'User': (Permission.LINK, True),
            'Admin': (Permission.LINK |
                      Permission.OTHER, False)
        }
        for r in roles:
            role = RoleModel.query.filter_by(name=r).first()
            if role is None:
                # 如果用户角色没有创建: 创建用户角色
                role = RoleModel(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
            db.session.commit()