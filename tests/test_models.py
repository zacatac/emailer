#! ../env/bin/python
# -*- coding: utf-8 -*-
from app import create_app
from app.database import db
from app.models import Customer
from datetime import datetime,date

class TestModels:
    def setup(self):
        app = create_app('app.config.DevelopmentConfig', env='dev')
        self.app = app.test_client()
        db.app = app
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_customer(self):
        customer = Customer(
            first_name='first', 
            last_name='last', 
            birth=date(2013, 3, 25),
            sex= 0,            
            email="asdf@asdf.com", 
            phone= "0"            
        )
        db.session.add(customer)
        db.session.commit()
