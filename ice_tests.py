# -*- coding: utf-8 -*-
# """
#     ICE Tests
#     ~~~~~~~~~~~~

#     Tests the Ice application.

#     :copyright: (c) 2010 by Armin Ronacher.
#     :license: BSD, see LICENSE for more details.
# """
# from flask import url_for, json

# import unittest

# from flask.ext.testing import TestCase as Base, Twill

# import app.models as models
# import app.database as database

# base_url = 'http://127.0.0.1:5000'
# tests_dir = '/'
# person1 = {
#     'first_name': 'Mr.',
#     'last_name':'Rogers',
#     'sex':'0',
#     'bday':'2011-01-01',
#     'email':'mrogers@no.com',
#     'activity':'0',    
# }


# class ModelsTestCase(Base):

#     db_uri = "sqlite:////Users/zrfield/laserstrike/ice/app/db/test.db"
 
#     def create_app(self):
#         app = Flask(__name__)
#         app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
#         db.init_app(app)
#         return app
 
#     def setUp(self):
#         db.create_all()
#         # fixtures.install(self.app, *fixtures.all_data)

 
#     def tearDown(self):
#         db.session.remove()
#         db.drop_all()

#     def test_empty_db(self):
#         """Start with a blank database."""    
#         c = self.client        
#         rv = c.get('/')
#         assert_equal(rv.status, '200 OK')
#         assert 'Manage Customers' in rv.data


# # class TestCase(Base):   
    
# #     def create_app(self):
# #         app = create_app(TestingConfig)
# #         from app.views import *
# #         db.init_app(app)
# #         return app
        
# #     def setUp(self):
# #         """Before each test, set up a blank database"""
# #         client = app.test_client()
# #         db.create_all()
        

# #     def tearDown(self):
# #         """Get rid of the database again after each test."""    
# #         db.session.remove()
# #         db.drop_all()

# #     def login(self, username, password):
# #         return self.client.post('/login', data=dict(
# #             username=username,
# #             password=password
# #         ), follow_redirects=True)

# #     def logout(self):
# #         return self.app.get('/logout', follow_redirects=True)



# # class TestCustomer(TestCase):
#  # testing functions

#     # def test_login_logout(self):
#     #     """Make sure login and logout works"""
#     #     c = self.app.test_client()
#     #     rv = self.login(self.app.config['USERNAME'],
#     #                     self.app.config['PASSWORD'])
#     #     print(rv.data)
#     #     assert b'You were logged in' in rv.data
#     #     rv = self.logout()
#     #     assert b'You were logged out' in rv.data
#     #     rv = self.login(self.app.config['USERNAME'] + 'x',
#     #                     self.app.config['PASSWORD'])
#     #     assert b'Invalid username' in rv.data
#     #     rv = self.login(self.app.config['USERNAME'],
#     #                     self.app.config['PASSWORD'] + 'x')
#     #     assert b'Invalid password' in rv.data

#     # def test_add_single(self):
#     #     """Test that adding single customer works"""
#     #     c = self.app.test_client()
#     #     self.login(self.app.config['USERNAME'],
#     #                self.app.config['PASSWORD'])
#     #     rv = c.post('/add', data=person1, follow_redirects=True)
#     #     assert b'<div class=flash>New entry was successfully posted</div>' in rv.data 
#     #     # Extract search call from        
#     #     rv = c.post('/find', data=person1, follow_redirects=True)
#     #     assert 'mrogers@no.com' in rv.data

#     # def test_add_bulk(self):
#     #     """Test adding bulk from CSV"""
#     #     c = self.app.test_client()
#     #     self.login(self.app.config['USERNAME'],
#     #                self.app.config['PASSWORD'])
#     #     users_test = open(tests_dir+'users1.csv', 'r')
#     #     rv = c.post('/add_all',data={'file':users_test,'activity':'0'},follow_redirects=True)
#     #     users_test.close()
#     #     print(rv.data)
#     #     assert '4 uploaded!' in rv.data                
                
#     # def test_calendar(self):
#     #     """Testing calendar generator"""
#     #     c = self.app.test_client()
#     #     rv = c.get('/calendar')
#     #     assert "Create Calendar" in rv.data
                
#     # def test_email_search(self):
#     #     """Testing email search"""
                
#     # def test_email_list(self):
#     #     """Testing email list"""
        

#     # def test_email_alerts(self):
#     #     """Testing front-end email alerting"""
        
    

   
    
# def main():
#     # cov = coverage(branch = True, omit = ['flask/*', 'self_tests.py','/Library/*'])
#     # cov.start()
#     try:
#         unittest.main()
#     except:
#         pass
#     # cov.stop()
#     # cov.save()
#     # print "\n\nCoverage Report:\n"
#     # cov.report()
    
# if __name__ == '__main__':
#     main()
