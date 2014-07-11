import csv,sys,imp,subprocess
from datetime import datetime
from werkzeug import secure_filename
from . import dictize, db

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def raise_the_roof():
    raise IntegrityError('Skating and hockey tables not yet supported')   

def db_contains(first_name,last_name,email,birth,verbose=False):
    if email == "":
        already = db.engine.execute('SELECT * FROM customer WHERE (first_name=:first_name AND last_name=:last_name AND birth=:birth)',
                             {"first_name":first_name, "last_name":last_name, "birth":birth}).fetchone()
    else: 
        already = db.engine.execute('SELECT * FROM customer WHERE (first_name=:first_name AND last_name=:last_name AND birth=:birth) OR (email=:email AND first_name=:first_name AND last_name=:last_name)',
                             {"first_name":first_name, "last_name":last_name,"email":email,"birth":birth}).fetchone()
    
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

def upload(customer,activity):
    first_name = customer[0].strip().title()
    last_name = customer[1].strip().title()
    sex = customer[2].strip().title()
    email = customer[4].strip().lower()   
    birth = customer[3].strip()
    visit_time = customer[5].strip()
    contains,id = db_contains(first_name, last_name, email,birth)
    if not contains:
        try:
            db.engine.execute('insert into customer (first_name, last_name, email, birth, sex, entered) values (?, ?, ?, ?, ?, ?)',[first_name, last_name, email, birth, sex ,str(datetime.now())])
            # db.commit()              
            if activity == 'laser':
                codename = customer[6].strip().upper()
                field = 'codename'
                insert = codename
            elif activity == 'learnToSkate':
                field = 'skill'
                insert = '1' #***ALERT***
            else:
                raise_the_roof()
            id = db.engine.execute('SELECT id FROM customer WHERE first_name=:first_name AND last_name=:last_name AND email=:email AND birth=:birth',{"first_name":first_name,"last_name":last_name,"email":email,"birth":birth}).fetchone()['id']
            command = 'INSERT INTO {0} ({1},customer_id) values (?,?)'.format(activity,field)
            db.engine.execute(command,[insert,id])
            command = 'INSERT INTO visit (visit_time,customer_id) values (?,?)'
            db.engine.execute(command,[visit_time,id])
            # db.commit()
            return True
        except IntegrityError:                        
                flash('Name fields, and email cannot be empty')
    else:                    
        command = 'INSERT INTO visit (visit_time,customer_id) values (?,?)'
        contains = True if db.engine.execute('SELECT visit.id FROM visit WHERE visit_time=:visit_time AND customer_id=:id',{"visit_time":visit_time,"id":id}).fetchone() is not None else False
        if not contains: # replace with contains after test
            db.engine.execute(command,[visit_time,id])
            # db.commit()
    return False
                        
def bulk_upload(addr,activity):
    f = open(addr, 'rb') # opens the csv file
    try:
        reader = csv.reader(f)  # creates the reader object        
        header = True
        rows = 0
        unique = 0
        if activity not in ['0','1']: raise_the_roof()
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
    print(queries)
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
