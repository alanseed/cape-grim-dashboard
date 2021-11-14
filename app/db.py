import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

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

class User:
    def __init__(self, username, email):
        self.username = username 
        self.email = email 
        self.role = 'guest'
        self.password = ' '
