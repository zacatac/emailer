import os

from flask import Flask
from flask.ext.assets import Environment
from webassets.loaders import PythonLoader as PythonAssetsLoader
from flask.ext.cache import Cache

# from app import assets
from database import db

# Setup flask cache
cache = Cache()

# init flask assets
assets_env = Environment()


def create_app(object_name, env="development"):
    """
    An flask application factory, as explained here:
    http://flask.pocoo.org/docs/patterns/appfactories/

    Arguments:
        object_name: the python path of the config object,
                     e.g. appname.settings.ProdConfig

        env: The name of the current environment, e.g. prod or dev
    """

    app = Flask(__name__)

    app.config.from_object(object_name)
    app.config['ENV'] = env

    #init the cache
    cache.init_app(app)

    #init SQLAlchemy
    db.init_app(app)

    # import and register the different asset bundles
    # assets_env.init_app(app)
    # assets_loader = PythonAssetsLoader(assets)
    # for name, bundle in assets_loader.load_bundles().iteritems():
    #     assets_env.register(name, bundle)

    # register our blueprints
    from controllers.main import main
    from controllers.customer import customer
    from controllers.email import email
    app.register_blueprint(main)
    app.register_blueprint(customer)
    app.register_blueprint(email)
    return app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var APPNAME_ENV
    env = os.environ.get('APPNAME_ENV', 'prod')
    app = create_app('app.config.%sConfig' % env.capitalize(), env=env)
    app.run()



# from flask import Flask       
# from flask_bootstrap import Bootstrap
# from models import *
# from database import db
# from app.config import DevelopmentConfig, ProductionConfig


# def create_app(config):
#     app = Flask(__name__)
#     Bootstrap(app)
#     app.config.update()
#     app.config.from_object(config)
#     app.config.from_envvar('FLASKR_SETTINGS', silent=True)   
#     return app
    
# app = create_app(DevelopmentConfig)
# db.init_app(app)
# with app.test_request_context():
#     db.create_all()  
      
# from app import views
