# This module contains all the database queries, except for those in forms.py 
import pymongo

import click
from flask import current_app, g,session
from flask.cli import with_appcontext
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash, generate_password_hash
import json
import datetime 
from os import environ

def get_db():
    DB_URI=environ.get('DB_URI')
    DB_NAME=environ.get('DB_NAME')  

    if 'client' not in g:
        g.client = pymongo.MongoClient(DB_URI) 
    if 'db' not in g:
        g.db = g.client[DB_NAME] 
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
    DB_URI=environ.get('DB_URI')
    DB_NAME=environ.get('DB_NAME')  

    client = pymongo.MongoClient(DB_URI) 
    database_list = client.database_names()

    if DB_NAME in database_list:
        client.drop_database(DB_NAME)

    # make the database     
    db = client[DB_NAME]
    g.client = client
    g.db = db 
    
    #add the default admin user 
    username =environ.get('ADMIN_NAME') 
    password=environ.get('ADMIN_PW')
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

# Read the list of observations and put them into the obs_table 
def add_observations():
    return 

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
    myquery = {'DataName':obs_name,'Time':{'$gte':start_time,"$lte":end_time}}
    results = obs_data.find(myquery).sort('Time')
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
    if get_db()["chart_data"].count_documents(filter={}) > 0:
        chart = get_db()["chart_data"] 
        result = chart.find().sort("StartDate",-1)[0] 
        return result["StartDate"]
    else:
        return None        

# return a list of time stamps (seconds) that have charts in the cache 
def get_dates(start,end): 
    # get the charts for these dates 
    start_date = datetime.datetime.fromisoformat(start) 
    end_date = datetime.datetime.fromisoformat(end) 
    chart = get_db()['chart_data'] 
    myquery = {'StartDate':{"$gte":start_date, "$lte":end_date}}
    results = chart.find(myquery).sort("StartDate")         

    #build a list of the dates 
    dates = {}
    for res in results: 
        this_date = int(res['StartDate'].timestamp())
        timestamp = str(this_date)
        if timestamp not in dates: 
            dates[timestamp] = 1 
        else: 
            dates[timestamp] += 1             
    return dates 

# flask command to initialise the database with the admin user 
@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.') 

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
