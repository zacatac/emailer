from app.database import db
from app.models import Customer, User, Role
from flask import url_for, current_app
from app import create_app
from testutils import TstClient
