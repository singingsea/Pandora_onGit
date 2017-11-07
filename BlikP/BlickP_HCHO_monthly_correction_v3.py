# -*- coding: utf-8 -*-
"""
Created on Thu Oct 12 14:45:05 2017

@author: ZhaoX

This code is to perform the SO2 VCD calibration/correction method as in Fioletov et al., AMT 2016 paper

Following Fioletov, 0.25 quantile regresstion is selected for correction
BlickP data has been filtered same as Fioletov et al.

The quantile regression part is modified based on:
http://rpy.sourceforge.net/rpy2/doc-2.3/html/robjects_formulae.html
AUTHOR
Dr. Phillip M. Feldman
"""

from IPython import get_ipython ## house keeping, first two lines to clear workspace
get_ipython().magic('reset -sf') 

from BlickP_SO2_monthly_correction_v3 import calibration_function, daily_plots_LTC, L2_data_column_nm_search
from matplotlib import pyplot as plt
import matplotlib.dates as dates
import numpy, pdb 
from numpy import array
from numpy.polynomial.polynomial import polyval
from scipy.optimize import fmin
import pandas as pd

def main():  
    global gas_type, instrument_name, new_df, calibration_factors, plot_path, df_Blick, useful_column_strs

    #%% ************* 1. import BlickP L2 data *********************
    import shelve
    my_shelf = shelve.open(Blick_shelve_filename)
    print('\n \n>>>Loading BlickP dataframe from: ' + Blick_shelve_filename )
    
    L2data_key = instrument_name + 's1_' + Short_location_name + '_L2Tot_rfus0p1' # eg. saved L2data name: Pandora108s1_Downsview_L2Tot_rsut2p1
    for key in my_shelf:
        if key == L2data_key:
            globals()['df_Blick']=my_shelf[key]
    my_shelf.close()
    
    #%% ************* 2. serch for corresponding column names in L2 data *********************
    
    [AMF_column_nm, VCD_column_nm, VCD_err_column_nm, L2_fit_quality_column_nm, integration_time_column_nm] = L2_data_column_nm_search(useful_column_strs,df_Blick)
    
        
    #%% ************* 3. filtering the data *********************
    initial_size = len(df_Blick)

    df_Blick = df_Blick[df_Blick[L2_fit_quality_column_nm] <= 0]
    df_Blick = df_Blick[df_Blick[integration_time_column_nm] <= 500]
    df_Blick = df_Blick[df_Blick[AMF_column_nm] <= 5]
    df_Blick = df_Blick[df_Blick[VCD_err_column_nm] < 0.35]
    
    df_Blick_2mu = df_Blick[df_Blick[AMF_column_nm] <= 2]
    df_Blick_3mu = df_Blick[df_Blick[AMF_column_nm] > 2][df_Blick[AMF_column_nm] <= 3]
    df_Blick_5mu = df_Blick[df_Blick[AMF_column_nm] > 3][df_Blick[AMF_column_nm] <= 5]
    df_Blick_2mu = df_Blick_2mu[df_Blick_2mu[integration_time_column_nm] <= 100]
    df_Blick_3mu = df_Blick_3mu[df_Blick_3mu[integration_time_column_nm] <= 300]    
    df_Blick = pd.concat([df_Blick_2mu,df_Blick_3mu,df_Blick_5mu], ignore_index = True)
    df_Blick = df_Blick.sort_values('LTC')
    df_Blick.index = df_Blick.LTC
    
    #df_Blick = df_Blick['2016-04-04':'2016-04-20'] # dummy filter, only for testing
    #df_Blick = df_Blick['2017-02-02':'2017-02-4'] # dummy filter, only for testing
    
    final_size = len(df_Blick)
    p_filtered = (initial_size - final_size)/initial_size*100
    print('\n \n>>>' + str(p_filtered) + ' % data have been filtered! \n')
    if p_filtered == 100:
        print('\n \n>>>Warning: No data left! Pls check filters ... \n')
        
    #%% ************* 4. loop over monthes or 30days, plot dSCD vs AMF quaintile plots ********************* 
    
    [new_df, calibration_factors] = calibration_function(calibration_method,df_Blick,gas_type,VCD_column_nm,AMF_column_nm, plot_path)         
   
    #%% ************* 5. plot daily timeserise *********************  

    if len(new_df) > 0:
        daily_plots_LTC(new_df, gas_type, instrument_name, plot_path)
    else:
        print('\n \n>>>Warning : no measurements left after apply calibration, no daily plots will be made.\n' )
       
    #%% ************* 6. save new dataframe, include calibrated SO2 VCDs*********************
    shelve_filename = plot_path + 'BlickP_monthly_calibrated_' + gas_type + '_' + instrument_name +'.out'   
    
    # save data to shelve
    my_shelf = shelve.open(shelve_filename,'n') # 'n' for new

    #for key in dir():
    for key in globals():
        #print(key)
        if key.find('new_df') != -1 or key.find('calibration_factors') != -1:
            try:
                my_shelf[key] = globals()[key]
                print('\n \n>>>"' + key + '" : data successfully saved! ')
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
    

#%%    
if __name__ == '__main__':
    import sys
    sys.path.insert(0, 'C://Users//ZhaoX//Pandora_onGit//local_inputs')
    from BlickP_HCHO_correction_inputs import *
    main()



