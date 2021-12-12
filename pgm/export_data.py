# Python script to export observation time series data as csv files 
# Assumes that the MongoDB URI is on the localhost 
# Assumes that the collection is called cg_data
# If no parameters are passed then it exports 1 - 10 July 2021 to ../demo

import pymongo
import os
import pandas as pd
import sys 
import datetime

def get_vals(db, obs_name, start_time, end_time):
    obs_data = db["obs_data"]
    myquery = {'DataName':obs_name,'Time':{'$gte':start_time,"$lte":end_time}}
    print(f"{obs_name}: Found {obs_data.count_documents(myquery)} records")
    results = obs_data.find(myquery).sort('Time')
    
    data = []
    for doc in results:
        rec = {"Time":doc["Time"], "Value":doc["Value"]} 
        data.append(rec)
    return data 

# read in the path for the exported csv files 
args = sys.argv
if len(args) == 1: 
    rel_path = '../demo' 
    start_date = '2021-07-01' 
    end_date = '2021-07-10'  
else: 
    rel_path = args[1] 
    start_date = args[2]
    end_date = args[3] 

# make the full path 
dir_path = os.path.dirname(os.path.realpath(__file__)) 
exp_data_path = os.path.normpath(os.path.join(
    dir_path, rel_path))
start = datetime.datetime.fromisoformat(start_date) 
end = datetime.datetime.fromisoformat(end_date) 

print(f'Start date = {start.strftime("%Y-%m-%d")}, End date = {end.strftime("%Y-%m-%d")}, Path = {exp_data_path}') 

try:
    os.makedirs(exp_data_path)
except FileExistsError:
    pass

# set up the database collections - drop if they exist
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["cg_data"]

# get the list of observation time series that are enabled 
chart_list = db['charts'].find({'Enable':1}) 

# loop over the list of time series 
for chart in chart_list: 
    
    # make the full file path 
    file_name = f"{start.strftime('%Y-%m-%d')}.cgbaps.{chart['ChartName']}.{chart['Legend']}.csv" 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.normpath(os.path.join(exp_data_path, file_name))
    print(f"Writing {file_path}")

    # get the data 
    obs = get_vals(db, chart['DataName'],start, end)  

    # put it into a dataframe and write out as a csv file 
    if len(obs) > 0:
        obs_df = pd.DataFrame(obs) 
        obs_df.to_csv(file_path,index=False)
 