#! ../env/bin/python
# -*- coding: utf-8 -*-
from . import url_for, current_app, db, create_app, TstClient

class TestForm():
    def setup(self):
        app = create_app('app.config.TestingConfig', env='dev')
        self.app = app
        db.app = app
        db.create_all()        
        self.client = TstClient(app.test_client(),db)
        

    def teardown(self):
        db.session.remove()
        db.drop_all()

    def test_register_form(self):
        """
        See Flask-User for basic tests
        Only tests inlucded here are specific
        to ice sports forum registration
        """
        username = "Jeffries"
        false_email = "asdf@testemaildomain.com"
        ice_email = "asdf@icesportsforum.com"
        password = "Password1"
        with self.app.app_context():
            self.client.post_invalid_form(url_for("user.register"),'Must have an Ice Sports Forum email to register',username=username, email=false_email, password=password, retype_password=password)

            self.client.post_valid_form(url_for("user.register"),username=username, email=ice_email, password=password, retype_password=password)

