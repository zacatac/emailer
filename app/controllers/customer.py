import os
from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, jsonify, Blueprint
from util import bulk_upload, upload, create_command
from . import db
from app import cache
from datetime import datetime
from flask.ext.user import current_user, login_required

customer = Blueprint('customer', __name__)

@customer.route('/customer/options')
def options():
    if current_user.is_authenticated():
        cur = db.engine.execute('select first_name, last_name, email, entered from customer order by id desc')
        players = cur.fetchall()
        players = [player for player in players if player[2] != '']
        return render_template('show_options.html' , entries=players)
    return redirect(url_for('user.login'))

@customer.route('/customer/register', methods=['GET'])
@login_required
def register():    
    return render_template('register.html')

@customer.route('/customer/find', methods=['GET','POST'])
@login_required
def find():
    if request.method == 'POST':
        search_dict = {
            'base0':('1','0',request.form['first_name'].strip().title()),
            'base1':('2','0',request.form['last_name'].strip().title()), 
            'base2':('0','0',request.form['email'].strip().lower()),
            'base3':('3','6',request.form['bday'])
        }
        search_dict = {key: value for key, value in search_dict.items() 
                       if value[2] != ''}
        if search_dict: 
            command = create_command(search_dict)                    
            entries = db.engine.execute(command).fetchall()
        else:
            entries = []
        return render_template('find.html', entries=entries)
    else:
        return render_template('find.html')


@customer.route('/customer/add', methods=['POST'])
@login_required
def add_player():
    # if not session.get('logged_in'):
    #     redirect(url_for('main.login'))
    first_name = request.form['first_name'].strip().title()
    last_name = request.form['last_name'].strip().title()
    sex = {
        '0':'F',
        '1':'M',
        '2':'N'}[request.form['sex']]
    birth = request.form['bday']
    email = request.form['email'].strip().lower()
    entered = str(datetime.now())
    activity = {
        '0':'laser',
        '1':'learnToSkate'
    }[request.form['activity']]
    visit_time = "0000-00-00" #***ALERT***
    field = "1" #***ALERT***
    customer = [
        first_name,
        last_name,
        sex,
        birth,
        email,
        entered,
        visit_time,
        field
    ]
    if upload(customer,activity):
        flash('New entry was successfully posted')
    else:
        flash('IntegrityError')
    return redirect(url_for('customer.register'))

@customer.route('/add_all', methods=['POST'])
@login_required
def add_players():
    path = os.path.join('app','uploads','users_upload.csv')
    request.files['file'].save(path)
    unique = bulk_upload(path,request.form['activity'])
    flash('{0} uploaded!'.format(unique))
    return redirect(url_for('customer.register'))
