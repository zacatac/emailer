import os
ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    ALLOWED_EXTENSIONS = set(['csv'])
    UPLOAD_FOLDER = './uploads/'

class DevelopmentConfig(Config):
    SECRET_KEY = 'development key'
    DATABASE = '/db/dev.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + ABSOLUTE_PATH + DATABASE    
    DEBUG = True
    # SQLALCHEMY_ECHO = True
    CACHE_TYPE = 'null'
    # This allows us to test the forms from WTForm
    WTF_CSRF_ENABLED = False


class TestingConfig(Config):
    SECRET_KEY = 'testing key'
    DATABASE = '/db/test.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + ABSOLUTE_PATH + DATABASE    
    TESTING = True

class ProductionConfig(Config):
    SECRET_KEY = 'testing key'
    CACHE_TYPE = 'simple'
    DATABASE = '/db/ice.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:////' + ABSOLUTE_PATH + DATABASE    
    
