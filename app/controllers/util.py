import csv,sys,imp,subprocess
from datetime import datetime
from werkzeug import secure_filename
from sqlalchemy import or_, and_
from sqlalchemy.exc import IntegrityError
from . import dictize, db, Customer, Visit, Laser

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def db_contains(first_name,last_name,email,birth,verbose=False):
    name_condition = [Customer.first_name==first_name,
                      Customer.last_name==last_name]
    name_and_birth = name_condition + [Customer.birth==birth]
    name_and_email = name_condition + [Customer.email==email]
    name_and_birth_and = and_(*name_and_birth)
    name_and_email_and = and_(*name_and_email)
    
    if email == "":
        already = Customer.query.filter(name_and_email_and)

    else: 
        already = Customer.query.filter(or_(*[name_and_birth_and, name_and_email_and]))
        
    already = already.first()
    if already is not None:
        return (True, already.id)
    return (False,None)

def upload(customer,activity):
    first_name = customer[0].strip().title()
    last_name = customer[1].strip().title()
    sex = {'M':0,'F':1,'':2,'N':3}[customer[2].strip().title()]
    email = customer[4].strip().lower()   
    if email == "": email = None
    birth = customer[3].strip()
    visit_time = customer[5].strip()
    if birth in ["0000-00-00", ""]:
        birth = None;
    contains,id = db_contains(first_name, last_name, email,birth)
    if not contains:
        customer_row= Customer(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            birth=birth,
                            sex=sex,
                            entered=str(datetime.now()))
        try:
            db.session.add(customer_row)
            db.session.commit()
        except:
            db.session.rollback()
            print("exception",customer_row.first_name,customer_row.last_name,customer_row.email)
            email = None
            customer_row=Customer(first_name=first_name,
                            last_name=last_name,
                            email=email,
                            birth=birth,
                            sex=sex,
                            entered=str(datetime.now()))

            db.session.add(customer_row)
            db.session.commit()
        finally:
            id = Customer.query.filter_by(first_name=first_name,
                                 last_name=last_name,
                                 email=email,
                                 birth=birth,
                                 sex=sex).first().id
            if activity == 'laser':
                codename = customer[6].strip().upper()
                player_aux = Laser(codename=codename,customer_id=id)
            elif activity == 'learnToSkate':
                field = 'skill'
                insert = '1' #***ALERT*** 
                player_aux = Laser(skill=1,customer_id=id)
            visit = Visit(visit_time=visit_time, customer_id=id)
            db.session.add(player_aux)            
            db.session.add(visit)
            db.session.commit()
            return True

            
    else:     
        query = Visit.query.filter(Visit.visit_time==visit_time, Visit.customer_id==id)
        if query.first() is not None:
            visit = Visit(visit_time=visit_time, customer_id=id)
            db.session.add(visit)
            db.session.commit()
    return False
                        
def bulk_upload(addr,activity):
    f = open(addr, 'rb') # opens the csv file
    try:
        reader = csv.reader(f)  # creates the reader object        
        header = True
        rows = 0
        unique = 0
        activity_dict = {'0':'laser','1':'learnToSkate'}
        activity = activity_dict[activity]       
        for row in reader:   # iterates the rows of the file in order
            rows += 1
            if header:
                header = False
            else:
                if upload(row,activity): unique += 1
    finally:
        f.close()      # closing    
    return unique

def create_command(queries):

    form_where_clause = lambda column, relation, criteria: {
        "0":"({0} LIKE \'%%{1}%%\')".format(column, criteria),
        "1":"({0} NOT LIKE \'%%{1}%%\')".format(column, criteria),
        "2":"({0} BETWEEN \'0\' AND \'{1}\')".format(column, criteria),
        "3":"({0} BETWEEN \'{1}\' AND \'9999\')".format(column, criteria),
        "4":"({0} LIKE \'{1}%%\')".format(column, criteria),
        "5":"({0} LIKE \'%%{1}\')".format(column, criteria),
        "6":"({0} = \'{1}\')".format(column, criteria),
        "7":"({0} IS NOT \'{1}\')".format(column, criteria),
        "8":"(date_part('month', {0}) = \'{1}\')".format(column,"{0}".format(criteria).zfill(2)) 
    }[relation]

    search_tables = {
        'laser':False,
        'learnToSkate':False,
        'visit':False
    }    

    select = "SELECT * FROM customer, "
    where = " WHERE "
    selectors = ["email","first_name","last_name","birth","codename","entered","visit_time","activity"]    
    laser = 'laser'
    visit = 'visit'
    learnToSkate = 'learnToSkate'
    customers = "customer"
    for query,values in queries.iteritems():
        selector = selectors[int(values[0])]
        relation = values[1]
        criteria = values[2]
        if selector == "codename":
            if not search_tables[laser]:
                search_tables[laser] = True
                select += laser + ", " 
                where += "(customer.id={0}.customer_id) AND ".format(laser)                                              
            where += form_where_clause("{0}.{1}".format(laser,selector),relation,criteria) + " AND "
        elif selector == "visit_time":
            if not search_tables[visit]:
                search_tables[visit] = True
                select += visit + ", "                
                where += "(customer.id={0}.customer_id) AND ".format(visit)                       
            where += form_where_clause("{0}.{1}".format(visit,selector),relation,criteria)  + " AND "
        elif selector == "activity":
            if criteria == "0": #Laserstrike
                if not search_tables[laser]:
                    search_tables[laser] = True
                    select += laser + ", "                
                where += "(customer.id={0}.customer_id) AND ".format(laser)                               
            elif criteria == "1": #Learn to skate
                if not search_tables[learnToSkate]:
                    search_tables[learnToSkate] = True
                    select += learnToSkate + ", "
                where += "(customer.id={0}.customer_id) AND ".format(learnToSkate)                               
        else:            
            where += form_where_clause("{0}.{1}".format(customers,selector),relation,criteria) + " AND "
    command = select[:-2] +  where[:-4]        
    return command
