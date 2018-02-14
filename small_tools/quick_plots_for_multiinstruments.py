# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 14:19:40 2018

@author: ZhaoX
"""
import matplotlib
from matplotlib import pyplot as plt
import matplotlib.dates as dates
import numpy, pdb
from numpy import array
from numpy.polynomial.polynomial import polyval
from scipy.optimize import fmin
import pandas as pd

#%%
def daily_plots_LTC(new_df, gas_type, instrument_name, plot_path,VCD_column_nm):
    DU = 2.6870e16
    labelsize = 16
    print('\n \n>>>Plotting daily time serise: ')
    new_df.index = new_df['LTC'] # use LTC as time index
    
    new_df.index = new_df.index.tz_localize(None) # remove timezone information (localize)
    new_df['timestamp'] = new_df.index  # use this localize time as timestamp (for x-axis in plot)
    
    #from sites_list import sites_list # import site names, if measurements were made in different sites, we will loop over sites by sites
    sites_list = {'Downsview': 'America/Toronto', 'FortMcKay': 'America/Edmonton', 'StGeorge':'America/Toronto'}
    locations = pd.unique(new_df.location)
    instrument = pd.unique(new_df.instrument)

    days = pd.date_range(start = new_df.timestamp.min(), end = new_df.timestamp.max(),freq = 'D', normalize = True)
    delta_time = pd.Timedelta(hours = 24)
    delta_time_xlim1 = pd.Timedelta(hours = 3) # only plot sunlight period, from 6 a.m. to 18 a.m. (local time)
    delta_time_xlim2 = pd.Timedelta(hours = 21)
    
    
    for day in days:
        fig = plt.figure(num=None, figsize=(10, 10), dpi=600, facecolor='w', edgecolor='k')
        ind_start = day
        ind_end = day + delta_time


        x_time = new_df.timestamp
        
        y2 = new_df[VCD_column_nm]*DU


        #ax = fig.add_subplot(1,1,1) 
        #ax.plot(x_time, y2  ,'.', markersize=12)
        
        groups = new_df.groupby('location')
        ax = fig.add_subplot(1,1,1) 
        for key, group in groups:
            x_group = group.timestamp
            y_group = group[VCD_column_nm]*DU

            ax.plot(x_group, y_group ,'.', markersize=12,  label = str(group.location[0]))
  
            
    
        xlim_left = pd.Timestamp.to_pydatetime(day + delta_time_xlim1)
        xlim_right = pd.Timestamp.to_pydatetime(day + delta_time_xlim2)
        #fig.xlim(xlim_left, xlim_right)
        ax.set_xlim(xlim_left, xlim_right)

        ax.legend(fontsize = labelsize)
        #ax = fig.add_subplot(1,1,1)     
        
        ax.xaxis.set_major_locator(dates.HourLocator(interval=2))
        ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
        
        if gas_type == 'O3':
            #ax.set_ylim(200,500)
            ax.text(day + pd.Timedelta(hours = 7),490, 'Srart time: ' + str(x_time[0]))
            ax.text(day + pd.Timedelta(hours = 7),480, 'End time: ' + str(x_time[-1]))
            #ax.text(day + pd.Timedelta(hours = 7),470, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
            ax.text(day + pd.Timedelta(hours = 7),460, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
        elif gas_type == 'NO2':
            #ax.set_ylim(0,2e16)
            ax.set_ylim(0.5e16,2e16)
            ax.text(day + pd.Timedelta(hours = 7),1.9e16, 'Srart time: ' + str(x_time[0]),  fontsize= labelsize)
            ax.text(day + pd.Timedelta(hours = 7),1.8e16, 'End time: ' + str(x_time[-1]),  fontsize= labelsize)
            #ax.text(day + pd.Timedelta(hours = 7),2.3, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
            ax.text(day + pd.Timedelta(hours = 7),1.7e16, 'Daily mean = ' + str(format(y2.mean(),'.2e'))+ ' molec/cm^2', fontsize= labelsize)
        elif gas_type == 'SO2':
            #ax.set_ylim(-3,4)
            ax.text(day + pd.Timedelta(hours = 7),3.7, 'Srart time: ' + str(x_time[0]))
            ax.text(day + pd.Timedelta(hours = 7),3.5, 'End time: ' + str(x_time[-1]))
            #ax.text(day + pd.Timedelta(hours = 7),3.3, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
            plt.text(day + pd.Timedelta(hours = 7),3.1, 'BlickP mean = ' + str(format(y2.mean(),'.2e'))+ ' molec/cm^2')
        elif gas_type == 'HCHO':
            #ax.set_ylim(-3,4)
            ax.text(day + pd.Timedelta(hours = 7),3.7, 'Srart time: ' + str(x_time[0]))
            ax.text(day + pd.Timedelta(hours = 7),3.5, 'End time: ' + str(x_time[-1]))
            #ax.text(day + pd.Timedelta(hours = 7),3.3, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
            ax.text(day + pd.Timedelta(hours = 7),3.1, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
        ax.set_xlabel('LTC', fontsize= labelsize)
        ax.set_ylabel(gas_type + ' VCD [molec/cm^2]', fontsize= labelsize)
        measurement_location = new_df.location
        ax.set_title(instrument_name + '@' + 'Toronto',fontsize = labelsize)
        #ax.set_title(instrument_name + '@' + 'FortMcKay',fontsize = labelsize)
        ax.grid()
        fig.tight_layout()
        if len(str(day.month)) == 1:
            monthlabel = '0' + str(day.month)
        else:
            monthlabel = str(day.month)
        if len(str(day.day)) == 1:
            daylabel = '0' + str(day.day)
        else:
            daylabel = str(day.day)
        timelabel = str(day.year) + monthlabel + daylabel
        
        plt.xticks(fontsize = labelsize)
        plt.yticks(fontsize = labelsize)
        #fig.savefig(plot_path + instrument[0] + '_' + str(location) + '_BlickP_' + gas_type + '_VCD_'+ timelabel +'.png',dpi=600, facecolor='w' )
        plt.savefig(plot_path + instrument[0] + '_' + 'Toronto' + '_BlickP_' + gas_type + '_VCD_'+ timelabel +'.png',dpi=600, facecolor='w' )
        #plt.show()

        #plt.clf()
        
        plt.close(fig)
        
#%%  
df108.index = df108.LTC
df109.index = df109.LTC
#df122.index = df122.LTC
df108 = df108['2017-11-28']
df109 = df109['2017-11-28']
#df122 = df122['2017-11-28']

df = pd.concat([df108,df109])
#df = df122
df.sort_values(by=['LTC'])
df = df[df['Column 11: L2 data quality flag for nitrogen dioxide: 0=high quality, 1=medium quality, 2=low quality']<1]
gas_type = 'NO2'
instrument_name = 'Pandora108&109'
#instrument_name = 'Pandora122'
plot_path = 'C:\\Users\\ZhaoX\\Pandora_onGit\\small_tools\\'
VCD_column_nm = 'Column 8: Nitrogen dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful'
daily_plots_LTC(df, gas_type, instrument_name, plot_path,VCD_column_nm)