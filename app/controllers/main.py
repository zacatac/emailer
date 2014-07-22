from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, jsonify, Blueprint, render_template_string
import util
from app import cache
from ..flask_user import current_user, login_required, roles_required
from flask.ext.login import LoginManager

# from app.forms import MyForm

main = Blueprint('main', __name__)

@main.route('/')
@cache.cached(timeout=1000)
def navigate():
    return render_template('navigate.html')

@main.route('/calendar')
def calendar():
    return render_template('calendar.html',calendar=None)    
