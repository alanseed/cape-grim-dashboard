import sqlite3

import click
from flask import current_app, g,session
from flask.cli import with_appcontext
from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash, generate_password_hash

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8')) 

    username = 'admin'
    password = 'admin'
    role = 'admin'
    email = 'guest@example.com'
    try:
        db.execute(
            "INSERT INTO user (username, email, role, password) VALUES (?, ?, ?, ?)",
            (username, email, role, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        error = f"User {username} is already registered."

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.') 

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)




class User(UserMixin):
    def __init__(self):
        self.id = None
        self._is_authenticated = False
        self._is_active = True
        self._is_anoymous = False

    def is_authenticated(self):
        return self._is_authenticated


    def is_authenticated(self, val):
        self._is_authenticated = val


    def is_active(self):
        return self._is_active


    def is_active(self, val):
        self._is_active = val

    def is_anoymous(self):
        return self._is_anoymous

    def is_anoymous(self, val):
        self._is_anoymous = val

    def check_pwd(self, request_pwd, pwd):
        """Check user request pwd and update authenticate status.

        Args:
            request_pwd: (str)
            pwd: (unicode)
        """
        if request_pwd:
            self.is_authenticated = request_pwd == str(pwd)
        else:
            self.is_authenticated = False   
