# manage.py

from flask.ext.script import Manager, Command

from ice import app
from flask import url_for

manager = Manager(app)

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

if __name__ == "__main__":
    manager.run()
