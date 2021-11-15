from flask_login import LoginManager, current_user, login_manager, login_user
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db, add_user, User 
from app.auth.forms import LoginForm, RegistrationForm
import functools

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
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None
        sql = f"SELECT * FROM user WHERE username = '{username}'"
        user = db.execute(sql).fetchone()

        if user is None:
            error = 'Incorrect username.'
            g.user = None
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
            g.user = None

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            g.user = None
            g.user = User(user['id']) 
            return render_template('main/index.html')

        flash(error)
        return redirect(url_for('/'))

    return render_template('auth/login.html') 

@bp.before_app_request
def load_logged_in_user():
    g.user = None 
    user_id = session.get('user_id')
    if user_id is not None:
        sql = f"SELECT * FROM user WHERE id = '{user_id}'"
        user = get_db().execute(sql).fetchone() 
        if user is None:
            session['user_id'] = None
        else:            
            g.user = User(user_id)     

@bp.route('/logout')
def logout():
    session.clear()
    g.user = None 
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

