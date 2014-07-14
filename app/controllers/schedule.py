import os
from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, jsonify, Blueprint
from . import db
from datetime import datetime
from flask.ext.user import login_required


schedule = Blueprint('schedule', __name__)

@schedule.route('/schedule/#', methods=['GET'])
def hours():
    return render_template('hours.html')
