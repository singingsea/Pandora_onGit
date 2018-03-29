# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 11:03:52 2018

@author: ZhaoX
"""

import pandas as pd
import shelve

# output file
output_file = 'C:\\Projects\\Zenith_NO2\\plots\\QDOAS_PanPS_ref2016_v3_Sky_imager.csv'
shelve_filename_output = 'C:\\Projects\\Zenith_NO2\\plots\\QDOAS_PanPS_ref2016_v3_Sky_imager'
# this is the merged QDOAS processed 
shelve_filename = 'C:\\Projects\\Zenith_NO2\\plots\\QDOAS_PanPS_ref2016_v3'
# load data to shelve
my_shelf = shelve.open(shelve_filename)
for key in my_shelf:
    globals()[key]=my_shelf[key]
my_shelf.close()

merged_data.sort_values(by = 'UTC', inplace = True)

# this is merged sky imager data
sky_imager_data_file = 'C:\\Projects\\sky_imager\\sky_imager_Toronto_2015_2017_simple.csv'
# read in DataFrames
df_sky_imager = pd.read_csv(sky_imager_data_file)



# make a column to merging on
df_sky_imager['UTC_index'] = pd.to_datetime(df_sky_imager.dtUTC)
df_sky_imager.set_index('UTC_index',inplace = True)
df_sky_imager['UTC'] = df_sky_imager.index.tz_localize('UTC')
df_sky_imager.sort_values(by = 'UTC', inplace = True)



# merge data
ZS_DS_SKY = pd.merge_asof(merged_data,df_sky_imager,on='UTC',tolerance=pd.Timedelta('30min'))

ZS_DS_SKY.to_csv(output_file,index=False)





#%% save merged_data to shelve
import shelve
my_shelf = shelve.open(shelve_filename_output,'n') # 'n' for new
print(dir())
for key in dir():
    print(key)
    if key.find('ZS_DS_SKY') != -1:
        try:
            my_shelf[key] = globals()[key]
            print(key + ' saved! ')
        except TypeError:
            #
            # __builtins__, my_shelf, and imported modules can not be shelved.
            #
            print('ERROR shelving: {0}'.format(key))
    else:
        #print('key not matched')
        pass
my_shelf.close()

# load data to shelve
my_shelf = shelve.open(shelve_filename_output)
for key in my_shelf:
    globals()[key]=my_shelf[key]
my_shelf.close()

