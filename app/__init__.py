import os
from flask import Flask, request
from flask.ext.assets import Environment, Bundle
from webassets.loaders import PythonLoader as PythonAssetsLoader
from flask.ext.cache import Cache
from flask.ext.babel import Babel
from flask_user import current_user, login_required, UserManager, UserMixin, SQLAlchemyAdapter, roles_required
from flask_user.forms import RegisterForm
from flask.ext.mail import Mail
from flask.ext.login import LoginManager
from flask.ext.migrate import Migrate
from database import db
from models import User, IceRegisterForm

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

    # Initialize Flask-Babel
    babel = Babel(app)                              
    
    # Initialize Flask-Mail
    mail = Mail(app)       

    # Initialize Flask-Migrate
    migrate = Migrate(app,db)
                         
    @babel.localeselector
    def get_locale():
        translations = [str(translation) for translation in babel.list_translations()]
        return request.accept_languages.best_match(translations)
    # Setup Flask-User
    db_adapter = SQLAlchemyAdapter(db,  User)       # Select database adapter
    user_manager = UserManager(db_adapter, 
                               app,
                               register_form = IceRegisterForm)     # Init Flask-User and bind to app
    # register blueprints
    from controllers.main import main
    from controllers.customer import customer
    from controllers.email import email
    from controllers.schedule import schedule
    app.register_blueprint(main)
    app.register_blueprint(customer)
    app.register_blueprint(email)
    app.register_blueprint(schedule)

    return app

if __name__ == '__main__':
    # Import the config for the proper environment using the
    # shell var APPNAME_ENV
    env = os.environ.get('APPNAME_ENV', 'prod')
    app = create_app('app.config.%sConfig' % env.capitalize(), env=env)
    # Create 'user007' user with 'secret' and 'agent' roles


    app.run(host='0.0.0.0')
