"""
Created on Wed Feb 20 03:56:19 2019
Author: Dalyapraz 
This code parses all JSON files from folder into Data Frames and then saves into CSV files
At the end there are 3 CSV files: alers, jams and irregularities
"""
import os, json
import pandas as pd
from pandas.io.json import json_normalize #import package for flattening json in pandas Data Frame

#Take all files form folder ending with .json
path_to_json = '/Users/dalyapraz/Desktop/City of LA/Waze/waze json dec31-jan9/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]


#Load first json object 
with open(os.path.join(path_to_json, json_files[0])) as first_file:
    data = json.load(first_file)
    
#ALERTS
#Create data frame for alerts from first file
df_alerts= json_normalize(data,'alerts', ['startTime', 'endTime'])
print(df_alerts.info())

#Go through all files starting from 2nd json_files[1], if file doesn't have object alerts - continue
for js in json_files[1:]:
    with open(os.path.join(path_to_json, js)) as json_file:
        json_data = json.load(json_file)
        try:
            df_file= json_normalize(json_data,'alerts', ['startTime', 'endTime'])
            df_alerts = df_alerts.append(df_file,ignore_index=True)
            print(json_files.index(js))
        except:
            print('no alerts for file', js)
            continue

#Load data into csv file
df_alerts.to_csv('alerts.csv', encoding='utf-8', index=False)
print('File with ALERTS is ready', df_alerts.info())


#IRREGULARITIES
#Create data frame for irregularities from first file, if there is no such object try with next

try :
    df_irr= json_normalize(data,['irregularities'],  ['startTime', 'endTime'])
    print(df_irr.info())
except:
    with open(os.path.join(path_to_json, json_files[1])) as first_file:
        data = json.load(first_file)
        
df_irr= json_normalize(data,['irregularities'],  ['startTime', 'endTime'])
print(df_irr.info()) 

#Go through all files starting from 2nd json_files[1], if file doesn't have object irregularities - continue
for js in json_files[1:]:
    with open(os.path.join(path_to_json, js)) as json_file:
        json_data = json.load(json_file)
        try:
            df_file= json_normalize(json_data,['irregularities'], ['startTime', 'endTime'])
            df_irr = df_irr.append(df_file,ignore_index=True)
            print(json_files.index(js))
        except:
            print('no irregularities for file', js)
            continue

#Load data into csv file
df_irr.to_csv('irregularities_full.csv', encoding='utf-8', index=False)
print('File with IRREGULARITIES is ready', df_irr.info())


#JAMS
#Create data frame for alerts from first file
df_jams= json_normalize(data,['jams'], ['startTime', 'endTime'])
print(df_jams.info())

#Go through all files starting from 2nd json_files[1], if file doesn't have object jams - continue
for js in json_files[1:]:
    with open(os.path.join(path_to_json, js)) as json_file:
        json_data = json.load(json_file)
        try:
            df_file= json_normalize(json_data,['jams'], ['startTime', 'endTime'])
            df_jams = df_jams.append(df_file,ignore_index=True)
            print(json_files.index(js))
        except:
            print('no jams for file', js)
            continue

#Load data into csv file
df_jams.to_csv('jams_full.csv', encoding='utf-8', index=False)
print('File with JAMS is ready', df_jams.info())
