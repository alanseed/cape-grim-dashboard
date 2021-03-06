# Python script to load data into the sql data base
# The collections are dropped and the data reloaded
# Assumes that all the csv files are in ../demo 
# Reads the chart configuration file demo/chart_config.csv 
# Observation time series data are read as csv files 
# [Start time].cgbaps.[chart name].[legend name].csv 
# 
# In the case of the demo files, these have been generated using 
# export_data.py based on the initial 1-year data drop  
# The chart configuration file is found at app/chart_config.csv 

# Writes to the cg_demo collection on URI "mongodb://localhost:27017/" 

import pymongo
import os
import pandas as pd
import sys
from os import environ,path 
from dotenv import load_dotenv 

# read in the environment 
basedir = path.abspath(path.dirname(__file__))
env_name =path.normpath(path.join(basedir, '../app/.env')) 
load_dotenv(env_name)

# read in the tables to be re-loaded
table_list = sys.argv
if len(table_list) == 1:
    table_list = ["charts","obs_data"]

# table_list = ["obs_data","charts"]

# make the file names
dir_path = os.path.dirname(os.path.realpath(__file__))
chart_config_name = os.path.normpath(os.path.join(
    dir_path, "../app/chart_config.csv"))
obs_data_path = os.path.normpath(os.path.join(
    dir_path, "../demo"))

# set up the database collections - drop if they exist
DB_URI=str(environ.get('DB_URI'))
DB_NAME=str(environ.get('DB_NAME'))
print(f"URI = {DB_URI}, Name = {DB_NAME}") 
if (DB_URI is None) or (DB_NAME is None):
    exit 

client = pymongo.MongoClient(DB_URI)
db = client[DB_NAME]
col_names = db.list_collection_names()

if "charts" in table_list:
    if "charts" in col_names:   
        db["charts"].drop()
    charts = db["charts"]

    # load the chart configurations
    charts_df = pd.read_csv(chart_config_name)
    charts_df.rename(columns={"Unnamed: 0":"Index"}, inplace=True) 
    charts_df["DataName"].str.strip()
    print(charts_df.info())

    if charts_df["DataName"].is_unique: 
        charts_dict = charts_df.to_dict(orient='records')
        for ia in range(len(charts_dict)):
            user_id = charts.insert_one(charts_dict[ia]).inserted_id
    else: 
        counts = charts_df["DataName"].value_counts( )
        print(counts)
        sys.exit("DataNames are not unique")

if "obs_data" in table_list:
    if "obs_data" in col_names:
        db["obs_data"].drop()
    obs_data = db["obs_data"]
    db.obs_data.create_index('DataName')

    # get the list of the files with the observations
    print(f"Reading files in data directory {obs_data_path}")
    file_names = os.listdir(obs_data_path)

    # loop over the file names and make the lists of observations for each chart
    # read the time in as a string and then convert to datatime64[ns, UTC]
    names = ["Time", "Value"]
    dtypes = {'Time': 'str', 'Value': 'float'}
    parse_dates = ['Time']
    number_files = 0 
    for file in file_names:
        full_path = obs_data_path + "/" + file
        number_files += 1 
        print(f"{number_files} - reading {full_path}")
        parts = file.split(".")
        chart_name = parts[2]
        legend = parts[3] 
        
        # get the data name for this chart and legend 
        chart = db.charts.find_one({"ChartName":chart_name,"Legend":legend})
        if chart == None:
            message = f"Could not find Chart {chart_name} and Legend = {legend} combo in the charts database"
            sys.exit(message) 
        data_name = chart["DataName"]
        obs_df = pd.read_csv(full_path, parse_dates=['Time'],date_parser=lambda x: pd.to_datetime(x, utc=True))

        nrecs = 0
        rec_list = []
        for irec in obs_df.index:
            rec = {"Time": obs_df["Time"][irec],
                   "DataName": data_name,
                   "Value": obs_df["Value"][irec]}
            rec_list.append(rec)
            nrecs += 1

        if len(rec_list) > 0:
            result = obs_data.insert_many(rec_list)
        print(f"Read {nrecs} records")

client.close()
