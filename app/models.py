# -*- coding: utf-8 -*-
"""
    Database Models
    ~~~~~~
"""
from database import db
from datetime import datetime,date

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
    

    
