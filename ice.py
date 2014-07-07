# -*- coding: utf-8 -*-
"""
    ICE
    ~~~~~~

    A customer management application provided 
    to the Ice Sports Forum.

    :copyright: (c) 2014 by Zackery Field.
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
DATABASE = './db/ice.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
UPLOAD_FOLDER = './uploads/'
ALLOWED_EXTENSIONS = set(['csv'])

# create our little application
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

def db_contains(first_name,last_name,email,verbose=False):
    db = get_db()
    if email == "":
        already = db.execute('SELECT * FROM customers WHERE (first_name=:first_name AND last_name=:last_name)',
                             {"first_name":first_name, "last_name":last_name}).fetchone()
    else: 
        already = db.execute('SELECT * FROM customers WHERE (first_name=:first_name AND last_name=:last_name) OR email=:email',
                         {"first_name":first_name, "last_name":last_name,"email":email}).fetchone()
    
    if already is not None:
        if verbose:
            already_entered = 'Person already entered into the database'
            print(already_entered + \
                  '\nName:{0} {1}\
                  \nEntered:{2}'\
                  .format(already['first_name'],
                          already['last_name'],
                          already['entered']))
        return (True, already['id'])
    return (False,None)

    
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

def bulk_upload(addr,activity):
    f = open(addr, 'rb') # opens the csv file
    print('opened file',f)
    try:
        reader = csv.reader(f)  # creates the reader object    
        header = True
        count = 0
        unique = 0
        def raise_the_roof():
            raise IntegrityError('Skating and hockey tables not yet supported')        
        if activity not in ['0','1']: raise_the_roof()
        activity_dict = {'0':'laser','1':'learnToSkate'}
        activity = activity_dict[activity]
        for row in reader:   # iterates the rows of the file in order
            count += 1
            if header:
                header = False
            else:
                db = get_db()
                first_name = row[0].strip().title()
                last_name = row[1].strip().title()
                sex = row[2].strip().title()
                email = row[4].strip()   
                birth = row[3].strip()
                visit_time = row[5].strip()
                codename = row[6].strip()
                contains,id = db_contains(first_name, last_name, email)
                if not contains:
                    try:
                        db.execute('insert into customers (first_name, last_name, email, birth, sex, entered) values (?, ?, ?, ?, ?, ?)',[first_name, last_name, email, birth, sex ,str(datetime.now())])
                        db.commit()        
                        if activity == 'laser':
                            field = 'codename'
                            insert = codename
                        elif activity == 'learnToSkate':
                            field = 'skill'
                            insert = '1' #***ALERT***
                        else:
                            raise_the_roof()
                        id = db.execute('SELECT id FROM customers WHERE first_name=:first_name AND last_name=:last_name AND email=:email AND birth=:birth',{"first_name":first_name,"last_name":last_name,"email":email,"birth":birth}).fetchone()['id']
                        command = 'INSERT INTO {0} ({1},customer_id) values (?,?)'.format(activity,field)
                        db.execute(command,[insert,id])
                        command = 'INSERT INTO visit (visit_time,customer_id) values (?,?)'
                        db.execute(command,[visit_time,id])
                        db.commit()
                        unique += 1
                    except IntegrityError:                        
                        flash('Name fields, and email cannot be empty')
                else:
                    command = 'INSERT INTO visit (visit_time,customer_id) values (?,?)'
                    contains = True if db.execute('SELECT visit.visit_id FROM visit WHERE visit_time=:visit_time AND customer_id=:id',{"visit_time":visit_time,"id":id}).fetchone() is not None else False
                    if contains:
                        print(db.execute('SELECT * FROM visit,customers WHERE visit_time=:visit_time AND customer_id=:id AND (customers.id=visit.customer_id)',{"visit_time":visit_time,"id":id}).fetchone())
                    if not contains:
                        db.execute(command,[visit_time,id])
                        db.commit()
                        
                    
    finally:
        f.close()      # closing    
    flash('{0} uploaded!'.format(unique))
    return redirect(url_for('register'))

@app.route('/add_all', methods=['POST'])
def add_players():
    if not session.get('logged_in'):
        redirect(url_for('login'))    
    request.files['file'].save('users_upload.csv')
    bulk_upload('users_upload.csv',request.form['activity'])
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
            return redirect(url_for('navigate'))
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
    my_dict = {}
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
            my_dict[item] = (base_value,relation_value,criteria_value)        
    search_tables = {
        'laser':False,
        'learnToSkate':False,
        'visit':False
    }
    
    form_where_clause = lambda column, relation, criteria: {
        "0":"({0} LIKE \"%{1}%\")".format(column, criteria),
        "1":"({0} NOT LIKE \"%{1}%\")".format(column, criteria),
        "2":"({0} BETWEEN \"0\" AND \"{1}\")".format(column, criteria),
        "3":"({0} BETWEEN \"{1}\" AND \"9999\")".format(column, criteria),
        "4":"({0} LIKE \"{1}%\")".format(column, criteria),
        "5":"({0} LIKE \"%{1}\")".format(column, criteria),
        "6":"({0} IS \"{1}\")".format(column, criteria),
        "7":"({0} IS NOT \"{1}\")".format(column, criteria),
        "8":"(strftime('%m', {0}) IS \"{1}\")".format(column,"{0}".format(criteria).zfill(2)) 
    }[relation]
    
    selectors = ["email","first_name","last_name","birth","codename","entered","visit_time","activity"]    
    create_basic_search_command = \
                                  lambda table, where_clause: \
                                  "SELECT * FROM {0} WHERE {1}".format(table,where_clause)
    create_join_search_command = \
                                 lambda table1, table2, table1id, table2id, where_clause: \
                                 "SELECT * FROM {0}, {1} WHERE ({0}.{2} = {1}.{3}) AND ({4})".format(table1,table2,table1id,table2id,where_clause)

    def create_command(search_tables,queries):
        select = "SELECT * FROM customers, "
        where = " WHERE "
        selectors = ["email","first_name","last_name","birth","codename","entered","visit_time","activity"]    
        laser = 'laser'
        visit = 'visit'
        learnToSkate = 'learnToSkate'
        customers = "customers"
        for query,values in queries.iteritems():
            selector = selectors[int(values[0])]
            relation = values[1]
            criteria = values[2]
            if selector == "codename":
                if not search_tables[laser]:
                    search_tables[laser] = True
                    select += laser + ", " 
                    where += "(customers.id={0}.customer_id) AND ".format(laser)                                              
                where += form_where_clause("{0}.{1}".format(laser,selector),relation,criteria) + " AND "
            elif selector == "visit_time":
                if not search_tables[visit]:
                    search_tables[visit] = True
                    select += visit + ", "                
                    where += "(customers.id={0}.customer_id) AND ".format(visit)                       
                where += form_where_clause("{0}.{1}".format(visit,selector),relation,criteria)  + " AND "
            elif selector == "activity":
                if criteria == "0": #Laserstrike
                    if not search_tables[laser]:
                        search_tables[laser] = True
                        select += laser + ", "                
                        where += "(customers.id={0}.customer_id) AND ".format(laser)                               
                elif criteria == "1": #Learn to skate
                    if not search_tables[learnToSkate]:
                        search_tables[learnToSkate] = True
                        select += learnToSkate + ", "
                        where += "(customers.id={0}.customer_id) AND ".format(learnToSkate)                               
            else:

                where += form_where_clause("{0}.{1}".format(customers,selectors[int(selector)]),relation,criteria) + " AND "
        command = select[:-2] +  where[:-4]        
        return command
    command = create_command(search_tables,my_dict)
    print("CALLING CREATE")
    print(command)
    print("END CREATE")
    db = get_db()
    entries = db.execute(command).fetchall()
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
