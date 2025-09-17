## This script will run daily, it will display the last month of available data for the sites included on the Dashboard
import fnmatch
import pandas as pd
import datetime
import os
from datetime import timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np
import requests
import json


"""TREX DF CREATION"""
## Set user on your system. Should be only variable in paths between computers.
user = "cpetrosi"

path = f'C:/Users/{user}/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files'
sites = ['OLA', 'WWF', 'VAC', 'SLC', 'FLT', 'WES']

#range df is a csv containing the min and max values for each parameter in the csiformat files
rangepath = f"C:/Users/{user}/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/suplementary/all_dl_ranges.csv"
rangedf = pd.read_csv(rangepath, header=[0],sep=',',na_values="NAN",engine='python')

rangedf.at[0, 'e_probe'] = -2
rangedf.at[0, 'H2O_probe'] = -10
rangedf.at[0, 'RH_3_1_1'] = -100
rangedf.at[0, 'T_DP_3_1_1'] = -100
rangedf.at[0, 'P_Tot'] = -2

all_st = []

for i in range(0,6):
  appended_data=[]
  for fname in fnmatch.filter(os.listdir(path),sites[i]+'*CSIFormat*'):
    df = pd.read_csv(path+'/'+fname, header=[0],skiprows=[0,2,3],sep=',',na_values="NAN",engine='python')
    df=df.reset_index(drop=True)
    df.TIMESTAMP= pd.to_datetime(df['TIMESTAMP'], format= 'mixed')
    appended_data.append(df)
  dff=pd.concat(appended_data)
  dff=dff.sort_values(by=['TIMESTAMP'])
  dff=dff.drop_duplicates()
  dff_all=dff
  all_st.append(dff_all)
df_all=pd.concat(all_st)

df_all=df_all.reset_index(drop=True)
df_all=df_all.drop_duplicates()
start_date = pd.Timestamp('2023-08-01')
mask = (df_all['TIMESTAMP'] >= start_date)
df_all = df_all.loc[mask]
df_all['ET'] = np.where(df_all['ET']<=0 , np.nan, df_all['ET'])
df_all['FC_mass'] = np.where(df_all['FC_mass']<-2 , np.nan, df_all['FC_mass'])
df_all['FC_mass'] = np.where(df_all['FC_mass']>1 , np.nan, df_all['FC_mass'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']<-10 , np.nan, df_all['TS5_2cm'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']> 100 , np.nan, df_all['TS5_2cm'])

#export df_all here or break down into smaller df's by site

VAC = df_all[df_all.Site=='VAC']
WWF = df_all[df_all.Site=='WWF']
OLA = df_all[df_all.Site=='OLA']
SLC = df_all[df_all.Site=='SLC']
FLT = df_all[df_all.Site=='FLT']
WES = df_all[df_all.Site=='WES']

trex_all = df_all

last_month = date.today() - timedelta(days=30)
last_month = np.datetime64(last_month)
trex_all = trex_all[trex_all["TIMESTAMP"] > last_month]

trex_all.to_csv(f"C:/Users/{user}/Documents/GitHub/crop-dashboard/sample-data/trex_data.csv")



test_calls = ['e_probe', 'e_sat_probe', 'H2O_probe', 'RH_3_1_1', 'T_DP_3_1_1', 'FW', 'H_FW', 'SW_IN', 'SW_OUT', 'LW_IN', 'LW_OUT', 'TA_3_1_1', 'T_CANOPY', 'G', 'CO2_sig_strgth_Min', 'H2O_sig_strgth_Min', 'CO2_density', 'H2O_density', 'LE', 'H', 'VPD', 'P_Tot', 'batt_volt']

"""OLIVE DF CREATION"""


path = f'C:/Users/{user}/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files'
sites = ['BLS_001', 'BLS_002', 'ORO_022', 'ORO_043', 'COR_CS3', 'ART_011', 'BRO_001']

rangepath = f"C:/Users/{user}/Box/TREX/MISCELLANEOUS/Datalogger_Report_Files/suplementary/all_dl_ranges.csv"
rangedf = pd.read_csv(rangepath, header=[0],sep=',',na_values="NAN",engine='python')


all_st = []

for i in range(0,7):
  appended_data=[]
  for fname in fnmatch.filter(os.listdir(path),sites[i]+'*CSIFormat*'):
    df = pd.read_csv(path+'/'+fname, header=[0],skiprows=[0,2,3],sep=',',na_values="NAN",engine='python')
    df=df.reset_index(drop=True)
    appended_data.append(df)
  dff=pd.concat(appended_data)
  dff=dff.sort_values(by=['TIMESTAMP'])
  dff=dff.drop_duplicates()
  dff['Site'] = sites[i]
  dff_all=dff
  all_st.append(dff_all)

df_all=pd.concat(all_st)
df_all=df_all.reset_index(drop=True)
df_all=df_all.drop_duplicates()
df_all.TIMESTAMP= pd.to_datetime(df_all['TIMESTAMP'], format= 'mixed')
df_all['FC_mass'] = np.where(df_all['FC_mass']<-2 , np.nan, df_all['FC_mass'])
df_all['FC_mass'] = np.where(df_all['FC_mass']>1 , np.nan, df_all['FC_mass'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']<-10 , np.nan, df_all['TS5_2cm'])
df_all['TS5_2cm'] = np.where(df_all['TS5_2cm']> 100 , np.nan, df_all['TS5_2cm'])

BL1 = df_all[df_all.Site=='BLS_001']
BL2 = df_all[df_all.Site=='BLS_002']
OR2 = df_all[df_all.Site=='ORO_022']
OR4 = df_all[df_all.Site=='ORO_043']
COR = df_all[df_all.Site=='COR_CS3']
ART = df_all[df_all.Site=='ART_011']
BRO = df_all[df_all.Site=='BRO_001']

matt_all = df_all

last_month = date.today() - timedelta(days=30)
last_month = np.datetime64(last_month)

matt_all = matt_all[matt_all["TIMESTAMP"] > last_month]
matt_all.to_csv(f"C:/Users/{user}/Documents/Github/crop-dashboard/sample-data/matt_data.csv")

"""LYNN ADDITION"""
path = f'C:/Users/{user}/Box/Gallo Downloads'
for fname in fnmatch.filter(os.listdir(path),'*CSIFormat*'):
  appended_data = []
  df = pd.read_csv(path+'/'+fname, header=[0],skiprows=[0,2,3],sep=',',na_values="NAN",engine='python')
  df=df.reset_index(drop=True)
  df.TIMESTAMP= pd.to_datetime(df['TIMESTAMP'], format= 'mixed')
  appended_data.append(df)
  dff=pd.concat(appended_data)
  dff=dff.sort_values(by=['TIMESTAMP'])
  dff=dff.drop_duplicates()
  dff_all=dff
  all_st.append(dff_all)
  df_all=pd.concat(all_st)
df_all.loc[df_all.Site == "New Ripp #2", "Site"] = "RIP_722"
df_all.loc[df_all.Site == "VOK", "Site"] = "VOK_001"
df_all.loc[df_all.Site == "SLM #1", "Site"] = "SLM_001"
df_all.loc[df_all.Site == "RIP760", "Site"] = "RIP_760"
df_all["TIMESTAMP"] = pd.to_datetime(df_all["TIMESTAMP"])


lynn_all = df_all



last_month = date.today() - timedelta(days=30)
last_month = np.datetime64(last_month)

lynn_all = lynn_all[lynn_all["TIMESTAMP"] > last_month]

lynn_all.to_csv(f"C:/Users/{user}/Documents/Github/crop-dashboard/sample-data/lynn_data.csv")

## All code below is used to send data to PythonAnywhere, optional for local use.

with open(f"C:/Users/{user}/Documents/GitHub/crop-dashboard/hidden_file.json", 'r') as file:
   user_info = json.load(file)

username = user_info["username"]
token = user_info["token"]  

file_path = f"C:/Users/{user}/Documents/GitHub/crop-dashboard/sample-data/trex_data.csv"
upload_path = "/home/audreypet/crop-dashboard/sample-data/trex_data.csv"

with open(file_path, 'rb') as f:
    response = requests.post(
        f'https://www.pythonanywhere.com/api/v0/user/{username}/files/path{upload_path}',
        headers={'Authorization': f'Token {token}'},
        files={'content': f}
    )


file_path = f"C:/Users/{user}/Documents/Github/crop-dashboard/sample-data/matt_data.csv"
upload_path = "/home/audreypet/crop-dashboard/sample-data/matt_data.csv"

with open(file_path, 'rb') as f:
    response = requests.post(
        f'https://www.pythonanywhere.com/api/v0/user/{username}/files/path{upload_path}',
        headers={'Authorization': f'Token {token}'},
        files={'content': f}
    )

file_path = f"C:/Users/{user}/Documents/Github/crop-dashboard/sample-data/lynn_data.csv"
upload_path = "/home/audreypet/crop-dashboard/sample-data/lynn_data.csv"

with open(file_path, 'rb') as f:
    response = requests.post(
        f'https://www.pythonanywhere.com/api/v0/user/{username}/files/path{upload_path}',
        headers={'Authorization': f'Token {token}'},
        files={'content': f}
    )