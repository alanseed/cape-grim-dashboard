# Python script to load data into the sql data base
# The collections are dropped and the data reloaded
# The chart configuration file and list of observations are found at app/chart_config.csv and app/obs-list.csv
import pymongo
import os
import pandas as pd

# make the file names
dir_path = os.path.dirname(os.path.realpath(__file__))
chart_config_name = os.path.normpath(os.path.join(
    dir_path, "../app/chart_config.csv"))
obs_list_name = os.path.normpath(os.path.join(
    dir_path, "../app/obs_list.csv"))
obs_data_path = os.path.normpath(os.path.join(
    dir_path, "../data"))

# set up the database collections - drop if they exist
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["cg_data"]
col_names = db.list_collection_names()

if "obs_names" in col_names:
    db["obs_names"].drop()
obs_name = db["obs_names"]

if "charts" in col_names:
    db["charts"].drop()
charts = db["charts"]

if "obs_data" in col_names:
    db["obs_data"].drop()
obs_data = db["obs_data"]
db.obs_data.create_index('Name')

# load the list of observation names
obs_df = pd.read_csv(obs_list_name)
obs_df.rename(columns={"Unnamed: 0": "Index"}, inplace=True)
obs_df["Index"] = obs_df["Index"].map(str)
obs_dict = obs_df.to_dict(orient="records")
for ia in range(len(obs_dict)):
    user_id = obs_name.insert_one(obs_dict[ia]).inserted_id

# load the chart configurations
charts_df = pd.read_csv(chart_config_name)
charts_df.rename(columns={"Unnamed: 0": "Index"}, inplace=True)
charts_dict = charts_df.to_dict(orient='records')
for ia in range(len(charts_dict)):
    user_id = charts.insert_one(charts_dict[ia]).inserted_id


# get the list of the files with the observations
print(f"Reading files in data directory {obs_data_path}")
file_names = os.listdir(obs_data_path)

# loop over the file names and make the lists of observations for each chart
# read the time in as a string and then convert to datatime64[ns, UTC]
names = ["Time", "Value"]
dtypes = {'Time': 'str', 'Value': 'float'}
parse_dates = ['Time']
for file in file_names:
    full_path = obs_data_path + "/" + file
    parts = file.split(".")
    chart_name = parts[2]
    obs_name = parts[3]
    obs_df = pd.read_csv(full_path, header=None, names=names, dtype=dtypes, parse_dates=parse_dates,
                         date_parser=lambda x: pd.to_datetime(x, utc=True))
    nrecs = 0 
    rec_list = [] 
    for irec in obs_df.index:
        rec = {"Time": obs_df["Time"][irec],
               "Name": obs_name,
               "Value:": obs_df["Value"][irec]}
        rec_list.append(rec)
        nrecs += 1 

    if len(rec_list) > 0:
        result = obs_data.insert_many(rec_list) 
        print(f"Read {nrecs} records from {full_path}")

client.close()
