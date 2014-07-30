from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, jsonify, Blueprint, current_app, json
from ..flask_user import login_required, roles_required
from ..flask_user.forms import LoginForm
import requests
from app import cache
from . import db, Customer, Laser
import mechanize
from base64 import b64encode

kiosk = Blueprint('kiosk', __name__)
cardid = False
codename = False 
swipe = False

@kiosk.route('/kiosk',methods=['GET','POST'])
def main():
    user_manager = current_app.user_manager
    login_form = user_manager.login_form(request.form)
    register_form = user_manager.register_form(request.form)
    
    if request.method == 'POST':  
        # swipe='%LTCC0000000000006580?;000000000000006580?'
        # true_swipe = {'swipe':swipe}

        # test_data = {
        #     'cardid':'0000000000006506',
        #     'FirstName':'TestFirst2',
        #     'LastName':'TestLast2',
        #     'phone':'',
        #     'phone2':'',
        #     'areacode':'813',
        #     'Sex':'F',
        #     'CodeName':'TESTTEST2',
        #     'GroupType':'',
        #     'email':'',
        #     'dob_y':'2001',
        #     'dob_m':'01',
        #     'dob_d':'02'
        # }
        # test_waiver = {
        #     'cardid':swipe.split('?')[1][1:], 
        #     'codename':'TestCode',
        #     'custid':swipe.split('?')[1][1:],
        # }

        # test_photo = {
        #     'cardid':swipe.split('?')[1][1:], 
        #     'data':''
        # }
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
        global swipe
        global cardid
        global codename
        session = requests.Session()
        if 'file' in request.form:
            photo = request.form['file']
            photo_data = {
                'cardid':cardid,
                'custid':cardid,
                'data':photo
            }
            print(photo[:100])
            swipe_data = { 'swipe':'%LTCC'+cardid+'?;00'+cardid+'?'}
            uploadphoto = session.post('http://cloudKiosks:MioEnergyBlackCherry@kiosk.centermanagerpro.com/230/ajax/uploadphoto.php', data=photo_data, headers=headers)
            
            print(uploadphoto.text)
            flash('Signed in successfully! You are ready to play!')
            return render_template('kiosk.html',laser=True)
        
        if 'swipe' not in request.form:
            if 'waiver' not in request.form:
                if 'birth' in request.form:
                    birth = request.form['birth'].split('/')
                    cardid = swipe.split('?')[0][5:]
                    codename = request.form['codename'].strip().upper()
                    entry_data = {
                        'cardid':cardid,
                        'FirstName':request.form['first_name'].strip().title(),
                        'LastName':request.form['last_name'].strip().title(),
                        'phone':'',
                        'phone2':'',
                        'areacode':'813',
                        'Sex':request.form['sex'].strip().upper(),
                        'CodeName':codename,
                        'GroupType':'',
                        'email':request.form['email'].strip().lower(),
                        'dob_y':birth[2],
                        'dob_m':birth[0],
                        'dob_d':birth[1]
                    }                
                    print(entry_data)
                else:
                    email = request.form['email']
                    print(email)
                    customer = Customer.query.filter(Customer.email==email).first()
                    if customer is not None:
                        flash('Logged in')
                        print(customer.email)
                        laser = Laser.query.filter(Laser.customer_id==customer.id).first()
                        if laser is None: 
                            codename = customer.first_name
                        else:
                            codename = laser.codename

                        birth = str(customer.birth).split('-')
                        print(customer.birth)
                        entry_data = {
                            'cardid':cardid,
                            'FirstName':customer.first_name,
                            'LastName':customer.last_name,
                            'phone':'',
                            'phone2':'',
                            'areacode':'813',
                            'Sex':{0:'F',1:'M',2:"F"}[customer.sex],
                            'CodeName':codename,
                            'GroupType':'',
                            'email':customer.email,
                            'dob_y':birth[2],
                            'dob_m':birth[0],
                            'dob_d':birth[1]
                        }                

                    else:
                        flash('Email not found')
                        return render_template('kiosk.html', swipe=True, laser=True)
                
                savedata = session.post('http://cloudKiosks:MioEnergyBlackCherry@kiosk.centermanagerpro.com/230/ajax/savedata.php', data=entry_data, headers=headers)

                print(savedata.text)
                json_data = json.loads(savedata.text)
                if json_data['success']:
                    return render_template('kiosk.html', waiver=True, laser=True)
            else:
                waiver_data = {
                    'cardid':cardid,
                    'codename':codename,
                    'custid':cardid
                }
                savewaiver = session.post('http://cloudKiosks:MioEnergyBlackCherry@kiosk.centermanagerpro.com/230/ajax/savewaiver.php', data=waiver_data, headers=headers)
                print(savewaiver.text)
                return render_template('kiosk.html', pic=True, laser=True)

        elif request.form['swipe'][:5] == "%LTCC":
            swipe = request.form['swipe']
            swipe_data = { 'swipe':swipe }
            cardid = swipe.split('?')[0][5:]            
            validate_swipe = session.post('http://cloudKiosks:MioEnergyBlackCherry@kiosk.centermanagerpro.com/230/ajax/validateswipe.php', data=swipe_data, headers=headers)
            json_data = json.loads(validate_swipe.text)
            print(swipe)
            if validate_swipe.status_code == 200 and json_data['reg']:
                print('passing')
                return render_template('kiosk.html', swipe=True, laser=True)
            else:
                flash('Card Not Registered')
                return render_template('kiosk.html', swipe=False, laser=True)
        elif request.form['swipe'] == '' or request.form['swipe'][0] != "%":
            flash('Card Read Error')
            return render_template('kiosk.html', swipe=False, laser=True)
        else:
            flash('not yet')
            return render_template('kiosk.html', swipe=True, laser=True)
        

            # uploadphoto = session.post('http://cloudKiosks:MioEnergyBlackCherry@kiosk.centermanagerpro.com/230/ajax/uploadphoto.php', data=test_photo, headers=headers)
            
            # print(uploadphoto.text)
    return render_template('kiosk.html', swipe=False, laser=True)

#cardid=0000000000006506&codename=TESTERCODE&
#custid=0000000000006506
