# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 15:09:26 2017

@author: ZhaoX
"""
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.dates as dates
import dateutil.parser
import numpy as np


#%%
def linear_fit(x,y):
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.stats import linregress
    #location = 'FortMcKay'
    global gas_type , instrument_name
    
    font = {'family' : 'normal', 'weight' : 'bold', 'size'   : 12}
    plt.rc('font', **font)
    #plt.figure(num=None, figsize=(10, 10), dpi=200, facecolor='w', edgecolor='k')
    
    
    #plt.scatter(x,y)
    fit = np.polyfit(x,y,1)
    fit_fn = np.poly1d(fit) 
    # fit_fn is now a function which takes in x and returns an estimate for y
    #plt.plot(x,y, 'k.', x, fit_fn(x), '--r')
    plt.plot( [-600, 600], [-600, 600], 'k-')
    plt.plot( x, fit_fn(x), 'r-')
    details = linregress(x,y)

    if gas_type == 'O3':
        plt.xlim([150,550])
        plt.ylim([150,550])
        plt.text(200,450,'y = ' + str(format(details.slope,'.5f')) + 'x + ' + str(format(details.intercept,'.5f')) )
        plt.text(200,400,'R = ' + str(format(details.rvalue,'.5f')))
        plt.text(200,350,'N = ' + str(len(x)))       
    elif gas_type == 'NO2': 
#        plt.xlim([-1,3])
#        plt.ylim([-1,3])
#        plt.text(0,2.5,'y = ' + str(format(details.slope,'.5f')) + 'x + ' + str(format(details.intercept,'.5f')) )
#        plt.text(0,2.3,'R = ' + str(format(details.rvalue,'.5f')))
#        plt.text(0,2.1,'N = ' + str(len(x)))   
        plt.xlim([-3,4])
        plt.ylim([-3,4])
        plt.text(-2,3.5,'y = ' + str(format(details.slope,'.5f')) + 'x + ' + str(format(details.intercept,'.5f')) )
        plt.text(-2,3.3,'R = ' + str(format(details.rvalue,'.5f')))
        plt.text(-2,3.1,'N = ' + str(len(x))) 
    elif gas_type == 'SO2':     
        plt.xlim([-3,4])
        plt.ylim([-3,4])
        plt.text(-2,3.5,'y = ' + str(format(details.slope,'.5f')) + 'x + ' + str(format(details.intercept,'.5f')) )
        plt.text(-2,3.3,'R = ' + str(format(details.rvalue,'.5f')))
        plt.text(-2,3.1,'N = ' + str(len(x)))   

    plt.xlabel('BlickP ' + gas_type + ' [DU]')
    plt.ylabel('PanPS ' + gas_type + ' [DU]')
    plt.title(instrument_name)
    plt.grid()
    plt.legend(loc='lower right')
    plt.savefig( 'Blick_vs_PanPS_lev3_'  + gas_type +  '_scatter.png')        
    plt.show()
    print(details)
    return details

#%%
def daily_plots(new_df):
    global gas_type, instrument_name

    new_df['timestamp'] = new_df.time
    new_df = new_df.set_index('time')
    
    days = pd.date_range(start = '2016-01-01 00:00:00', end = '2016-12-31 00:00:00')
    delta_time = pd.Timedelta(hours = 24)
    delta_time_xlim1 = pd.Timedelta(hours = 11)
    delta_time_xlim2 = pd.Timedelta(hours = 25)
    
    fig = plt.figure(num=None, figsize=(10, 10), dpi=200, facecolor='w', edgecolor='k')
    for day in days:
        ind_start = day
        ind_end = day + delta_time
    
        if len(new_df.timestamp[ind_start:ind_end]) == 0:
            print('no measurements in day' + str(day))
        else:
            x_time = new_df.timestamp[ind_start:ind_end]
            
            if gas_type == 'O3':
                y1 = new_df.O3_VCD[ind_start:ind_end]
                y2 = new_df['Column 8: Ozone total vertical column amount [Dobson Units], -9e99=retrieval not successful'][ind_start:ind_end]
            elif gas_type == 'NO2':
                y1 = new_df.NO2_VCD[ind_start:ind_end]
                y2 = new_df['Column 8: Nitrogen dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful'][ind_start:ind_end]
            elif gas_type == 'SO2':
                y1 = new_df.SO2_VCD[ind_start:ind_end]
                y2 = new_df['Column 14: Sulfur dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful'][ind_start:ind_end]
                
            plt.plot(x_time, y1 ,'.k',label = 'PanPS lev3')
            plt.plot(x_time, y2 ,'rx', label = 'BlickP')
    
            plt.xlim(day + delta_time_xlim1, day + delta_time_xlim2)
            plt.legend()
            ax = fig.add_subplot(1,1,1)        
            ax.xaxis.set_major_locator(dates.HourLocator(interval=2))
            ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
            
            if gas_type == 'O3':
                plt.ylim(200,500)
                plt.text(day + pd.Timedelta(hours = 12),490, 'Srart time: ' + str(x_time[0]))
                plt.text(day + pd.Timedelta(hours = 12),480, 'End time: ' + str(x_time[-1]))
                plt.text(day + pd.Timedelta(hours = 12),470, 'PanPS mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
                plt.text(day + pd.Timedelta(hours = 12),460, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
            elif gas_type == 'NO2':
                plt.ylim(-1,3)
                plt.text(day + pd.Timedelta(hours = 12),2.7, 'Srart time: ' + str(x_time[0]))
                plt.text(day + pd.Timedelta(hours = 12),2.5, 'End time: ' + str(x_time[-1]))
                plt.text(day + pd.Timedelta(hours = 12),2.3, 'PanPS mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
                plt.text(day + pd.Timedelta(hours = 12),2.1, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
            elif gas_type == 'SO2':
                plt.ylim(-3,4)
                plt.text(day + pd.Timedelta(hours = 12),3.7, 'Srart time: ' + str(x_time[0]))
                plt.text(day + pd.Timedelta(hours = 12),3.5, 'End time: ' + str(x_time[-1]))
                plt.text(day + pd.Timedelta(hours = 12),3.3, 'PanPS mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
                plt.text(day + pd.Timedelta(hours = 12),3.1, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
                
            plt.xlabel('UTC')
            plt.ylabel(gas_type + ' VCD [DU]')
            measurement_location = new_df.location_x[ind_start:ind_end]
            plt.title(instrument_name + '@' + measurement_location[0])
            plt.grid()
            plt.tight_layout()
            plt.savefig('Blick_vs_PanPS_lev3_' + gas_type + '_timeserise'+ str(day.year) +str(day.month)+ str(day.day)+'.png')
            plt.clf()
            #plt.show()
    plt.close()

#%%
#%% ****************** 1. load preprocessed data from shelves ******************
import shelve
#Blick_shelve_filename = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\108\\Blick\\L2_test\\Blick_L2.out' # this folder has Pandora108 SO2,HCHO fitting results
#Blick_shelve_filename = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\108\\Blick\\L2\\Blick_L2.out' # this folder has Pandora108 Ozone,NO2 fitting results
Blick_shelve_filename = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\109\\Blick\\L2\\Blick_L2.out' # this folder has Pandora109 Ozone,NO2,SO2,HCHO fitting results
my_shelf = shelve.open(Blick_shelve_filename)
print('Loading BlickP dataframe from: ' + Blick_shelve_filename )
for key in my_shelf:
    globals()[key]=my_shelf[key]
my_shelf.close()

#PanPS_shelve_filename = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\108\\L3_plots\\lev3.out' # this folder has Pandora108 PanPS processed level 3 data
PanPS_shelve_filename = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\109\\L3_plots\\lev3.out'  #this folder has Pandora109 PanPS processed level 3 data
my_shelf = shelve.open(PanPS_shelve_filename)
print('Loading PanPS dataframe from: ' + PanPS_shelve_filename )
for key in my_shelf:
    globals()[key]=my_shelf[key]
my_shelf.close()


#%% ****************** 2. manual inputs information ******************
#instrument_name = 'Pandora 108'
instrument_name = 'Pandora 109'
#gas_type = 'O3'
gas_type = 'NO2'
#gas_type = 'SO2'

#%% ****************** 3. merge BlickP and PanPS dataframe ******************
print('Start merging for ' + gas_type + ' measurements:')
# prepare Blick dataframe: here we concat ozone measurements from two sites
if gas_type == 'O3':
    #df_Blick = pd.concat([Pandora108s1_Downsview_L2Tot_rout0p1,Pandora108s1_FortMcKay_L2Tot_rout0p1], ignore_index = True)
    df_Blick = pd.concat([Pandora109s1_Downsview_L2Tot_rout0p1,Pandora109s1_StGeorge_L2Tot_rout0p1], ignore_index = True)
elif gas_type == 'NO2':
    #df_Blick = pd.concat([Pandora108s1_Downsview_L2Tot_rnvs0p1,Pandora108s1_FortMcKay_L2Tot_rnvs0p1], ignore_index = True)    
    df_Blick = pd.concat([Pandora109s1_Downsview_L2Tot_rnvs0p1,Pandora109s1_StGeorge_L2Tot_rnvs0p1], ignore_index = True)
elif gas_type == 'SO2':
    #df_Blick = pd.concat([Pandora108s1_Downsview_L2Tot_rsut1p1,Pandora108s1_FortMcKay_L2Tot_rsut1p1], ignore_index = True)
    #df_Blick = pd.concat([Pandora108s1_Downsview_L2Tot_rsut2p1,Pandora108s1_FortMcKay_L2Tot_rsut2p1], ignore_index = True)
    df_Blick = pd.concat([Pandora109s1_Downsview_L2Tot_rsut2p1,Pandora109s1_StGeorge_L2Tot_rsut2p1], ignore_index = True)
# prepare PanPs dataframe:
df_PanPS = df_lev3

# sort data by time, here time is timestamps, phrased from the ISO timestamp in original data file
df_Blick = df_Blick.sort_values('time')
df_PanPS = df_PanPS.sort_values('time')

# note: the PanPS use time at the start of the measurements, while BlickP gives time at the middle of the measurements ... 
# for more details, see headers of PanPS lev3 data file and BlickP L2 file
time_offset = pd.Timedelta(seconds = 30)
df_PanPS.time += time_offset

# merge data by their timestamp, need give tolerance for time differece between two datasets
print('Merging PanPS and BlickP dataframe ...')
new_df = pd.merge_asof(df_PanPS, df_Blick, on='time', tolerance=pd.Timedelta('30s'))

# filter merged data (note PanPS lev3 data has all types of trace gass fitted!)
print('Filtering the merged dataframe ...')

if gas_type == 'O3':
    # the following filters are for PanPS data
    new_df = new_df[new_df['Column 14: Fitting window index, unique number for each fitting window'] == 5]
    new_df = new_df[new_df['Column 29: Geometrical ozone air mass factor'] <= 3]
    # the following filter is for BlickP data
    new_df = new_df[new_df['Column 27: Level 2 Fit data quality flag: 0=high quality, 1=medium quality, 2=low quality'] <= 0 ]
elif gas_type == 'NO2':
    # the following filters are for PanPS data
    new_df = new_df[new_df['Column 14: Fitting window index, unique number for each fitting window'] == 2]
    new_df = new_df[new_df['Column 32: Geometrical nitrogen dioxide air mass factor'] <= 3]
    # the following filter is for BlickP data
    new_df = new_df[new_df['Column 21: Level 2 Fit data quality flag: 0=high quality, 1=medium quality, 2=low quality'] <= 0 ]
elif gas_type == 'SO2':
    # the following filters are for PanPS data
    new_df = new_df[new_df['Column 14: Fitting window index, unique number for each fitting window'] == 9]
    new_df = new_df[new_df['Column 35: Geometrical sulfur dioxide air mass factor'] <= 3]
    # the following filter is for BlickP data
    new_df = new_df[new_df['Column 27: Level 2 Fit data quality flag: 0=high quality, 1=medium quality, 2=low quality'] <= 0 ]

if gas_type == 'O3':
    Pan_VCD = new_df.O3_VCD
    Blick_VCD = new_df['Column 8: Ozone total vertical column amount [Dobson Units], -9e99=retrieval not successful']
    
elif gas_type == 'NO2':    
    Pan_VCD = new_df.NO2_VCD
    Blick_VCD = new_df['Column 8: Nitrogen dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful']
       
elif gas_type == 'SO2':
    Pan_VCD = new_df.SO2_VCD
    Blick_VCD = new_df['Column 14: Sulfur dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful']

# filter NaN VCD cells in the merged data
ind_isnull = pd.isnull(Pan_VCD )
ind_notnull = [not bool for bool in ind_isnull]
new_df = new_df[ind_notnull]

ind_isnull = pd.isnull(Blick_VCD)
ind_notnull = [not bool for bool in ind_isnull]
new_df = new_df[ind_notnull]

#%% ************* 4. make grouped scatter plots *********************
# plot correlation plot between PanPS and BlickP processed VCD data
x = np.array(Pan_VCD)
y = np.array(Blick_VCD)
# group dataframe by measurement locations
try:
    groups = new_df.groupby('location')
except: 
    groups = new_df.groupby('location_x')
    
plt.figure(num=None, figsize=(10, 10), dpi=200, facecolor='w', edgecolor='k')
for name, group in groups:
    if gas_type == 'O3':
        plt.scatter(group.O3_VCD,group['Column 8: Ozone total vertical column amount [Dobson Units], -9e99=retrieval not successful'], label = name)
    elif gas_type == 'NO2':  
        plt.scatter(group.NO2_VCD,group['Column 8: Nitrogen dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful'], label = name)
    elif gas_type == 'SO2':    
        plt.scatter(group.SO2_VCD,group['Column 14: Sulfur dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful'], label = name)
plt.legend()
linear_fit(x,y)

#%% ************* 5. make daily timeserise plots *********************
daily_plots(new_df)

#%% ************* 6. save merged dataframe *********************
shelve_filename = 'PanPS_BlickP_merged' + gas_type + '_' + instrument_name +'.out'   

# save data to shelve
import shelve
my_shelf = shelve.open(shelve_filename,'n') # 'n' for new
print(dir())
for key in dir():
    print(key)
    if key.find('new_df') != -1:
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
my_shelf = shelve.open(shelve_filename)
for key in my_shelf:
    globals()[key]=my_shelf[key]
my_shelf.close()

