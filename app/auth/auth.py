from flask_login import LoginManager, current_user, login_user
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db 
from app.forms import LoginForm, RegistrationForm
import functools
from . import app 

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegistrationForm()
    if request.method == 'POST':
        if current_user.is_authenticated:
            return redirect(url_for('index'))

        if form.validate_on_submit():
            db = get_db()
            try:
                db.execute(
                    "INSERT INTO user (username, email,role,password) VALUES (?, ?, ?,?)",
                    (form.username.data, form.email.data, "guest", generate_password_hash(form.password.data)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {form.username.data} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return current_app.send_static_file('index.html')

        flash(error)

    return render_template('auth/login.html') 


@login_manager.user_loader
def load_user(user_id):




    return User.get(user_id)

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone() 

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

