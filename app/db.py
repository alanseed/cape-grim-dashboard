from flask_sqlalchemy import SQLAlchemy 

import click
from flask import current_app, g
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash

def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy( ) 
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.session.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.session.execute(f.read().decode('utf8')) 

    username = 'admin'
    password = 'admin'
    role = 'admin'
    email = 'guest@example.com'
    try:
        db.session.execute(
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
