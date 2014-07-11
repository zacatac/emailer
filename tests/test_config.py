#! ../env/bin/python
# -*- coding: utf-8 -*-
from app import create_app


class TestConfig:
    def test_dev_config(self):
        app = create_app('app.config.DevelopmentConfig', env='dev')

        assert app.config['DEBUG'] is True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:////Users/zrfield/laserstrike/ice/app/db/dev.db'
        assert app.config['SECRET_KEY'] == 'development key'

    def test_prod_config(self):
        app = create_app('app.config.ProductionConfig', env='prod')

        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:////Users/zrfield/laserstrike/ice/app/db/ice.db'
        assert app.config['CACHE_TYPE'] == 'simple'
