#! ../env/bin/python
# -*- coding: utf-8 -*-

from __future__ import print_function

from flask import current_app, url_for

from datetime import datetime,date

from . import User, Role

# **********************
# ** Global Variables **
# **********************
# Using global variable for speed
user1 = "Jeffries"

def check_valid_register_form(um, client, db):
    global user1

    User = um.db_adapter.UserClass

    # Define defaults
    kwargs = {
        username:'jeffries',
        email:username+'@example.com',
        password:'Password1',
        retype_password:'Password1'
    }
    print("test_valid_register_form")

    client.post_valid_form(url_for("user.register"),**kwargs)

    user1username = User.query.filter(User.username==username)
    user1email = User.query.filter(User.email==email)
    assert user1username
    assert user1email
    assert not user1username.active
