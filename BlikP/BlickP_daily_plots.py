# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 16:06:26 2017

@author: ZhaoX
"""

#from IPython import get_ipython ## house keeping, first two lines to clear workspace
#get_ipython().magic('reset -sf') 

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
    
    print('\n \n>>>Plotting daily time serise: ')
    new_df.index = new_df['LTC'] # use LTC as time index
    
    new_df.index = new_df.index.tz_localize(None) # remove timezone information (localize)
    new_df['timestamp'] = new_df.index  # use this localize time as timestamp (for x-axis in plot)
    
    from sites_list import sites_list # import site names, if measurements were made in different sites, we will loop over sites by sites
    locations = pd.unique(new_df.location)
    instrument = pd.unique(new_df.instrument)
    for location in locations:
        days = pd.date_range(start = new_df.timestamp.min(), end = new_df.timestamp.max(),freq = 'D', normalize = True)
        delta_time = pd.Timedelta(hours = 24)
        delta_time_xlim1 = pd.Timedelta(hours = 3) # only plot sunlight period, from 6 a.m. to 18 a.m. (local time)
        delta_time_xlim2 = pd.Timedelta(hours = 21)
        
        
        for day in days:
            fig = plt.figure(num=None, figsize=(10, 10), dpi=200, facecolor='w', edgecolor='k')
            ind_start = day
            ind_end = day + delta_time
    
            if len(new_df.timestamp[ind_start:ind_end]) == 0:
                print('no measurements (after filtration) found in day: ' + str(day))
            else:
                x_time = new_df.timestamp[ind_start:ind_end]
                
                y2 = new_df[VCD_column_nm][ind_start:ind_end]

                #plt.plot(x_time, y2 ,'rx', label = 'BlickP original VCD')
                
                groups = new_df[ind_start:ind_end].groupby('VCD_err_rounded')
                ax = fig.add_subplot(1,1,1) 
                #ax.plot(x_time, y2 ,'.')
 
                for key, group in groups:

                    #x_group = group.timestamp[ind_start:ind_end]
                    x_group = group.timestamp[ind_start:ind_end]
                    y_group = group[VCD_column_nm][ind_start:ind_end]
                
                    #plt.plot(x_group, y_group ,'s', label = str(group.VCD_err_rounded[0]))
                    ax.plot(x_group, y_group ,'.', markersize=12,  label = str(group.VCD_err_rounded[0]))
                    
            
                xlim_left = pd.Timestamp.to_pydatetime(day + delta_time_xlim1)
                xlim_right = pd.Timestamp.to_pydatetime(day + delta_time_xlim2)
                #fig.xlim(xlim_left, xlim_right)
                ax.set_xlim(xlim_left, xlim_right)

                ax.legend()
                #ax = fig.add_subplot(1,1,1)     
                
                ax.xaxis.set_major_locator(dates.HourLocator(interval=2))
                ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
                
                if gas_type == 'O3':
                    ax.set_ylim(200,500)
                    ax.text(day + pd.Timedelta(hours = 7),490, 'Srart time: ' + str(x_time[0]))
                    ax.text(day + pd.Timedelta(hours = 7),480, 'End time: ' + str(x_time[-1]))
                    #ax.text(day + pd.Timedelta(hours = 7),470, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
                    ax.text(day + pd.Timedelta(hours = 7),460, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
                elif gas_type == 'NO2':
                    ax.set_ylim(-1,3)
                    ax.text(day + pd.Timedelta(hours = 7),2.7, 'Srart time: ' + str(x_time[0]))
                    ax.text(day + pd.Timedelta(hours = 7),2.5, 'End time: ' + str(x_time[-1]))
                    #ax.text(day + pd.Timedelta(hours = 7),2.3, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
                    ax.text(day + pd.Timedelta(hours = 7),2.1, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
                elif gas_type == 'SO2':
                    ax.set_ylim(-3,4)
                    ax.text(day + pd.Timedelta(hours = 7),3.7, 'Srart time: ' + str(x_time[0]))
                    ax.text(day + pd.Timedelta(hours = 7),3.5, 'End time: ' + str(x_time[-1]))
                    #ax.text(day + pd.Timedelta(hours = 7),3.3, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
                    plt.text(day + pd.Timedelta(hours = 7),3.1, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
                elif gas_type == 'HCHO':
                    ax.set_ylim(-3,4)
                    ax.text(day + pd.Timedelta(hours = 7),3.7, 'Srart time: ' + str(x_time[0]))
                    ax.text(day + pd.Timedelta(hours = 7),3.5, 'End time: ' + str(x_time[-1]))
                    #ax.text(day + pd.Timedelta(hours = 7),3.3, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
                    ax.text(day + pd.Timedelta(hours = 7),3.1, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
                ax.set_xlabel('LTC')
                ax.set_ylabel(gas_type + ' VCD [DU]')
                measurement_location = new_df.location[ind_start:ind_end]
                ax.set_title(instrument_name + '@' + measurement_location[0] + '\nColour coded by rounded uncertainty of VCD in [DU]')
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
                
                fig.savefig(plot_path + instrument[0] + '_' + str(location) + '_BlickP_' + gas_type + '_VCD_'+ timelabel +'.png',dpi=600, facecolor='w' )
                #plt.show()

                #plt.clf()
                
            plt.close(fig)
        


#%%
def L2_data_column_nm_search(useful_column_strs,df_Blick):
    
    No_of_column_find = pd.DataFrame()
    No_of_column_find['No_of_AMF_find'] = [0]
    No_of_column_find['No_of_VCD_find'] = [0] 
    No_of_column_find['No_of_VCD_err_find'] = [0] 
    No_of_column_find['No_of_L2_fit_quality_find'] = [0]
    No_of_column_find['No_of_integration_time_find'] = [0] 
    
    for key in df_Blick.keys():         
        if key.find(useful_column_strs['AMF_str']) > 0:
            AMF_column_nm = key
            No_of_column_find['No_of_AMF_find'] += 1
        elif key.find(useful_column_strs['VCD_str']) > 0:
            VCD_column_nm = key
            No_of_column_find['No_of_VCD_find'] += 1
        elif key.find(useful_column_strs['VCD_err_str']) > 0:
            VCD_err_column_nm = key
            No_of_column_find['No_of_VCD_err_find'] += 1
        elif key.find(useful_column_strs['L2_fit_quality']) > 0:
            L2_fit_quality_column_nm = key
            No_of_column_find['No_of_L2_fit_quality_find'] += 1
        elif key.find(useful_column_strs['integration_time_str']) > 0:
            integration_time_column_nm = key
            No_of_column_find['No_of_integration_time_find'] += 1 
   
    mean_column_find = No_of_column_find.iloc[0,:].mean()            
    if  mean_column_find == 1:
        print('\n \n>>>Corresponding column names have been found from L2 files')
    elif mean_column_find < 1:
        print('\n \n>>>Wanring: One necessary column in L2 file is not identified. Pls check key words for corresponding columns')
    elif mean_column_find > 1:
        print('\n \n>>>Wanring: Key words for corresponding column is not unique! This may cause wrong interpretation of data! Pls check key words for corresponding columns')
   
    return AMF_column_nm, VCD_column_nm, VCD_err_column_nm, L2_fit_quality_column_nm, integration_time_column_nm
#%%    
def main(input_df):
    global gas_type, instrument_name, new_df, calibration_factors, plot_path, df_Blick, useful_column_strs
    
    instrument_name = input_df.instrument_name    
    Short_location_name = input_df.Short_location_name
    gas_type = input_df.gas_type
    Blick_shelve_filename = input_df.Blick_shelve_filename
    plot_path = input_df.plot_path
    useful_column_strs = input_df.useful_column_strs
    sites_list = input_df.sites_list
    trace_gases = input_df.trace_gases
    #%% ************* 1. import BlickP L2 data *********************
    import shelve
    my_shelf = shelve.open(Blick_shelve_filename)
    print('\n \n>>>Loading BlickP dataframe from: ' + Blick_shelve_filename )
    
    L2data_key = instrument_name + 's1_' + Short_location_name + '_L2Tot_' + trace_gases[gas_type] +'p1' # eg. saved L2data name: Pandora108s1_Downsview_L2Tot_rsut2p1
    for key in my_shelf:
        if key == L2data_key:
            globals()['df_Blick']=my_shelf[key]
    my_shelf.close()
    
    #%% ************* 2. serch for corresponding column names in L2 data *********************
    
    [AMF_column_nm, VCD_column_nm, VCD_err_column_nm, L2_fit_quality_column_nm, integration_time_column_nm] = L2_data_column_nm_search(useful_column_strs,df_Blick)
    
    #%% ************* 3. filtering the data *********************
    initial_size = len(df_Blick)

    df_Blick = df_Blick[df_Blick[L2_fit_quality_column_nm] <= 1]
#    df_Blick = df_Blick[df_Blick[integration_time_column_nm] <= 500]
#    df_Blick = df_Blick[df_Blick[AMF_column_nm] <= 5]
#    
#    
#    df_Blick_2mu = df_Blick[df_Blick[AMF_column_nm] <= 2]
#    df_Blick_3mu = df_Blick[df_Blick[AMF_column_nm] > 2][df_Blick[AMF_column_nm] <= 3]
#    df_Blick_5mu = df_Blick[df_Blick[AMF_column_nm] > 3][df_Blick[AMF_column_nm] <= 5]
#    df_Blick_2mu = df_Blick_2mu[df_Blick_2mu[integration_time_column_nm] <= 100]
#    df_Blick_3mu = df_Blick_3mu[df_Blick_3mu[integration_time_column_nm] <= 300]    
#    df_Blick = pd.concat([df_Blick_2mu,df_Blick_3mu,df_Blick_5mu], ignore_index = True)
    df_Blick = df_Blick.sort_values('LTC')
    df_Blick.index = df_Blick.LTC
    
    # filter data by start processing date, this only used for auto-weekly processing
    if input_df.weekly_processing == True:
        df_Blick = df_Blick[input_df.start_date:]
    
    #df_Blick = df_Blick['2016-04-04':'2016-04-20'] # dummy filter, only for testing
    #df_Blick = df_Blick['2017-02-02':'2017-02-4'] # dummy filter, only for testing
    
    final_size = len(df_Blick)
    p_filtered = (initial_size - final_size)/initial_size*100
    print('\n \n>>>' + str(p_filtered) + ' % data have been filtered! \n')
    if p_filtered == 100:
        print('\n \n>>>Warning: No data left! Pls check filters ... \n')
    #%% ************* 4. group data by uncertainty *********************     
    if gas_type == 'O3':
        df_Blick = df_Blick[df_Blick[VCD_err_column_nm] <= 4]
        df_Blick['VCD_err_rounded'] = df_Blick[VCD_err_column_nm].round()
    elif gas_type == 'NO2':
        df_Blick = df_Blick[df_Blick[VCD_err_column_nm] <= 2]
        df_Blick['VCD_err_rounded'] = df_Blick[VCD_err_column_nm].round()
    elif gas_type == 'SO2':
        df_Blick = df_Blick[df_Blick[VCD_err_column_nm] <= 0.35]
        df_Blick['VCD_err_rounded'] = df_Blick[VCD_err_column_nm].round(1)
    elif gas_type == 'HCHO':
        df_Blick = df_Blick[df_Blick[VCD_err_column_nm] <= 0.35]
        df_Blick['VCD_err_rounded'] = df_Blick[VCD_err_column_nm].round(1)
    #%% ************* 5. plot daily timeserise *********************  

    if len(df_Blick) > 0:
        daily_plots_LTC(df_Blick, gas_type, instrument_name, plot_path,VCD_column_nm)
    else:
        print('\n \n>>>Warning : no measurements left after apply filters, no daily plots will be made.\n' )
        
#    #%% ************* 6. save new dataframe, include calibrated SO2 VCDs*********************
#    if input_df.weekly_processing == False:# we will save filtered VCDs, only if this is not auto-weekly processing
#        shelve_filename = plot_path + 'BlickP_filtered_VCD_' + gas_type + '_' + instrument_name +'.out'   
#        
#        # save data to shelve
#        my_shelf = shelve.open(shelve_filename,'n') # 'n' for new
#    
#        #for key in dir():
#        for key in globals():
#            #print(key)
#            if key.find('df_Blick') != -1:
#                try:
#                    my_shelf[key] = globals()[key]
#                    print('\n \n>>>"' + key + '" : data successfully saved! ')
#                except TypeError:
#                    print('ERROR shelving: {0}'.format(key))
#            else:
#                #print('key not matched')
#                pass
#        my_shelf.close()
#        
#        # load data to shelve
#        my_shelf = shelve.open(shelve_filename)
#        for key in my_shelf:
#            globals()[key]=my_shelf[key]
#        my_shelf.close()
#    
#%%
if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'C://Users//ZhaoX//Pandora_onGit//local_inputs')
    sys.path.insert(0, '\\\\wdow05dtmibroh\\CDrive\\UTILS\\Blick\\Pandora_onGit\\local_inputs')
    from BlickP_daily_VCD_plot_inputs import *
    main(input_df)



