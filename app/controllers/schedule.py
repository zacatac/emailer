import os
from . import db
from datetime import datetime
from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, jsonify, Blueprint
from ..flask_user import login_required, roles_required, current_user
from app import cache
from . import db
from ..models import User, Schedule


# import gflags
# import httplib2

# from apiclient.discovery import build
# from oauth2client.file import Storage
# from oauth2client.client import OAuth2WebServerFlow
# from oauth2client.tools import run

# FLAGS = gflags.FLAGS
schedule = Blueprint('schedule', __name__)

@schedule.route('/schedule/manage', methods=['GET','POST'])
# @roles_required('management')
def hours():
    if request.method == "POST":
        hours = {}
        for item in request.form:
            hours[item] = request.form[item]
        print(hours)
        user = User.query.filter_by(id=current_user.id).first()
        print(user.username, user.email)
        if user is None:
            raise ValueError("NOOOOOOOO")
        available = []
        for i in range(7):
            data = (hours['start%s' % i], hours['end%s' % i])
            available.append(data)        
        print(available)
        sch = Schedule.query.filter_by(user_id=user.id).first()
        if sch is None:
            
            sch = Schedule(user_id=user.id,available=available)
            db.session.add(sch)
        else:
            print('not handled properly')
            sch.available=available
        db.session.commit()
        
        flash('Hours Uploaded!')
        sch = Schedule.query.filter_by(user_id=user.id).first()
        print(sch.available)
        return render_template('hours.html')                
    return render_template('hours.html')

@schedule.route('/schedule/register', methods=['GET','POST'])
@roles_required('management')
def register_employee():
    return render_template('employee_login_or_register.html')

# # Set up a Flow object to be used if we need to authenticate. This
# # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
# # the information it needs to authenticate. Note that it is called
# # the Web Server Flow, but it can also handle the flow for native
# # applications
# # The client_id and client_secret can be found in Google Developers Console
# FLOW = OAuth2WebServerFlow(
#     client_id='YOUR_CLIENT_ID',
#     client_secret='YOUR_CLIENT_SECRET',
#     scope='https://www.googleapis.com/auth/calendar',
#     user_agent='YOUR_APPLICATION_NAME/YOUR_APPLICATION_VERSION')

# # To disable the local server feature, uncomment the following line:
# # FLAGS.auth_local_webserver = False

# # If the Credentials don't exist or are invalid, run through the native client
# # flow. The Storage object will ensure that if successful the good
# # Credentials will get written back to a file.
# storage = Storage('calendar.dat')
# credentials = storage.get()
# if credentials is None or credentials.invalid == True:
#   credentials = run(FLOW, storage)

# # Create an httplib2.Http object to handle our HTTP requests and authorize it
# # with our good Credentials.
# http = httplib2.Http()
# http = credentials.authorize(http)

# # Build a service object for interacting with the API. Visit
# # the Google Developers Console
# # to get a developerKey for your own application.
# service = build(serviceName='calendar', version='v3', http=http,
#        developerKey='YOUR_DEVELOPER_KEY')
