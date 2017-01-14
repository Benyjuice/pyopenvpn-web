from . import db
from .models import UserModel, LogModel
from datetime import datetime


class Api:
    def __init__(self, username=""):
        self.username = username

    def varify(self, password):
        user = UserModel.query.filter_by(username=self.username).first()
        if not user:
            return 1

        if user.verify_password(password) and user.enable and user.active:
            return 0
        else:
            return 1

    def connect(self, trusted_ip, trusted_port):
        user = UserModel.query.filter_by(username=self.username).first()
        if not user:
            print('Error:no sunch user:%s\n' % self.username)
            return 1
        log = LogModel(user=user,
                       trusted_ip=trusted_ip,
                       trusted_port=trusted_port)
        db.session.add(log)
        db.session.commit()

    def disconnect(self, bytes_received, bytes_sent):
        logs = LogModel.query.filter_by(username=self.username,finished=False).all()
        if not logs:
            return 1
        for log in logs:
            log.finished = True
            log.bytes_received = bytes_received
            log.bytes_sent = bytes_sent
            log.end_time = datetime.utcnow()
            db.session.add(log)
            db.session.commit()
