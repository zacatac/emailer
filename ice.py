# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask and sqlite3.

    :copyright: (c) 2010 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import os
import csv,sys
from sqlite3 import dbapi2 as sqlite3, IntegrityError
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack
from flask_bootstrap import Bootstrap
from datetime import datetime
from werkzeug import secure_filename
from parse_csv import CSV_to_dict as dictize


# configuration
DATABASE = './db/emailer.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['csv'])

# create our little application :)
app = Flask(__name__)
Bootstrap(app)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def init_db():
    """Creates the database tables."""
    with app.app_context():
        db = get_db()
        with app.open_resource('./db/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db

    return top.sqlite_db

def db_contains(first_name,last_name,email):
    db = get_db()
    already = db.execute('SELECT * FROM customers WHERE (first_name=:first_name AND last_name=:last_name) OR email=:email',
                         {"first_name":first_name, "last_name":last_name,"email":email}).fetchone()
    
    if already is not None:
        already_entered = 'Person already entered into the database'
        print(already_entered + \
        '\nName:{0} {1}\
        \nEntered:{2}'\
        .format(already['first_name'],
                already['last_name'],
                already['entered']))
        return True
    return False

    
@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()
@app.route('/')
def navigate():
    return render_template('navigate.html')


@app.route('/customers')
def customers():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    db = get_db()
    cur = db.execute('select first_name, last_name, email, entered from customers order by id desc')
    players = cur.fetchall()
    players = [player for player in players if player[2] != '']
    return render_template('show_options.html' , entries=players)

@app.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        criteria = {}
        criteria['first_name'] = request.form['first_name'].strip().title()
        criteria['last_name'] = request.form['last_name'].strip().title()        
        criteria['email'] = request.form['email'].strip().lower()

        int_not_None = lambda x: int(x) if x != '' else None
        try:
            int_not_None(request.form['year'])
            int_not_None(request.form['month'])
            int_not_None(request.form['day'])
        except ValueError:
            flash('Year, month, and day fields must\
            be numeric.')
            redirect(url_for('customers'))
            
        criteria['year'] = int_not_None(request.form['year'])
        criteria['month'] = int_not_None(request.form['month'])
        criteria['day'] = int_not_None(request.form['day'])
        
        db = get_db()
        entries = db.execute('SELECT * FROM customers WHERE (first_name=:first_name AND last_name=:last_name) OR (email=:email)',\
                    criteria).fetchall()

        return render_template('search.html', entries=entries)
    else:
        return render_template('search.html')



@app.route('/add', methods=['POST'])
def add_player():
    if not session.get('logged_in'):
        redirect(url_for('login'))
    db = get_db()
    first_name = request.form['first_name'].strip().title()
    last_name = request.form['last_name'].strip().title()
    email = request.form['email'].strip()
    if not db_contains(first_name,last_name,email):
        try:
            db.execute('insert into customers (first_name, last_name, email, entered) values (?, ?, ?, ?)',
                       [first_name, last_name, email, str(datetime.now())])
            db.commit()
            flash('New entry was successfully posted')
        except IntegrityError:
            flash('IntegrityError')
    return redirect(url_for('register'))

def bulk_upload(addr):
    f = open(addr, 'rb') # opens the csv file
    print('opened file',f)
    try:
        reader = csv.reader(f)  # creates the reader object    
        header = True
        count = 0
        unique = 0
        for row in reader:   # iterates the rows of the file in order
            count += 1
            if header:
                header = False
            else:
                db = get_db()
                first_name = row[0].strip().title()
                last_name = row[1].strip().title()
                email = row[4].strip()   
                birth = row[3].strip()
                already = db.execute('SELECT * FROM customers WHERE first_name=:first_name AND last_name = :last_name',
                                         {"first_name":first_name, "last_name":last_name}).fetchone()
                if not db_contains(first_name, last_name, email):
                    try:
                        db.execute('insert into customers (first_name, last_name, email, birth, entered) values (?, ?, ?, ?, ?)',
                                   [first_name, last_name, email, birth,str(datetime.now())])
                        db.commit()
                        unique += 1
                        # flash('New entry was successfully posted')
                    except IntegrityError:                        
                        flash('Name fields, and email cannot be empty')
    finally:
        f.close()      # closing    
    flash('{0} uploaded!'.format(unique))
    return redirect(url_for('register'))

@app.route('/add_all', methods=['POST'])
def add_players():
    if not session.get('logged_in'):
        redirect(url_for('login'))    
    request.files['file'].save('users_upload.csv')
    bulk_upload('users_upload.csv')
    return redirect(url_for('register'))

@app.route('/register', methods=['GET'])
def register():    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('customers'))
    return render_template('login.html', error=error)

@app.route('/calendar')
def calendar():
    return render_template('calendar.html',calendar=None)

@app.route('/make-calendar',methods=['POST'])
def make_calendar():
    calendar = "<p> MY CALENDAAAA </p>"
    return render_template('calendar.html',calendar=calendar)
    

@app.route('/email/create',methods=['GET','POST'])
def create_list():
    selectors = ["email","first_name","last_name","birth","codename","entered","recent","activity"]
    relation_map = lambda relation,criteria: {
        "0":"LIKE \"%{0}%\"".format(criteria),
        "1":"NOT LIKE \"%{0}%\"".format(criteria),
        "2":"BETWEEN \"{0}\"".format(criteria),
        "3":"BETWEEN \"{0}\"".format(criteria),
        "4":"LIKE \"{0}%\"".format(criteria),
        "5":"LIKE \"%{0}\"".format(criteria),
        "6":"IS \"{0}\"".format(criteria),
        "7":"IS NOT \"{0}\"".format(criteria)
    }[relation]
    create_search_command = \
                            lambda table, selector, mapped_relation: \
                            "SELECT * FROM {0} WHERE {1} {2}".format(table,selector,mapped_relation)
    selector = selectors[int(request.form['base'])]
    relation = request.form['relation']
    criteria = request.form['criteria']        
    mapped_relation = relation_map(relation,criteria)
    command = create_search_command("CUSTOMERS",selector,mapped_relation)
    db = get_db()
    print(command)
    
    entries = db.execute(command).fetchall()
    print("****ENTRIES****")
    for entry in entries:
        print(entries)
    return render_template('email.html',entries=entries)

@app.route('/email', methods=['GET','POST'])
def email():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template("email.html")
             

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('navigate'))



if __name__ == '__main__':
    try:
        init_db()
    except sqlite3.OperationalError:
        pass
    # app.run(host='0.0.0.0') #Run the server on the network
    app.run()
