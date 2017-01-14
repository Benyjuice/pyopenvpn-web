# python flask config class
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class ConfigBase:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '!((!(!!FXX'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    MAIL_SUBJECT_PREFIX = '[Huayue]'
    MAIL_SUBJECT_PREFIX = 'Huayue Admin <admin@huayuebox.com>'
    ADMIN = os.environ.get('ADMIN')
    OPENVPN_LOGFILE = "/etc/openvpn/openvpn-status.log"
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(ConfigBase):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
            'mysql://root:199184@localhost/openvpn-dev'
    

class TestingConfig(ConfigBase):
    TESING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data-test.sqlite')


class ProductionConfig(ConfigBase):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'data.sqlite')


config = {
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    
    'default':DevelopmentConfig
}
