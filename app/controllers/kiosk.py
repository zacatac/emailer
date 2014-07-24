from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, jsonify, Blueprint, current_app, json
from ..flask_user import login_required, roles_required
from ..flask_user.forms import LoginForm
import requests
from app import cache
from . import db, Customer
import mechanize
from base64 import b64encode

kiosk = Blueprint('kiosk', __name__)

@kiosk.route('/kiosk',methods=['GET','POST'])
def main():
    
    user_manager = current_app.user_manager
    login_form = user_manager.login_form(request.form)
    register_form = user_manager.register_form(request.form)
    
    if request.method == 'POST':          
        swipe='%LTCC0000000000006506?;000000000000006506?'
        true_swipe = {'swipe':swipe}

        test_data = {
            'cardid':'0000000000006506',
            'FirstName':'TestFirst2',
            'LastName':'TestLast2',
            'phone':'',
            'phone2':'',
            'areacode':'813',
            'Sex':'F',
            'CodeName':'TESTTEST2',
            'GroupType':'',
            'email':'',
            'dob_y':'2001',
            'dob_m':'01',
            'dob_d':'02'
        }
        test_waiver = {
            'cardid':swipe.split('?')[1][1:], 
            'codename':'TestCode',
            'custid':swipe.split('?')[1][1:],
        }

        test_photo = {
            'cardid':swipe.split('?')[1][1:], 
            'data':''
        }
        # birth = request.form['birth'].split('/')
        # entry_data = {
        #     'cardid':swipe.split('?')[2][1:],
        #     'FirstName':request.form['first_name'].strip().title(),
        #     'LastName':request.form['last_name'].strip().title(),
        #     'phone':'',
        #     'phone2':'',
        #     'areacode':'813',
        #     'Sex':request.form['sex'].strip().upper(),
        #     'CodeName':request.form['codename'].strip().upper(),
        #     'GroupType':'',
        #     'email':request.form['email'].strip().lower(),
        #     'dob_y':birth[2],
        #     'dob_m':birth[0],
        #     'dob_d':birth[1]
        # }

        headers={
            'Accept':'*/*',
            'Origin':'http://kiosk.centermanagerpro.com',
            'X-Requested-With':'XMLHttpRequest',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer':'http://kiosk.centermanagerpro.com/230/',
            'Accept-Encoding':'gzip,deflate,sdch',
            'Accept-Language':'en-US,en;q=0.8',
            'Connection':'Keep-Alive',
        }
        # auth = session.get('http://cloudKiosks:MioEnergyBlackCherry@kiosk.centermanagerpro.com/230')
        # if auth.status_code == 200:
 
        session = requests.Session()
        if 'swipe' not in request.form:
            if 'birth' in request.form:
                pass # register person
            else:
                customer = Customer.query.filter(email=email).first()
                if customer is not None:
                    flash('Logged in')
                else:
                    flash('Email not found')
                
        elif request.form['swipe'][:5] == "%LTCC":
            swipe = request.form['swipe']
            swipe_data = { 'swipe':swipe }
            cardid = swipe.split('?')[0][5:]            
            validate_swipe = session.post('http://cloudKiosks:MioEnergyBlackCherry@kiosk.centermanagerpro.com/230/ajax/validateswipe.php', data=swipe_data, headers=headers)
            json_data = json.loads(validate_swipe.text)
            if validate_swipe.status_code == 200 and json_data['reg']:
                print('passing')
                return render_template('kiosk.html', swipe=True)
            else:
                flash('Card Not Registered')
                return render_template('kiosk.html', swipe=False)
        elif request.form['swipe'][0] != "%":
            flash('Card Read Error')
            return render_template('kiosk.html', swipe=False)
        else:
            flash('not yet')
            return render_template('kiosk.html', swipe=True)
        
        # savedata = session.post('http://cloudKiosks:MioEnergyBlackCherry@kiosk.centermanagerpro.com/230/ajax/savedata.php', data=test_data, headers=headers)
        
        # print(savedata.text)

        # savewaiver = session.post('http://cloudKiosks:MioEnergyBlackCherry@kiosk.centermanagerpro.com/230/ajax/savewaiver.php', data=test_waiver, headers=headers)
        
        # print(savewaiver.text)

            # uploadphoto = session.post('http://cloudKiosks:MioEnergyBlackCherry@kiosk.centermanagerpro.com/230/ajax/uploadphoto.php', data=test_photo, headers=headers)
            
            # print(uploadphoto.text)
    return render_template('kiosk.html', swipe=False)

