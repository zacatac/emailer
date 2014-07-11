from flask import request, session, g, redirect, url_for, abort, \
     render_template, flash, _app_ctx_stack, jsonify, Blueprint
import util
from app import cache

# from app.forms import MyForm

main = Blueprint('main', __name__)
USERNAME = 'admin'
PASSWORD = 'default'

# @main.teardown_appcontext
# def shutdown_session(exception=None):
#     """Closes the database again at the end of the request."""
#     db_session.remove()

@main.route('/')
@cache.cached(timeout=1000)
def navigate():
    return render_template('navigate.html')

@main.route('/calendar')
def calendar():
    return render_template('calendar.html',calendar=None)    


@main.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('main.navigate'))

@main.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != USERNAME:
            error = 'Invalid username'
        elif request.form['password'] != PASSWORD:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('main.navigate'))
    return render_template('login.html', error=error)


# @main.route('/wtform', methods=['GET', 'POST'])
# def wtform():
#     form = MyForm()

#     if request.method == 'GET':
#         return render_template('wtform_example.html', form=form)
#     elif request.method == 'POST':
#         if form.validate_on_submit():
#             flash("The form was successfully submitted", 'success')
#         else:
#             flash("There was a problem submitting the form!", 'danger')
#         return render_template('wtform_example.html', form=form)
