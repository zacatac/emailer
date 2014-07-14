import os
from flask.ext.user.forms import RegisterForm
ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    ALLOWED_EXTENSIONS = set(['csv'])
    UPLOAD_FOLDER = './uploads/'
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_PASSWORD_SALT = "salty"
    CSRF_ENABLED = True

    # Configure Flask-Mail -- Required for Confirm email and Forgot password features
    MAIL_SERVER   = 'smtp.gmail.com'
    MAIL_PORT     = 465
    MAIL_USE_SSL  = True                            # Some servers use MAIL_USE_TLS=True instead
    MAIL_USERNAME = 'field.zackery@gmail.com'
    MAIL_PASSWORD = 'ntomrwkqrutznfwy'
    MAIL_DEFAULT_SENDER = '"Sender" <field.zackery@gmail.com>'

    # Configure Flask-User
    USER_ENABLE_USERNAME         = True
    USER_ENABLE_CONFIRM_EMAIL    = True
    USER_ENABLE_CHANGE_USERNAME  = True
    USER_ENABLE_CHANGE_PASSWORD  = True
    USER_ENABLE_FORGOT_PASSWORD  = True
    USER_ENABLE_RETYPE_PASSWORD  = True
    USER_LOGIN_TEMPLATE = 'flask_user/login_or_register.html'
    USER_REGISTER_TEMPLATE = 'flask_user/login_or_register.html'

class DevelopmentConfig(Config):
    SECRET_KEY = 'development key'
    DATABASE = 'dev.db'
    DATABASE_DIRECTORY = 'db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(ABSOLUTE_PATH,DATABASE_DIRECTORY,DATABASE)    
    DEBUG = True
    CACHE_TYPE = 'null'
    WTF_CSRF_ENABLED = False

class TestingConfig(Config):
    SECRET_KEY = 'testing key'
    DATABASE = '/db/test.db'
    DATABASE_DIRECTORY = 'db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(ABSOLUTE_PATH,DATABASE_DIRECTORY,DATABASE)    
    TESTING = True

class ProductionConfig(Config):
    SECRET_KEY = 'testing key'
    CACHE_TYPE = 'simple'
    DATABASE = '/db/ice.db'
    DATABASE_DIRECTORY = 'db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(ABSOLUTE_PATH,DATABASE_DIRECTORY,DATABASE) 
