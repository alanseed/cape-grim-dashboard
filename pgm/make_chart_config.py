# Python script to generate the configuration file for the charts 
#
# The details for each chart were included as a page in a spreadsheet, but did not include a list 
# of observations for each chart
# The observation data I received are time,data pairs of one observation. The chart and observation 
# names are encoded in the file name 
# The list of observations is encoded in JSON and the string is added to the dataframe columns "ObsList"
# This script parses the files names to derive the list of observations for each chart and writes
# the complete configuration as a csv file 

import os,sys  
import json 
import pandas as pd

# make the file names etc 
dir_path = os.path.dirname(os.path.realpath(__file__)) 
chart_spec_name = os.path.join(dir_path,"CBAPS_Daily_Reports.csv")
data_path = os.path.normpath(os.path.join(dir_path,"../data"))
out_file_name = os.path.normpath(os.path.join(dir_path,"../app/static/chart_config.csv"))

#get the list of the files 
print (f"Reading the files in {data_path}") 
file_names = os.listdir(data_path)

#loop over the file names and make the lists of observations for each chart 
chart_list = [] 
for file in file_names:
    parts = file.split(".")
    chart_name = parts[2]
    obs_name = parts[3] 

    this_chart = None  
    #loop over the list of charts 
    for ia in range(len(chart_list)):
        if chart_list[ia].get("name") == chart_name:
            this_chart = chart_list[ia]
            break

    #add a new chart if name not in the list 
    if this_chart == None: 
        temp = {"name":chart_name,"obs":[obs_name]}
        chart_list.append(temp)
    else: 
        this_chart["obs"].append(obs_name)    

#read the chart specifications from the csv file into a dataframe 
chart_spec_df = pd.read_csv(chart_spec_name)
chart_spec_df['ObsList'] = chart_spec_df['ObsList'].astype(str) 

# get the list of observations and add them to the dataframe 
for ia in range(len(chart_spec_df)):
    chart_name = chart_spec_df.loc[ia,"Name"] 
    this_chart = None  
    for ib in range(len(chart_list)):
        if chart_list[ib].get("name") == chart_name:
            this_chart = chart_list[ib]
            break
    
    if this_chart == None:
        #did not find the chart name in the data files 
        chart_spec_df.iloc[ia, 1] = 0
    else:
        # did not find obs in data files so disable this chart 
        if len(this_chart["obs"]) == 0:
            chart_spec_df.iloc[ia, 1] = 0
        else:
            # encode list as JSON so we have a string to work with
            obs_string = json.JSONEncoder().encode(this_chart["obs"])
            chart_spec_df.iloc[ia, 2] = obs_string 

#write out the chart configuration as a csv file 
print(f"Writing chart configuration to {out_file_name}")
chart_spec_df.to_csv(out_file_name)