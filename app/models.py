# -*- coding: utf-8 -*-
"""
    Database Models
    ~~~~~~
"""
from flask import current_app

from database import db
from datetime import datetime,date
from flask.ext.user import UserMixin, login_required
from flask.ext.user.forms import RegisterForm
from wtforms import validators, ValidationError

def icesportsforum_email(form, field):
    email = field.data.strip().lower()
    if "@" not in email or email.split("@")[1] != "icesportsforum.com":
            raise ValidationError('Must have an Ice Sports Forum email to register')
    

class IceRegisterForm(RegisterForm):
    def validate(self):       
        if icesportsforum_email not in self.email.validators:
            email = self.email.validators.append(icesportsforum_email)
        return super(IceRegisterForm, self).validate()
        

# Define the User-Roles pivot table
user_roles = db.Table('user_roles',
                      db.Column('id', db.Integer(), primary_key=True),
                      db.Column('user_id', db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE')),
                      db.Column('role_id', db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE')))

# Define User model.
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean(), nullable=False, default=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, default='')
    email = db.Column(db.String(255), nullable=False, unique=True)
    confirmed_at = db.Column(db.DateTime())
    reset_password_token = db.Column(db.String(100), nullable=False, default='')
    # Relationships
    roles = db.relationship('Role', secondary=user_roles,
                            backref=db.backref('users', lazy='dynamic'))
    
# Define Role model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    birth = db.Column(db.DateTime)
    sex = db.Column(db.Integer)
    email = db.Column(db.String)
    phone = db.Column(db.Integer)
    entered = db.Column(db.DateTime, nullable=False)

    def __init__(self, first_name, last_name, birth, sex,
                 email, phone, entered=None):
        self.first_name = first_name
        self.last_name = last_name
        self.birth = birth
        self.email = email
        self.phone = phone
        self.sex = sex
        if entered is None:
            entered = datetime.now()
        self.entered = entered

    def __repr__(self):
        return '<User: {0}>'.format(self.first_name + self.last_name)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    visit_time = db.Column(db.DateTime, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))

class Laser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    codename = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
class LearnToSkate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    skill = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    

    

