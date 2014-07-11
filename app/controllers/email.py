from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, jsonify, Blueprint
from util import create_command
from app import cache
from . import db

email = Blueprint('email', __name__)

@email.route('/email/create',methods=['GET','POST'])
def multi_search():
    search_dict = {}
    print(request.form)
    for item in request.form: 
        if item[:-1] == "base":
            base_value = request.form[item]
            relation_value = request.form['relation{0}'.format(item[-1])]
            if base_value == "7":
                criteria_value = request.form['activity{0}'.format(item[-1])]
            elif relation_value == "8":
                criteria_value = request.form['month{0}'.format(item[-1])]
            else:
                criteria_value = request.form['criteria{0}'.format(item[-1])]
            search_dict[item] = (base_value,relation_value,criteria_value)        
    command = create_command(search_dict)
    print(command)
    entries = db.engine.execute(command).fetchall()
    return render_template('email.html',entries=entries)

@email.route('/email', methods=['GET','POST'])
def index():
    if not session.get('logged_in'):
        return redirect(url_for('main.login'))
    return render_template("email.html")
