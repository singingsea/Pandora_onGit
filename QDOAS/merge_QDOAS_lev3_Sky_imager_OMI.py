# -*- coding: utf-8 -*-
"""
Created on Mon Mar 26 15:16:53 2018

@author: ZhaoX
"""

def open_shelf(shelve_filename):
    import shelve
    my_shelf = shelve.open(shelve_filename)
    
    for key in my_shelf:
        globals()[key]=my_shelf[key]
    my_shelf.close()  

#%% load OMI data
import pandas as pd
# this is OMI NO2 at given location
#OMI_data_path = 'file:///C:/Projects/OMI/NO2/download2/combined_data_at_a_location.csv' # old file, without pixel information
#OMI_data_path = 'file:///C:/Projects/OMI/NO2/download2/combined_data_at_a_location_pixinfo2.csv'# this file has pixel information, Fov75area and viewing zenith angle
OMI_data_path = 'file:///C:/Projects/OMI/NO2/download2/combined_data_at_a_location_pixinfo2_onlysmallpix.csv'# this file has pixel information, the f1 and f2 averaging only use small pixel with VAZ <=45. 
df_omi = pd.read_csv(OMI_data_path)

# make a column to merging on
df_omi['UTC_index'] = pd.to_datetime(df_omi.UTC)
df_omi.set_index('UTC_index',inplace = True)
df_omi['UTC'] = df_omi.index.tz_localize('UTC')
df_omi.sort_values(by = 'UTC', inplace = True)


#%% load merged Pandora ZS/DS no2 and sky imager data
# this is ZS/DS Pandora data + sky imager data
#shelve_filename = 'C:\\Projects\\Zenith_NO2\\plots\\QDOAS_PanPS_ref2016_v3_Sky_imager'
shelve_filename = 'C:\\Projects\\Zenith_NO2\\plot_lev3_corrected\\QDOAS_PanPS_ref2016_v5_Sky_imager'
open_shelf(shelve_filename)

ZS_DS_SKY.sort_values(by = 'UTC', inplace = True)# this is Pandora ZS/DS no2 and sky imager data

#%% merge data
df_omi_closest = df_omi.copy()
df_omi_closest = df_omi_closest[df_omi_closest.mean_type == 'closest']
df_omi_closest = pd.merge_asof(ZS_DS_SKY,df_omi_closest,on ='UTC',tolerance=pd.Timedelta('30min'))

df_omi_f1 = df_omi.copy()
df_omi_f1 = df_omi_f1[df_omi_f1.mean_type == 'dis_f1']
df_omi_f1 = pd.merge_asof(ZS_DS_SKY,df_omi_f1,on ='UTC',tolerance=pd.Timedelta('30min'))

df_omi_f2 = df_omi.copy()
df_omi_f2 = df_omi_f2[df_omi_f2.mean_type == 'dis_f2']
df_omi_f2 = pd.merge_asof(ZS_DS_SKY,df_omi_f2,on ='UTC',tolerance=pd.Timedelta('30min'))

#%%
#df.to_csv('C:\\Projects\\Zenith_NO2\\plots\\QDOAS_PanPS_ref2016_v3_Sky_imager_OMI.csv',index = False)
#df.to_csv('C:\\Projects\\Zenith_NO2\\plot_lev3_corrected\\QDOAS_PanPS_ref2016_v5_Sky_imager_OMI.csv',index = False)
df_omi_closest.to_csv('C:\\Projects\\Zenith_NO2\\plot_lev3_corrected\\QDOAS_PanPS_ref2016_v5_Sky_imager_OMI_closest_onlysmallpix.csv',index = False)
df_omi_f1.to_csv('C:\\Projects\\Zenith_NO2\\plot_lev3_corrected\\QDOAS_PanPS_ref2016_v5_Sky_imager_OMI_f1_onlysmallpix.csv',index = False)
df_omi_f2.to_csv('C:\\Projects\\Zenith_NO2\\plot_lev3_corrected\\QDOAS_PanPS_ref2016_v5_Sky_imager_OMI_f2_onlysmallpix.csv',index = False)


