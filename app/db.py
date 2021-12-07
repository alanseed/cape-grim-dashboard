# This module contains all the database queries, except for those in forms.py 
import pymongo

import click
from flask import current_app, g,session
from flask.cli import with_appcontext
from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash, generate_password_hash
import json
import datetime 

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
    print(add_user(username,password,role,email))

# Add a user to the user table  
def add_user(username, password, role, email):
    hp = generate_password_hash(password)
    user_dict = {"name":username,"password":hp,"role":role,"email":email}

    user = g.db["users"]
    error = None 
    
    # check if the username exists 
    myquery = {"name":username}
    cursor = user.find(myquery)
    if cursor.count() > 0:
         error = f"User {username} is already registered." 
    else: 
        user_id = user.insert_one(user_dict).inserted_id
        error = f"User {username} registered."
    return error 

# Check if username, password pair is in the user table 
# Returns None if pair is valid else the error string 
def is_valid_user(username,password):
    user = get_db()["users"]
    error = None

    # check if the username exists 
    myquery = {"name":username}
    mydoc = user.find_one(myquery)
    if mydoc is None: 
        error = f"User {username} not found." 
    elif not check_password_hash(mydoc['password'], password):
        error = "Incorrect password"
    return error  

# return the _id for this user 
def get_user_id(username):
    user = get_db()["users"]
    myquery = {"name":username} 
    myuser = user.find_one(myquery)
    user_id = str(myuser["_id"])
    print (f"User id = {user_id}")
    return user_id

# Read the list of observations and put them into the obs_table 
def add_observations():
    return 

# return a dictionary of user details for a user_id 
def get_user(user_id): 
    user = get_db()["users"]
    myquery = { "_id":user_id}
    myuser = user.find_one(myquery) 
    return myuser

# return a list of obs names 
def get_obs_list(): 
    obs_names = get_db()["obs_names"]
    names = []
    for irec in obs_names.find():
        names.append(irec["ObsList"])
    return json.dumps(names)


# return a list dictionaries {time, value}
def get_vals(obs_name, start_time, end_time):
    obs_data = get_db()["obs_data"]
    myquery = {'Name':obs_name,'Time':{'$gte':start_time,"$lte":end_time}}
    results = obs_data.find(myquery)
    data = []
    for doc in results:
        rec = {"Time":doc["Time"], "Value":doc["Value"]} 
        data.append(rec)

    return data 
    
# write the chart to the data base 
# assumes that fig is the JSON buffer from plotly 
def add_chart(chart_name, start_time, end_time, fig): 
    
    chart = get_db()["chart_data"] 
    chart_dict = { 
        "ChartName":chart_name, 
        "StartDate":start_time, 
        "EndDate":end_time, 
        "GenTime":datetime.datetime.utcnow(), 
        "Data":fig
    }
    user_id = chart.insert_one(chart_dict).inserted_id

# read the chart from the data base 
# returns a dictionary 
def get_chart(chart_name, start_date): 
    chart = get_db()["chart_data"] 
    myquery = {'ChartName':chart_name, 'StartDate':start_date} 
    result = chart.find_one(myquery) 
    return result 

# delete all charts that were generated before a certain date 
# returns the numer of charts that were deleted 
def delete_charts(gen_date): 
    chart = get_db()["chart_data"]
    myquery = {'GenDate':{"$lte":gen_date}}
    result = chart.delete_many(myquery)         
    return result.deleted_count 

# Function returns true if there are charts for date 
def is_valid_date(date):
    start_date = datetime.datetime.fromisoformat(date)
    chart = get_db()["chart_data"] 
    myquery = {'StartDate':start_date} 
    result = chart.find_one(myquery) 
    if result is None:
        return False
    else:
        return True 

# function to return the date of the latest charts 
def get_latest_chart():
    chart = get_db()["chart_data"] 
    result = chart.find().sort("StartDate",-1)[0] 
    return result["StartDate"]

# flask command to initialise the database with the admin user 
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.') 

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# User class for user authentication 
class User(UserMixin):
    def __init__(self):
        self.id = None
        self._is_authenticated = False
        self._is_active = False
        self._is_anoymous = False

    def __init__(self, user_id):
        self.id = user_id
        self._is_authenticated = True
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
