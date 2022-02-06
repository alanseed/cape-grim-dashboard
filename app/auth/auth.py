# Routes to manage user registration, login and logout 

from flask_login import LoginManager, current_user, login_manager, login_user, logout_user
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort
)
from app.db import get_db, get_latest_chart, add_user
from app.user import User
from app.auth.forms import LoginForm, RegistrationForm 
from app.auth.Util import is_safe_url

bp = Blueprint('auth', __name__, url_prefix='/auth')

# TO DO - have not set up the email to confirm address etc etc 
# TO DO - need a way for admin to manage user roles 
# register a new user, default role = guest. 
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

# user login route 
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
            next = request.args.get('next') 
            if next is not None:
                if not is_safe_url(next):
                    return abort(400)  
                return redirect(next) 
            else:
                return redirect(url_for('main.met'))    

        flash(error)
        return render_template('auth/login.html') 

    return render_template('auth/login.html') 

# user logout route 
@bp.route('/logout')
def logout():
    session.pop('_flashes', None)
    logout_user() 
    return redirect(url_for('main.met'))

def close_user(): 
    logout_user()
    session.clear()

def init_app(app):
    app.teardown_appcontext(close_user)    