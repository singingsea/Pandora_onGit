# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 15:16:53 2018

@author: ZhaoX
"""
#%% load OMI data
import pandas as pd
# this is OMI NO2 at given location
OMI_data_path = 'file:///C:/Projects/OMI/NO2/download2/combined_data_at_a_location.csv'
df_omi = pd.read_csv(OMI_data_path)

# make a column to merging on
df_omi['UTC_index'] = pd.to_datetime(df_omi.UTC)
df_omi.set_index('UTC_index',inplace = True)
df_omi['UTC'] = df_omi.index.tz_localize('UTC')
df_omi.sort_values(by = 'UTC', inplace = True)


#%% load merged Pandora ZS/DS no2 and sky imager data
import shelve
# this is ZS/DS Pandora data + sky imager data
shelve_filename = 'C:\\Projects\\Zenith_NO2\\plots\\QDOAS_PanPS_ref2016_v3_Sky_imager'
# load data to shelve
my_shelf = shelve.open(shelve_filename)
for key in my_shelf:
    globals()[key]=my_shelf[key]
my_shelf.close()
ZS_DS_SKY.sort_values(by = 'UTC', inplace = True)

#%% merge data
df = pd.merge_asof(ZS_DS_SKY,df_omi,on ='UTC',tolerance=pd.Timedelta('30min'))

#%%
df.to_csv('C:\\Projects\\Zenith_NO2\\plots\\QDOAS_PanPS_ref2016_v3_Sky_imager_OMI.csv',index = False)


