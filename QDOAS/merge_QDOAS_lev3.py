# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 14:17:55 2018

@author: xiaoy
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import dateutil.parser
import numpy as np

def open_shelf(shelve_filename):
    import shelve
    my_shelf = shelve.open(shelve_filename)
    
    for key in my_shelf:
        globals()[key]=my_shelf[key]
    my_shelf.close()  
    

#%%
def add_datetime(df):
    
    # add timestamp
    print('Convert ISO 8601 time to Python-dateutil datetime')
    df['time'] = list(map(dateutil.parser.parse, df['Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)']))
    # add UTC and LTC
    print('Add UTC column to dataframe')              
    df['UTC'] = df.time.dt.tz_convert('UTC')
    if location in sites_list.keys():
        print('Add LTC column to dataframe')              
        df['LTC'] = df.time.dt.tz_convert(sites_list[location])
    else:
       print('\n')
       print('-------- Warnning: -----------')
       print('Do not know timezone for the new measurement location (not in measurement location lists) : "' + location + '"')
       print('No local time (LTC) column created for this site.')
       print('------------------- \n')
    return df

import sys
sys.path.insert(0, 'E:\\Pandora_onGit\\BlikP')
from sites_list import sites_list    
location = 'Downsview'
lev3_shelve_filename = 'E:\\Projects\\Zenith_NO2\\Pan_level3data_V2_plots\\lev3.out'
QDOAS_shelve_filename = 'E:\\Projects\\Zenith_NO2\\QDOAS_outputs\\QDOAS_outputs.out'
plotpath = 'E:\\Projects\\Zenith_NO2\\plots\\'

open_shelf(lev3_shelve_filename)
open_shelf(QDOAS_shelve_filename)
df_lev3 = add_datetime(df_lev3)
df_QDOAS['UTC_simple'] = df_QDOAS['Date (DD/MM/YYYY)_Time (hh:mm:ss)']

df_QDOAS.set_index(['UTC_simple'],inplace = True)
df_QDOAS['UTC'] = df_QDOAS.index.tz_localize('UTC')
df_QDOAS.sort_values(by = 'UTC', inplace = True)
df_lev3.sort_values(by = 'UTC', inplace = True)
merged_data = pd.merge_asof(df_QDOAS, df_lev3, on='UTC',tolerance=pd.Timedelta('1hr'))

merged_data.y = merged_data['NO2_Vis.SlCol(no2)']
merged_data.x = merged_data['NO2_VCD']
merged_data.ci = merged_data['Fluxes 450']/merged_data['Fluxes 500']


font = {'family' : 'DejaVu Sans', 'weight' : 'bold', 'size'   : 12}
plt.rc('font', **font)
fig = plt.figure(figsize=(22, 18), dpi=200, facecolor='w', edgecolor='k') 
cm = plt.cm.get_cmap('jet')
gs = gridspec.GridSpec(1, 1, height_ratios=[1], width_ratios=[1]) 

ax0 = plt.subplot(gs[0])
#sc = ax0.scatter(merged_data.x, merged_data.y, merged_data.ci, s=10, cmap=cm)
sc = ax0.scatter(merged_data.x, merged_data.y, merged_data.ci, cmap=cm)
plt.colorbar(sc).set_label('CI')
ax0.grid()
ax0.set_ylabel(ylabel_1 + ' dSCD [DU]')
ax0.set_xlabel('VCD [DU]')
ax0.legend()
ax0.set_title(filepath)

plt.tight_layout()
plt.savefig(plotpath +'test.png')
#plt.show()
plt.close()





