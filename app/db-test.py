# This module contains all the database queries, except for those in forms.py 
import pymongo
import click
from flask import g 
from flask.cli import with_appcontext 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin  
from datetime import datetime
from bson.objectid import ObjectId 
from app import login 
from user import User

@login.user_loader
def load_user(id):
    return User.get_user_id(id) 

def get_db():
    if 'client' not in g:
        g.client = pymongo.MongoClient("mongodb://localhost:27017/") 
    if 'db' not in g:
        g.db = g.client["cg_data"] 
    return g.db

def close_db(e=None):
    client = g.pop('client',None)
    db = g.pop('db',None)
    if client is not None:
        client.close()

# method to drop the collections in the database 
# also creates the cg-data database if required 
def init_db():
    # check if cg_data exists and if yes delete it 
    client = pymongo.MongoClient("mongodb://localhost:27017/") 
    database_list = client.database_names()

    if "cg_data" in database_list:
        client.drop_database("cg_data")

    # make the database     
    db = client["cg_data"]
    g.client = client
    g.db = db 
    
    #add the default admin user 
    username ="admin"
    password="admin"
    role="admin"
    email="admin@email.address" 
    response = User().add_user(username,password,role,email) 
    print(response)


# flask command to initialise the database with the admin user 
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.') 

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)      
