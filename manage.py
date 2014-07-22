#!/usr/bin/env python
import os,sys
from getopt import getopt
from flask.ext.script import Manager, Server
from flask.ext.migrate import MigrateCommand
from app import create_app
from app.models import Customer, Users, Role
from app.database import db


env = os.environ.get('APPNAME_ENV', 'development')
app = create_app('app.config.%sConfig' % env.capitalize(), env=env)
user_manager = app.user_manager

manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command("server", Server())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, User=Users)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your Alchemy models
    """
    # print(app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()
    manager_role = Role(name='management')
    employee_role = Role(name='employee')
    db.session.add(manager_role)
    db.session.add(employee_role)
    db.session.commit()
    if not Users.query.filter(Users.username=='user007').first():

        user1 = Users(username='user007', email='user007@example.com', active=True,
                     password=user_manager.hash_password('Password1'))
        user1.roles.append(employee_role)
        # user1.set_role()
        db.session.add(user1)
        db.session.commit()

        user2 = Users(username='test', email='testuser@icesportsforum.com', active=True,
                     password=user_manager.hash_password('Password1'))
        # user2.set_role()
        user2.roles.append(manager_role)
        db.session.add(user2)
        db.session.commit()

        user3 = Users(username='test3', email='testuser3@icesportsforum.com', active=True,
                     password=user_manager.hash_password('Password1'))
        # user3.set_role()
        user3.roles.append(manager_role)
        db.session.add(user3)
        db.session.commit()



if __name__ == "__main__":
    manager.run()

@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():
        
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)
            
        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:25s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)
        
    for line in sorted(output):
        print line
        links = []
