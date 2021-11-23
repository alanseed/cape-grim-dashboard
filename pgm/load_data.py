# Python script to load data into the sql data base 
# The chart configuration file and list of observations are found at app/chart_config.csv and app/obs-list.csv  
# The sql data base is found at instance/cg-dashboard.sqlite 
import sqlite3 
import os
import sys
import json
import pandas as pd

# make the file names 
dir_path = os.path.dirname(os.path.realpath(__file__))
chart_config_name = os.path.normpath(os.path.join(
    dir_path, "../app/chart_config.csv"))
obs_list_name = os.path.normpath(os.path.join(
    dir_path, "../app/obs_list.csv"))
sql_name = os.path.normpath(os.path.join(
    dir_path, "../instance/cg-dashboard.sqlite"))

con = sqlite3.connect(sql_name) 
cur = con.cursor()
