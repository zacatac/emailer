#!/usr/bin/env python
import os

from flask.ext.script import Manager, Server
from app import create_app
from app.models import Customer
from app.database import db

env = os.environ.get('APPNAME_ENV', 'development')
app = create_app('app.config.%sConfig' % env.capitalize(), env=env)

manager = Manager(app)
manager.add_command("server", Server())


@manager.shell
def make_shell_context():
    """ Creates a python REPL with several default imports
        in the context of the app
    """

    return dict(app=app, User=User)


@manager.command
def createdb():
    """ Creates a database with all of the tables defined in
        your Alchemy models
    """
    print(app.config['SQLALCHEMY_DATABASE_URI'])
    db.create_all()

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
