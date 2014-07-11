#! ../env/bin/python
# -*- coding: utf-8 -*-
from coverage import coverage
import re
import mechanize

from app import create_app
from database import db

class TestURLs():
    def setup(self):
        app = create_app('app.config.DevelopmentConfig', env='dev')
        self.app = app.test_client()
        db.app = app
        db.create_all()

    def teardown(self):
        db.session.remove()
        db.drop_all()


    def test_navigate(self):
        rv = self.app.get('/')
        assert_equal(rv.status, '200 OK')
        assert 'Manage Customers' in rv.data
        assert 'Create a calendar' in rv.data
        assert 'Send emails' in rv.data

    def test_login(self):
        rv = self.app.get('/login')