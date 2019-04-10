# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 11:16:39 2018

@author: ZhaoX
"""

from matplotlib import pyplot as plt
import matplotlib.dates as dates
import numpy, pdb
from numpy import array
from numpy.polynomial.polynomial import polyval
from scipy.optimize import fmin
import pandas as pd


#%%
def open_shelf(shelve_filename):
    import shelve
    my_shelf = shelve.open(shelve_filename)
    
    for key in my_shelf:
        globals()[key]=my_shelf[key]
    my_shelf.close()  
    
#%%
def get_single_fitting_result(df,routine, start_wv,end_wv,poly,offset,wv_change,fit_config_idx):
    df = df[df['Column 1: Two letter code of measurement routine'] == routine]
    df = df[df['Column 15: Starting wavelength of fitting window [nm]'] == start_wv][df['Column 16: Ending wavelength of fitting window [nm]'] == end_wv]
    df = df[df['Column 17: Order of smoothing polynomial used in spectral fitting'] == poly][df['Column 18: Order of offset polynomial used in spectral fitting, -1=no offset'] == offset][df['Column 19: Order of wavelength change polynomial used in spectral fitting, -1=no wavelength change'] == wv_change]
    df = df[df['Column 20: Sum over 2^i with i being a fitting configuration index, 0=Ring spectrum is fitted, 1=molecular scattering is subtracted before fitting, 2=linear fitting is applied despite non-linear situation, 3=uncertainty in not used in fitting, 4 and 5 decide which reference is used: both 4 and 5 not set uses the synthetic reference spectrum from the calibration file, 4 set and 5 not set uses the theoretical reference spectrum from the calibration file, 4 not set and 5 set uses the measured spectrum with the lowest viewing zenith angle in the sequence, both 4 and 5 set uses a reference spectrum from an external file, 6=level 2 data wavelength change not used in fitting'] == fit_config_idx]
    window_indexs =pd.unique(df['Column 14: Fitting window index, unique number for each fitting window'])
    print('Fitting window indexs found: ' + str(window_indexs))    
    
    return df
#%%
def quantile_regression(x, y, gas_type, column_type, plot_path):

    # inputs: x, y  --> array; year_month_str ==> only for making label; column_type --> used for label = 'dSCDs' or VCDs''
    N_coefficients = 2
    fractions = [0.01,0.05,0.1, 0.2, 0.25, 0.3, 0.5]
    symbol_size = 10
    
    #  Define tilted absolute value function.    
    def tilted_abs(rho, x):
       """
       OVERVIEW
    
       The tilted absolute value function is used in quantile regression.
    
    
       INPUTS
    
       rho: This parameter is a probability, and thus takes values between 0 and 1.
    
       x: This parameter represents a value of the independent variable, and in
       general takes any real value (float) or NumPy array of floats.
       """
    
       return x * (rho - (x < 0))
    
    # Estimate quantiles via direct optimization.
    
    def model(x, beta):
       """
       This example defines the model as a polynomial, where the coefficients of the
       polynomial are passed via `beta`.
       """
    
       return polyval(x, beta)
    
    
    def objective(beta, rho):
       """
       The objective function to be minimized is the sum of the tilted absolute
       values of the differences between the observations and the model.
       """
       return tilted_abs(rho, y - model(x, beta)).sum()
    
    
    # Define starting point for optimization:
    beta_0= numpy.zeros(N_coefficients)
    if N_coefficients >= 2:
       beta_0[1]= 1.0
    
    # `beta_hat[i]` will store the parameter estimates for the quantile
    # corresponding to `fractions[i]`:
    beta_hat= []
    
    for i, fraction in enumerate(fractions):
       beta_hat.append( fmin(objective, x0=beta_0, args=(fraction,), xtol=1e-8,
         disp=False, maxiter=3000) )
    
    
    # Plot the data with overlays of estimated quantiles.
    
    # Create figure window:
    fig= plt.figure(figsize=[15,15], dpi=120, facecolor=[1,1,1])
    
    # Plot (x,y) pairs on a scatter diagram.  The argument `s` specifies the symbol
    # area in units of points squared.
    p1= plt.scatter(x, y, s=symbol_size)

    if column_type == 'dSCDs':
        x_min = 0
        y_min = -10
        x_max = 5
        y_max = 30
    elif column_type == 'VCDs':
        x_min = 0
        y_min = -10
        x_max = 5
        y_max = 10
    else:
        x_min = min(x)
        y_min = min(y)
        x_max = max(x)
        y_max = max(y)
        
#    x_min = min(x)
#    y_min = min(y)
#    x_max = max(x)
#    y_max = max(y)      
#        
    plt.xlim([x_min, x_max])
    plt.ylim([y_min, y_max])
    plt.title("Quantile Regression with Quantiles Corresponding to\n"
      "the Fractions %s\n" % str(fractions)[1:-1], size=18)
    plt.xlabel("AMF", size=18)
    plt.ylabel(gas_type + ' '+ column_type +' [DU]', size=18)
    
    # Enable 'hold' so that lines will be plotted as overlays on scatter diagram
    # rather than in separate figure windows:
    #plt.hold(True)
    
    # Draw a line for each quantile:
    for i, fraction in enumerate(fractions):
       plt.plot(x, polyval(x, beta_hat[i]), linewidth=2,label = str(fraction))      
    
    x1_location = x_min + 0.02*abs(x_max - x_min)
    y1_location = y_max - 0.02*abs(y_max - y_min)
    x2_location = x1_location
    y2_location = y1_location - 0.05*abs(y_max - y_min)
    x3_location = x1_location
    y3_location = y2_location - 0.05*abs(y_max - y_min)
    N_points = len(x)
    plt.grid(True)
    plt.legend(loc = 'upper right')
    #plt.text(x1_location,y1_location,'Year-Month-Day: ' + year_month_str,  size=18)
    #plt.text(x2_location,y2_location, '25th % [intercept slop] = '+ str(beta_hat[4]), size=18)
    plt.text(x2_location,y2_location, '5th % [intercept slop] = '+ str(beta_hat[1]), size=18)
    plt.text(x3_location,y3_location, 'No. of measurements = '+ str(N_points), size=18)
    # Nothing is displayed until we invoke `show`:
    #plt.savefig(plot_path + 'Quantile_regression_'+ column_type + '_vs_AMF_' + year_month_str + '.png')
    plt.savefig(plot_path + 'Quantile_regression_'+ column_type + '_vs_AMF.png')
    #plt.show()
    plt.clf()
    plt.close()

    #return beta_hat[4]
    return beta_hat[1]
#%%
#%%
def daily_plots_LTC(new_df, gas_type, instrument_name, plot_path):
    print('\n \n>>>Plotting daily time serise: ')
    #new_df = new_df.set_index('LTC') # use LTC as time index
    new_df.index = new_df['LTC'] # use LTC as time index
    
    new_df.index = new_df.index.tz_localize(None) # remove timezone information (localize)
    new_df['timestamp'] = new_df.index  # use this localize time as timestamp (for x-axis in plot)
    
    from sites_list import sites_list # import site names, if measurements were made in different sites, we will loop over sites by sites
    locations = pd.unique(new_df.location)
    instrument = pd.unique(new_df.instrument)
    for location in locations:
        #timezone = sites_list[location]
        days = pd.date_range(start = new_df.timestamp.min(), end = new_df.timestamp.max(),freq = 'D', normalize = True)
        delta_time = pd.Timedelta(hours = 24)
        delta_time_xlim1 = pd.Timedelta(hours = 3) # only plot sunlight period, from 6 a.m. to 18 a.m. (local time)
        delta_time_xlim2 = pd.Timedelta(hours = 21)

        fig = plt.figure(num=None, figsize=(10, 10), dpi=200, facecolor='w', edgecolor='k')
        for day in days:
            ind_start = str(day)
            ind_end = str(day + delta_time)
    
            if len(new_df.timestamp[ind_start:ind_end]) == 0:
                print('no measurements (after filtration) found in day: ' + str(day))
            else:
                x_time = new_df.timestamp[ind_start:ind_end]
                
                if gas_type == 'O3':
                    y1 = new_df.VCD_corrected[ind_start:ind_end]
                    y2 = new_df['O3_VCD'][ind_start:ind_end]
                elif gas_type == 'NO2':
                    y1 = new_df.VCD_corrected[ind_start:ind_end]
                    y2 = new_df['NO2_VCD'][ind_start:ind_end]
                elif gas_type == 'SO2':
                    y1 = new_df.VCD_corrected[ind_start:ind_end]
                    y2 = new_df['SO2_VCD'][ind_start:ind_end]
         
                plt.plot(x_time, y1 ,'.k',label = 'Corrected VCD')
                plt.plot(x_time, y2 ,'rx', label = 'BlickP original VCD')

        
                plt.xlim(day + delta_time_xlim1, day + delta_time_xlim2)
                plt.legend()
                ax = fig.add_subplot(1,1,1)        
                ax.xaxis.set_major_locator(dates.HourLocator(interval=2))
                ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M'))
                
                if gas_type == 'O3':
                    plt.ylim(200,500)
                    plt.text(day + pd.Timedelta(hours = 7),490, 'Srart time: ' + str(x_time[0]))
                    plt.text(day + pd.Timedelta(hours = 7),480, 'End time: ' + str(x_time[-1]))
                    plt.text(day + pd.Timedelta(hours = 7),470, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
                    plt.text(day + pd.Timedelta(hours = 7),460, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
                elif gas_type == 'NO2':
                    plt.ylim(-1,3)
                    plt.text(day + pd.Timedelta(hours = 7),2.7, 'Srart time: ' + str(x_time[0]))
                    plt.text(day + pd.Timedelta(hours = 7),2.5, 'End time: ' + str(x_time[-1]))
                    plt.text(day + pd.Timedelta(hours = 7),2.3, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
                    plt.text(day + pd.Timedelta(hours = 7),2.1, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
                elif gas_type == 'SO2':
                    plt.ylim(-3,4)
                    plt.text(day + pd.Timedelta(hours = 7),3.7, 'Srart time: ' + str(x_time[0]))
                    plt.text(day + pd.Timedelta(hours = 7),3.5, 'End time: ' + str(x_time[-1]))
                    plt.text(day + pd.Timedelta(hours = 7),3.3, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
                    plt.text(day + pd.Timedelta(hours = 7),3.1, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
                elif gas_type == 'HCHO':
                    plt.ylim(-3,4)
                    plt.text(day + pd.Timedelta(hours = 7),3.7, 'Srart time: ' + str(x_time[0]))
                    plt.text(day + pd.Timedelta(hours = 7),3.5, 'End time: ' + str(x_time[-1]))
                    plt.text(day + pd.Timedelta(hours = 7),3.3, 'Corrected mean = ' + str(format(y1.mean(),'.2f')) + ' DU')
                    plt.text(day + pd.Timedelta(hours = 7),3.1, 'BlickP mean = ' + str(format(y2.mean(),'.2f'))+ ' DU')
                plt.xlabel('LTC')
                plt.ylabel(gas_type + ' VCD [DU]')
                measurement_location = new_df.location[ind_start:ind_end]
                plt.title(instrument_name + '@' + measurement_location[0])
                plt.grid()
                plt.tight_layout()
                if len(str(day.month)) == 1:
                    monthlabel = '0' + str(day.month)
                else:
                    monthlabel = str(day.month)
                if len(str(day.day)) == 1:
                    daylabel = '0' + str(day.day)
                else:
                    daylabel = str(day.day)
                timelabel = str(day.year) + monthlabel + daylabel
                plt.savefig(plot_path + instrument[0] + '_' + str(location) + '_BlickP_vs_CorrectedVCD_' + gas_type + '_'+ timelabel +'.png')
                #plt.show()
                #plt.close(fig)
                plt.clf()
                
        plt.close()    
#%%
import sys

sys.path.insert(0, 'C:\\Users\\ZhaoX\\Documents\\GitHub\\Pandora_onGit\\BlikP')
from sites_list import sites_list
instrument_nm = 'Pandora 104'
#instrument_nm = 'Pandora 103'
#plot_path = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P103_correction3\\'
#plot_path = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P104_correction\\Downsview\\'
plot_path = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P104_correction\\FortMcKay\\'
# load Pandora PanPS processed lev3 data    
#shelve_filename = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P103_plots\\lev3.out'
#shelve_filename = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P104_plots\\Downsview\\lev3.out'
shelve_filename = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P104_plots\\FortMcKay\\lev3.out'
open_shelf(shelve_filename)
#output_shelve_filename = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P103_correction3\\lev3_corrected.out'
#output_shelve_filename = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P104_correction\\Downsview\\lev3_corrected.out'
output_shelve_filename = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P104_correction\\FortMcKay\\lev3_corrected.out'

# use "get_single_fitting_result" to select a fitting window
#df_O3 = get_single_fitting_result(df_lev3,'SU',310.0,330.0,4,0,1,18) # O3, window 5, default ozone
#df_NO2 = get_single_fitting_result(df_lev3,'SO',400.0,440.0,4,0,1,18) # 
df_NO2_modified_1 = get_single_fitting_result(df_lev3,'SO',400.0,500.0,4,-1,-1,2) # NO2, window 2, modified no2, recommended by Vitali
#df_NO2_modified_2 = get_single_fitting_result(df_lev3,'SO',400.0,500.0,4,-1,-1,17)
#df_SO2 = get_single_fitting_result(df_lev3,'SU',306.0,330.0,4,0,1,2) # SO2, window 9, Fioletov et al. AMT, 2016
df_NO2_modified_1.sort_values(by=['UTC'], inplace=True) # need sort the data by time
df = df_NO2_modified_1.copy()

# filters
df = df[df['Column 21: Fitting result index: 1,2=no error, >2=error'] <=2][df['Column 32: Geometrical nitrogen dioxide air mass factor'] <=5][df['Column 64: Integration time [ms]'] < 500]
df =df[df['Column 31: Uncertainty of nitrogen dioxide slant column amount [Dobson Units], negative value=not fitted or fitting not successfull'] < 0.35]

x = df['Column 32: Geometrical nitrogen dioxide air mass factor']
y = df['Column 30: Nitrogen dioxide slant column amount [Dobson Units], -9e99=not fitted or fitting not successfull']
No_days = len(df.time.dt.date.unique())

beta = quantile_regression(x, y, 'NO2', 'dSCDs',plot_path)# plot SCD vs AMF quaintile plots
#monthly_factors = {'year': month_label.year, 'month': month_label.month, 'intercept': beta[0], 'slop': beta[1]}
#monthly_factors = {'year': month_label.year, 'month': month_label.month, 'day': 1, 'intercept': beta[0], 'slop': beta[1], 'No_points': len(x), 'No_days': No_days}
#calibration_factors = calibration_factors.append(monthly_factors, ignore_index = True) # save monthly calibration factors
#df.loc[:,'VCD_corrected'] = (y - beta[0])/x - beta[1] # apply correction factors; this is Vitali's method in his 2016 Pandora SO2 AMT paper
df.loc[:,'VCD_corrected'] = (y - beta[0])/x # apply correction factors; this is Herman's method in Pandora NO2 JGR paper.This makes more sense! 
y = df['VCD_corrected']
print('Ref SCD = ' + str(beta[0]))
quantile_regression(x, y,'NO2', 'VCDs',plot_path) # plot VCD vs AMF quaintile plots
#df['instrument'] = 'Pandora 103'
#daily_plots_LTC(df, 'NO2', 'Pandora 103', plot_path)
df['instrument'] = instrument_nm
daily_plots_LTC(df, 'NO2', instrument_nm, plot_path)

df_lev3 = df.copy()

#%% save merged_data to shelve
import shelve
my_shelf = shelve.open(output_shelve_filename,'n') # 'n' for new
#print(dir())
for key in dir():
    #print(key)
    if key.find('df_lev3') != -1:
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


