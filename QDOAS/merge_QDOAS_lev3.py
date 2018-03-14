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

def get_single_fitting_result(df,routine, start_wv,end_wv,poly,offset,wv_change,fit_config_idx):
    df = df[df['Column 1: Two letter code of measurement routine'] == routine]
    df = df[df['Column 15: Starting wavelength of fitting window [nm]'] == start_wv][df['Column 16: Ending wavelength of fitting window [nm]'] == end_wv]
    df = df[df['Column 17: Order of smoothing polynomial used in spectral fitting'] == poly][df['Column 18: Order of offset polynomial used in spectral fitting, -1=no offset'] == offset][df['Column 19: Order of wavelength change polynomial used in spectral fitting, -1=no wavelength change'] == wv_change]
    df = df[df['Column 20: Sum over 2^i with i being a fitting configuration index, 0=Ring spectrum is fitted, 1=molecular scattering is subtracted before fitting, 2=linear fitting is applied despite non-linear situation, 3=uncertainty in not used in fitting, 4 and 5 decide which reference is used: both 4 and 5 not set uses the synthetic reference spectrum from the calibration file, 4 set and 5 not set uses the theoretical reference spectrum from the calibration file, 4 not set and 5 set uses the measured spectrum with the lowest viewing zenith angle in the sequence, both 4 and 5 set uses a reference spectrum from an external file, 6=level 2 data wavelength change not used in fitting'] == fit_config_idx]
    window_indexs =pd.unique(df['Column 14: Fitting window index, unique number for each fitting window'])
    print('Fitting window indexs found: ' + str(window_indexs))
    
    return df

#lev3_shelve_filename = 'E:\\Projects\\Zenith_NO2\\Pan_level3data_V2_plots\\lev3.out'
lev3_shelve_filename = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P103_plots\\lev3.out'
#QDOAS_shelve_filename = 'E:\\Projects\\Zenith_NO2\\QDOAS_outputs\\QDOAS_outputs.out'
QDOAS_shelve_filename = 'C:\\Projects\\Zenith_NO2\\QDOAS_outputs\\QDOAS_outputs.out'
#plotpath = 'E:\\Projects\\Zenith_NO2\\plots\\'
plotpath = 'C:\\Projects\\Zenith_NO2\\plots\\'

open_shelf(lev3_shelve_filename)
open_shelf(QDOAS_shelve_filename)

df_O3 = get_single_fitting_result(df_lev3,'SU',310.0,330.0,4,0,1,18) # window 5, default ozone
df_NO2 = get_single_fitting_result(df_lev3,'SO',400.0,440.0,4,0,1,18) # 
df_NO2_modified_1 = get_single_fitting_result(df_lev3,'SO',400.0,500.0,4,-1,-1,2) # window 2, modified no2, recommended by Vitali
df_NO2_modified_2 = get_single_fitting_result(df_lev3,'SO',400.0,500.0,4,-1,-1,17)
df_SO2 = get_single_fitting_result(df_lev3,'SU',306.0,330.0,4,0,1,2) # window 9, Fioletov et al. AMT, 2016

df_lev3 = df_NO2_modified_1 

df_QDOAS['UTC_simple'] = df_QDOAS['Date (DD/MM/YYYY)_Time (hh:mm:ss)']

df_QDOAS.set_index(['UTC_simple'],inplace = True)
df_QDOAS['UTC'] = df_QDOAS.index.tz_localize('UTC')
df_QDOAS.sort_values(by = 'UTC', inplace = True)
df_lev3.sort_values(by = 'UTC', inplace = True)
merged_data = pd.merge_asof(df_QDOAS, df_lev3, on='UTC',tolerance=pd.Timedelta('1hr'))

merged_data = merged_data.dropna(subset=['NO2_Vis.SlCol(no2)']).dropna(subset=['NO2_VCD']).dropna(subset=['Fluxes 450']).dropna(subset=['Fluxes 500'])
merged_data = merged_data[merged_data['NO2_Vis.SlCol(no2)']<0.5e37]
merged_data = merged_data[merged_data['Column 31: Uncertainty of nitrogen dioxide slant column amount [Dobson Units], negative value=not fitted or fitting not successfull']<5][merged_data['Column 31: Uncertainty of nitrogen dioxide slant column amount [Dobson Units], negative value=not fitted or fitting not successfull']>0]
merged_data = merged_data[merged_data['Column 21: Fitting result index: 1,2=no error, >2=error']<=2]
merged_data = merged_data[merged_data['Column 24: Normalized rms of weighted spectral fitting residuals, negative value=fitting not successfull'] <= 0.1]
merged_data = merged_data[merged_data['Column 64: Integration time [ms]']<=500]
merged_data = merged_data[merged_data['NO2_Vis.SlErr(no2)']<=1e17]
merged_data = merged_data[merged_data['NO2_VCD']<=5][merged_data['NO2_VCD']>=-1]

DU = 2.6870e+16
merged_data.y = merged_data['NO2_Vis.SlCol(no2)']/DU
merged_data.x = merged_data['NO2_VCD']
merged_data.ci = merged_data['Fluxes 450']/merged_data['Fluxes 500']


#%% fig 1
font = {'family' : 'DejaVu Sans', 'weight' : 'bold', 'size'   : 12}
plt.rc('font', **font)
fig = plt.figure(figsize=(10, 10), dpi=200, facecolor='w', edgecolor='k') 
cm = plt.cm.get_cmap('jet')
gs = gridspec.GridSpec(2, 2, height_ratios=[1,1], width_ratios=[1,1]) 

ax0 = plt.subplot(gs[0])
#sc = ax0.scatter(merged_data.x, merged_data.y, merged_data.ci, s=10, cmap=cm)
sc = ax0.scatter(merged_data.x, merged_data.y, c = merged_data.ci, s = 10, cmap=cm)
plt.colorbar(sc).set_label('CI')
ax0.grid()
ax0.set_ylabel('ZS dSCD [DU]')
ax0.set_xlabel('DS VCD [DU]')
ax0.legend()
ax0.set_title('ZS vs. DS NO2')

ax1 = plt.subplot(gs[1])
sc = ax1.scatter(merged_data.SZA, merged_data.y/merged_data.x, c = merged_data.ci, s= 10, cmap=cm)
plt.colorbar(sc).set_label('CI')
ax1.grid()
ax1.set_ylabel('ZS AMF')
ax1.set_xlabel('SZA')
ax1.legend()
ax1.set_title('ZS vs. DS NO2')

ax2 = plt.subplot(gs[2])
#sc = ax2.scatter(merged_data.time, merged_data.x, c = merged_data.ci, s= 10, cmap=cm)
#plt.colorbar(sc).set_label('CI')
ax2.plot(merged_data.time, merged_data.x,'k.', label = 'VCD')
ax2.grid()
ax2.set_ylabel('DS VCD [DU]')
ax2.set_xlabel('time')
ax2.legend()
ax2.set_title('ZS vs. DS NO2')

ax3 = plt.subplot(gs[3])
#sc = ax3.scatter(merged_data.time, merged_data.y, c = merged_data.ci, s= 10, cmap=cm)
#plt.colorbar(sc).set_label('CI')
ax3.plot(merged_data.time, merged_data.y,'k.', label = 'dSCD')
ax3.grid()
ax3.set_ylabel('ZS dSCD [DU]')
ax3.set_xlabel('time')
ax3.legend()
ax3.set_title('ZS vs. DS NO2')


plt.tight_layout()
plt.savefig(plotpath +'test.png')
#plt.show()
plt.close()

#%% fig 2
font = {'family' : 'DejaVu Sans', 'weight' : 'bold', 'size'   : 12}
plt.rc('font', **font)
fig = plt.figure(figsize=(20, 10), dpi=200, facecolor='w', edgecolor='k') 
cm = plt.cm.get_cmap('jet')
gs = gridspec.GridSpec(2, 1, height_ratios=[1,1], width_ratios=[1]) 

ax0 = plt.subplot(gs[0])
ax0.plot(merged_data.time, merged_data.x,'k.', label = 'VCD')
ax0.grid()
ax0.set_ylabel('DS VCD [DU]')
ax0.set_xlabel('time')
ax0.legend()
ax0.set_title('DS NO2')

ax1 = plt.subplot(gs[1])
ax1.plot(merged_data.time, merged_data['Column 24: Normalized rms of weighted spectral fitting residuals, negative value=fitting not successfull'],'k.', label = 'RMS')
ax1.grid()
ax1.set_ylabel('RMS')
ax1.set_xlabel('time')
ax1.legend()
ax1.set_title('DS NO2')


plt.tight_layout()
plt.savefig(plotpath +'NO2_DS_VCD_timeserise.png')
#plt.show()
plt.close()
