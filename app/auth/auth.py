from flask_login import LoginManager, current_user, login_manager, login_user, logout_user
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db, get_latest_chart, add_user
from app.user import User
from app.auth.forms import LoginForm, RegistrationForm 
from app.auth.Util import is_safe_url
import functools 
from datetime import datetime

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if current_user.is_authenticated:
            return render_template('main/index_met.html', init = True)

        if form.validate_on_submit():
            error = add_user(form.username.data, form.password.data, "guest", form.email.data)
            if error != None:
                flash(error)
            else:
                flash('Congratulations, you are now a registered user!')
                return redirect(url_for("auth.login"))
        
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

# save the user id in the session and the user details in g 
@bp.route('/login', methods=('GET', 'POST'))
def login(): 
    session.pop('_flashes', None)
    form = LoginForm()
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        user = User(None) 
        error = user.get_user(username, password) 

        if error is None: 
            login_user(user) 
            flash('Logged in sucessfully') 
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            date = get_latest_chart().strftime("%Y-%m-%d")      
            return render_template('main/index_met.html',init=True, date=date)

        flash(error)
        return render_template('auth/login.html') 

    return render_template('auth/login.html') 

# check if session["user_id"] is valid 
# if not then set session["user_id"] to None 
@bp.before_app_request
def load_logged_in_user(): 
    user_id = session.get('user_id') 
    username = session.get('username')

    if user_id is not None:
        user_col = get_db()["users"]
        myquery = {"_id":user_id} 
        myuser = user_col.find_one(myquery)
        if myuser is None: 
            close_user() 
        else:
            g.username = username

@bp.route('/logout')
def logout():
    session.pop('_flashes', None)
    logout_user() 
    date = get_latest_chart().strftime("%Y-%m-%d")
    session['date'] = date
    return render_template('main/index_met.html', init=True, date=date)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

def close_user(): 
    logout_user()
    session.clear()

def init_app(app):
    app.teardown_appcontext(close_user)    