#!.venv/bin/python
from flask_script import Manager, Shell, Command, Option
from app import create_app, db, Api
from app.models import UserModel, LogModel, RoleModel
import os
from flask_migrate import Migrate, MigrateCommand


app = create_app(os.getenv('CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db, directory="migrations")

def make_shell_contex():
    return dict(db=db,app=app,User=UserModel,Log=LogModel, Api=Api, role=RoleModel)


class Varify(Command):
    def __init__(self, default_name=None):
        self.default_name = default_name
        self.default_password = None

    def get_options(self):
        return [
            Option('-n', '--name', dest='name', default=self.default_name),
            Option('-p', '--password', dest='password', default=self.default_password)
        ]

    def run(self, name, password):
        user = UserModel.query.filter_by(username=name).first()
        if not user:
            return 1
        if user.verify_password(password):
            return 0
        else:
            return 1

class Connect(Command):
    def get_options(self):
        return [
            Option('-n', '--name', dest='name', default=""),
            Option('-i', '--ip', dest='ip', default=""),
            Option('-p', '--port', dest='port', default="")
        ]
    def run(self, name, ip, port):
        api = Api(name)
        api.connect(ip,port)


class Disonnect(Command):
    def get_options(self):
        return [
            Option('-n', '--name', dest='name', default=""),
            Option('-r', '--received', dest='received', default=0),
            Option('-s', '--sent', dest='sent', default=0)
        ]
    def run(self, name, received, sent):
        api = Api(name)
        api.disconnect(received, sent)


manager.add_command('shell', Shell(make_context=make_shell_contex))
manager.add_command('db',MigrateCommand)
manager.add_command('varify',Varify)
manager.add_command('connect', Connect)
manager.add_command('disconnect', Disonnect)

if __name__=='__main__':
    manager.run()
