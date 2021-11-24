from flask_login import LoginManager, current_user, login_manager, login_user
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from app.db import get_db, add_user, get_user_id, is_valid_user, User 
from app.auth.forms import LoginForm, RegistrationForm
import functools
from bson.objectid import ObjectId

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('index'))

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
    form = LoginForm()
    error = None 
    if request.method == 'POST':
        username = str(request.form['username'])
        password = str(request.form['password'])
        error = is_valid_user(username, password)

        if error is None:
            user_id = get_user_id(username)
            session.clear()
            session['user_id'] = user_id
            g.user = User(user_id)
            g.username = username 
            return render_template('main/index.html')

        flash(error)
        return render_template('auth/login.html')
    return render_template('auth/login.html') 

# check if session["user_id"] is valid 
# if not then set session["user_id"] to None 
@bp.before_app_request
def load_logged_in_user():
    db = get_db()
    g.user = None 
    user_id = session.get('user_id') 
    if user_id is not None:
        user_col = db["users"]
        myquery = {"_id":user_id} 
        myuser = user_col.find_one(myquery)
        if myuser is None:
            session["user_id"] = None
        else:
            g.user = User(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    g.user = None 
    return render_template('main/index.html')

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

