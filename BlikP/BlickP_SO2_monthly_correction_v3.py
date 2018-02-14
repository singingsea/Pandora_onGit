# -*- coding: utf-8 -*-
"""
Created on Tue Oct 31 16:06:26 2017

@author: ZhaoX
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 14:00:37 2017

@author: ZhaoX
"""

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

from matplotlib import pyplot as plt
import matplotlib.dates as dates
import numpy, pdb
from numpy import array
from numpy.polynomial.polynomial import polyval
from scipy.optimize import fmin
import pandas as pd


def quantile_regression(x, y, year_month_str, gas_type, column_type, plot_path):

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
    #fig= plt.figure(figsize=[15,15], dpi=120, facecolor=[1,1,1])
    
    # Plot (x,y) pairs on a scatter diagram.  The argument `s` specifies the symbol
    # area in units of points squared.
    p1= plt.scatter(x, y, s=symbol_size)

    if column_type == 'dSCDs':
        x_min = 1
        y_min = -7
        x_max = 5.0
        y_max = 10
    elif column_type == 'VCDs':
        x_min = 1
        y_min = -2
        x_max = 5.0
        y_max = 6
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
    plt.text(x1_location,y1_location,'Year-Month-Day: ' + year_month_str,  size=18)
    plt.text(x2_location,y2_location, '25th % [intercept slop] = '+ str(beta_hat[4]), size=18)
    plt.text(x3_location,y3_location, 'No. of measurements = '+ str(N_points), size=18)
    # Nothing is displayed until we invoke `show`:
    plt.savefig(plot_path + 'Quantile_regression_'+ column_type + '_vs_AMF_' + year_month_str + '.png')
    #plt.show()
    plt.clf()
    #plt.close()

    return beta_hat[4]

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
            ind_start = day
            ind_end = day + delta_time
    
            if len(new_df.timestamp[ind_start:ind_end]) == 0:
                print('no measurements (after filtration) found in day: ' + str(day))
            else:
                x_time = new_df.timestamp[ind_start:ind_end]
                
                if gas_type == 'O3':
                    y1 = new_df.VCD_corrected[ind_start:ind_end]
                    y2 = new_df['Column 8: Ozone total vertical column amount [Dobson Units], -9e99=retrieval not successful'][ind_start:ind_end]
                elif gas_type == 'NO2':
                    y1 = new_df.VCD_corrected[ind_start:ind_end]
                    y2 = new_df['Column 8: Nitrogen dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful'][ind_start:ind_end]
                elif gas_type == 'SO2':
                    y1 = new_df.VCD_corrected[ind_start:ind_end]
                    y2 = new_df['Column 14: Sulfur dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful'][ind_start:ind_end]
                elif gas_type == 'HCHO':
                    y1 = new_df.VCD_corrected[ind_start:ind_end]
                    y2 = new_df['Column 8: Formaldehyde total vertical column amount [Dobson Units], -9e99=retrieval not successful'][ind_start:ind_end]
             
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
def plot_monthly_Calibration_Factor(calibration_factors, gas_type, plot_path):
    
    calibration_factors = calibration_factors[calibration_factors.intercept != 0]
    
    fig1= plt.figure(figsize=[15,7], dpi=120, facecolor=[1,1,1])
    ax = plt.gca()
    ax2 = ax.twinx()
    x_time_stamp = {'year': calibration_factors.year, 'month': calibration_factors.month}
    x_time_stamp['day'] = 1 # give dummy value for day number
    x_time = pd.to_datetime(x_time_stamp)
    p1, = ax.plot(x_time,calibration_factors.intercept,'b.--',label = 'intercept')
    p2, = ax2.plot(x_time,calibration_factors.slop,'g.--',label = 'slop')
    
    ax.set_xlabel('Time', size = 16)
    ax.set_ylabel('Intercept [DU]', size = 16)
    ax2.set_ylabel('Slop [1/AMF]', size = 16)
    
    ax.yaxis.label.set_color(p1.get_color())
    ax2.yaxis.label.set_color(p2.get_color())
   
    lines = [p1, p2]
    ax.legend(lines, [l.get_label() for l in lines])
    
    plt.grid()
    plt.tight_layout()
    plt.savefig(plot_path + 'Calibration_factors_' + gas_type + '.png')
    #plt.show()
    plt.close(fig1)
    plt.clf()
    
    
    fig2= plt.figure(figsize=[15,7], dpi=120, facecolor=[1,1,1])
    ax = plt.gca()
    #ax2 = ax.twinx()
    x_time_stamp = {'year': calibration_factors.year, 'month': calibration_factors.month}
    x_time_stamp['day'] = 1 # give dummy value for day number
    x_time = pd.to_datetime(x_time_stamp)
    VCD_correction_value_mu2 = -calibration_factors.intercept/2-calibration_factors.slop
    VCD_correction_value_mu3 = -calibration_factors.intercept/3-calibration_factors.slop
    VCD_correction_value_mu4 = -calibration_factors.intercept/4-calibration_factors.slop
    
    p1, = ax.plot(x_time,VCD_correction_value_mu2,'.--',label = '\mu = 2')
    p2, = ax.plot(x_time,VCD_correction_value_mu3,'.--',label = '\mu = 3')
    p3, = ax.plot(x_time,VCD_correction_value_mu4,'.--',label = '\mu = 4')
    #p2, = ax2.plot(x_time,calibration_factors.slop,'g.--',label = 'slop')
    
    ax.set_xlabel('Time', size = 16)
    ax.set_ylabel('Intercept [DU]', size = 16)
    #ax2.set_ylabel('Slop [1/AMF]', size = 16)
    
    ax.yaxis.label.set_color(p1.get_color())
    #ax2.yaxis.label.set_color(p2.get_color())
   
    lines = [p1, p2, p3]
    ax.legend(lines, [l.get_label() for l in lines])
    
    plt.grid()
    plt.tight_layout()
    plt.savefig(plot_path + 'Calibration_factors_' + gas_type + '_VCD_correction_values.png')
    #plt.show()
    plt.close(fig2)
    plt.clf()

#%% 
def plot_xDays_Calibration_Factor(calibration_factors, gas_type, plot_path):
    
    calibration_factors = calibration_factors[calibration_factors.intercept != 0]
    
    fig1= plt.figure(figsize=[15,7], dpi=120, facecolor=[1,1,1])
    ax = plt.gca()
    ax2 = ax.twinx()
    x_time_stamp = {'year': calibration_factors.year, 'month': calibration_factors.month, 'day': calibration_factors.day}
    
    if len(x_time_stamp) == 0:
        print('No calibration were made! Check data inputs or date range.')
    else:
        x_time = pd.to_datetime(x_time_stamp)
        p1, = ax.plot(x_time,calibration_factors.intercept,'b.--',label = 'intercept')
        p2, = ax2.plot(x_time,calibration_factors.slop,'g.--',label = 'slop')
        
        ax.set_xlabel('Time', size = 16)
        ax.set_ylabel('Intercept [DU]', size = 16)
        ax2.set_ylabel('Slop [1/AMF]', size = 16)
        
        ax.yaxis.label.set_color(p1.get_color())
        ax2.yaxis.label.set_color(p2.get_color())
       
        lines = [p1, p2]
        ax.legend(lines, [l.get_label() for l in lines])
        
        plt.grid()
        plt.tight_layout()
        plt.savefig(plot_path + 'Calibration_factors_' + gas_type + '.png')
        #plt.show()
        plt.close(fig1)
        plt.clf()
        
        
        fig2= plt.figure(figsize=[15,7], dpi=120, facecolor=[1,1,1])
        ax = plt.gca()
        #ax2 = ax.twinx()
        x_time_stamp = {'year': calibration_factors.year, 'month': calibration_factors.month, 'day': calibration_factors.day}
        
        x_time = pd.to_datetime(x_time_stamp)
        VCD_correction_value_mu2 = -calibration_factors.intercept/2-calibration_factors.slop
        VCD_correction_value_mu3 = -calibration_factors.intercept/3-calibration_factors.slop
        VCD_correction_value_mu4 = -calibration_factors.intercept/4-calibration_factors.slop
        
        p1, = ax.plot(x_time,VCD_correction_value_mu2,'.--',label = '\mu = 2')
        p2, = ax.plot(x_time,VCD_correction_value_mu3,'.--',label = '\mu = 3')
        p3, = ax.plot(x_time,VCD_correction_value_mu4,'.--',label = '\mu = 4')
        #p2, = ax2.plot(x_time,calibration_factors.slop,'g.--',label = 'slop')
        
        ax.set_xlabel('Time', size = 16)
        ax.set_ylabel('Correction to VCD [DU]', size = 16)
        #ax2.set_ylabel('Slop [1/AMF]', size = 16)
        
        ax.yaxis.label.set_color(p1.get_color())
        #ax2.yaxis.label.set_color(p2.get_color())
       
        lines = [p1, p2, p3]
        ax.legend(lines, [l.get_label() for l in lines])
        
        plt.grid()
        plt.tight_layout()
        plt.savefig(plot_path + 'Calibration_factors_' + gas_type + '_VCD_correction_values.png')
        #plt.show()
        plt.close(fig2)
        plt.clf()
    
        fig3= plt.figure(figsize=[15,7], dpi=120, facecolor=[1,1,1])
        ax = plt.gca()
        ax2 = ax.twinx()
        x_time_stamp = {'year': calibration_factors.year, 'month': calibration_factors.month, 'day': calibration_factors.day}
        
        x_time = pd.to_datetime(x_time_stamp)
        
        p1, = ax.plot(x_time,calibration_factors.No_days,'b.--',label = 'No. of days')
        p2, = ax2.plot(x_time,calibration_factors.No_points,'g.--',label = 'No. of meas. points')
    
        
        ax.set_xlabel('Time', size = 16)
        ax.set_ylabel('No. of days used in cali.', size = 16)
        ax2.set_ylabel('No. of meas. points used in cali.', size = 16)
        
        ax.yaxis.label.set_color(p1.get_color())
        ax2.yaxis.label.set_color(p2.get_color())
       
        lines = [p1, p2]
        ax.legend(lines, [l.get_label() for l in lines])
        
        plt.grid()
        plt.tight_layout()
        plt.savefig(plot_path + 'Calibration_factors_' + gas_type + '_info_calibration.png')
        #plt.show()
        plt.close(fig3)
        plt.clf()
#%%        
def calibration_function(calibration_method,df_Blick,gas_type,VCD_column_nm,AMF_column_nm, plot_path):
    
    df_Blick.index = df_Blick['LTC']
    df_Blick.index = df_Blick.index.tz_localize(None) # remove timezone information (localize)
    df_Blick['timestamp'] = df_Blick.index
    meas_dates = pd.unique(df_Blick.timestamp.dt.date) # dates Pandora made any measurements
    
    #%%
    if calibration_method == 'test':
        fig= plt.figure(figsize=[15,15], dpi=120, facecolor=[1,1,1])
        calibration_factors = pd.DataFrame([],columns=['year','month','day','intercept','slop','No_points','No_days'])
        
        df_Blick['scd_o3'] = df_Blick['Column 8: Ozone total vertical column amount [Dobson Units], -9e99=retrieval not successful']*df_Blick['Column 10: Direct ozone air mass factor']
        df_Blick['scd_so2'] = df_Blick['Column 14: Sulfur dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful']*df_Blick['Column 16: Direct sulfur dioxide air mass factor']
        
        df_Blick['ratio'] = df_Blick['scd_so2']/df_Blick['scd_o3']

        x = df_Blick['Column 16: Direct sulfur dioxide air mass factor']
        y = df_Blick.ratio
        [a, b] = quantile_regression(x, y, 'any', gas_type, 'VCDs_test',plot_path)
        df_Blick['VCD_corrected'] = df_Blick['Column 8: Ozone total vertical column amount [Dobson Units], -9e99=retrieval not successful']*((df_Blick.ratio-a)/df_Blick['Column 10: Direct ozone air mass factor'] - b)

        new_df = df_Blick

    #%% ************* 4. loop over monthes, plot dSCD vs AMF quaintile plots ********************* 
    if calibration_method == 'monthly':
        print('\n \n>>> Performing calibration using monthly data: ')
        #meas_dates = pd.unique(df_Blick.time.dt.date)
        start_day = meas_dates.min()
        end_day = meas_dates.max()
        start_year_month = str(start_day.year) + '-' + str(start_day.month)
        end_year_month = str(end_day.year) + '-' + str(end_day.month)
        if start_year_month == end_year_month:
            end_year_month = str(end_day.year) + '-' + str(end_day.month+1)
        month_labels = pd.date_range(start = start_year_month, end = end_year_month, freq = 'M', tz = 'UTC')
            
        new_df = pd.DataFrame() 
        calibration_factors = pd.DataFrame([],columns=['year','month','intercept','slop'])
        fig= plt.figure(figsize=[15,15], dpi=120, facecolor=[1,1,1])
        for month_label in month_labels:
            year_month_str = str(month_label.year)+ '-' + str(month_label.month)
            try:
                df_Blick_monthly = df_Blick[year_month_str]
                if len(df_Blick_monthly) > 100:
                    #x = df_Blick_monthly['Column 16: Direct sulfur dioxide air mass factor']
                    #y = df_Blick_monthly['Column 14: Sulfur dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful']*x
                    x = df_Blick_monthly[AMF_column_nm]
                    y = df_Blick_monthly[VCD_column_nm]*x
                    No_days = len(df_Blick_monthly.time.dt.date.unique())
                    
                    beta = quantile_regression(x, y, year_month_str, gas_type, 'dSCDs',plot_path)# plot SCD vs AMF quaintile plots
                    #monthly_factors = {'year': month_label.year, 'month': month_label.month, 'intercept': beta[0], 'slop': beta[1]}
                    monthly_factors = {'year': month_label.year, 'month': month_label.month, 'day': 1, 'intercept': beta[0], 'slop': beta[1], 'No_points': len(x), 'No_days': No_days}
                    calibration_factors = calibration_factors.append(monthly_factors, ignore_index = True) # save monthly calibration factors
                    df_Blick_monthly.loc[:,'VCD_corrected'] = (y - beta[0])/x - beta[1] # apply correction factors
                    y = df_Blick_monthly['VCD_corrected']
                    quantile_regression(x, y, year_month_str, gas_type, 'VCDs',plot_path) # plot VCD vs AMF quaintile plots
                    if len(new_df) == 0:
                        new_df = df_Blick_monthly
                    else:
                        new_df = pd.concat([new_df,df_Blick_monthly],ignore_index = True)
                    print('Calibration was made for :' + year_month_str )
                else:
                    print('>>> Only found less than 100 datapoints for' + year_month_str + '(year-month)' + ', data ignored')
            except:
                print('No calibration was made for :' + year_month_str )
        
    #%% ************* 4.1. loop over 30-days, plot dSCD vs AMF quaintile plots ********************* 
    if calibration_method == '30days':
        print('\n \n>>> Performing calibration using time window = 30days ... ')
        day_offset = 15
        
        new_df = pd.DataFrame() 
        calibration_factors = pd.DataFrame([],columns=['year','month','day','intercept','slop','No_points','No_days'])
        #df_Blick['timestamp'] = df_Blick['time']
        #df_Blick = df_Blick.set_index('time')
#        df_Blick.index = df_Blick['LTC']
#        df_Blick.index = df_Blick.index.tz_localize(None) # remove timezone information (localize)
#        df_Blick['timestamp'] = df_Blick.index
#        meas_dates = pd.unique(df_Blick.timestamp.dt.date) # dates Pandora made any measurements
    
        fig= plt.figure(figsize=[15,15], dpi=120, facecolor=[1,1,1])
        for meas_date in meas_dates:
                start_day = meas_date - pd.DateOffset(days = day_offset) # start date that measurements will be used in calibration
                end_day = meas_date + pd.DateOffset(days = day_offset) # end date that measurements will be used in calibration
                TF1 = meas_dates >= start_day.date()
                TF2 = meas_dates <= end_day.date()
                TF3 = TF1 & TF2 # TF index that within the calibration periodes
                if sum(TF3) < 20:
                    extended_day_offset = 30
                    start_day = meas_date - pd.DateOffset(days = extended_day_offset) # start date that measurements will be used in calibration
                    end_day = meas_date + pd.DateOffset(days = extended_day_offset) # end date that measurements will be used in calibration
                    TF1 = meas_dates >= start_day.date()
                    TF2 = meas_dates <= end_day.date()
                    TF3 = TF1 & TF2 # TF index that within the calibration periodes

                    
                if sum(TF3) != 0:
                    start_meas = meas_dates[TF3].min()
                    end_meas = meas_dates[TF3].max()
                    if start_meas == end_meas:
                        end_meas = end_meas + pd.DateOffset(days = 1)
                    df_Blick_xDays = df_Blick[start_meas:end_meas].copy()    
                    #df_Blick_xDays.sort_values(inplace=True,by='timestamp')
                    df_Blick_xDays.sort_values(inplace=True,by='LTC')
                    year_month_str = str(meas_date.year) + '-' + str(meas_date.month) + '-' + str(meas_date.day)
                    
                    if len(df_Blick_xDays) > 100:
                        x = df_Blick_xDays[AMF_column_nm]
                        y = df_Blick_xDays[VCD_column_nm]*x
                        
                        No_days = sum(TF3)
                        beta = quantile_regression(x, y, year_month_str, gas_type, 'dSCDs', plot_path)# plot SCD vs AMF quaintile plots
                        monthly_factors = {'year': meas_date.year, 'month': meas_date.month, 'day': meas_date.day,'intercept': beta[0], 'slop': beta[1], 'No_points': len(x), 'No_days': No_days}
                        calibration_factors = calibration_factors.append(monthly_factors, ignore_index = True) # save monthly calibration factors
                        
                        # apply calibration factors to the measurement day
                        measurement_day_start_ind = meas_date
                        measurement_day_end_ind = meas_date + pd.DateOffset(days=1)
                        df_Blick_1Day = df_Blick_xDays[measurement_day_start_ind:measurement_day_end_ind].copy()
                        if len(df_Blick_1Day) > 0:
                            #df_Blick_1Day['VCD_corrected'] = (y - beta[0])/x - beta[1] # apply correction factors
                            df_Blick_1Day.loc[:,'VCD_corrected'] = (y - beta[0])/x - beta[1] # apply correction factors
                            x = df_Blick_1Day[AMF_column_nm]
                            #y = df_Blick_1Day[VCD_column_nm]
                            y = df_Blick_1Day['VCD_corrected']
                            quantile_regression(x, y, year_month_str, gas_type, 'VCDs', plot_path) # plot VCD vs AMF quaintile plots
                            if len(new_df) == 0:
                                new_df = df_Blick_1Day
                            else:
                                new_df = pd.concat([new_df,df_Blick_1Day],ignore_index = True)
                    else:
                        print('Only found less than 100 datapoints for' + year_month_str + '(year-month)' + ', data ignored')  
        #new_df['time'] = new_df.timestamp
        if len(new_df) > 0:
            new_df = new_df.sort_values(by='UTC')
        else:
            print('\n \n>>>Warning : no measurements left after apply "30days calibration", pls check filters or input data!')       
#%%
    if len(calibration_factors) > 0:
        plot_xDays_Calibration_Factor(calibration_factors, gas_type, plot_path)         
    else:
        print('\n \n>>>Warning : no calibration factors returned, pls check filters or input data!')       
    return new_df, calibration_factors
    
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
def main():
    global gas_type, instrument_name, new_df, calibration_factors, plot_path, df_Blick, useful_column_strs
    #%% ************* 1. import BlickP L2 data *********************
    import shelve
    my_shelf = shelve.open(Blick_shelve_filename)
    print('\n \n>>>Loading BlickP dataframe from: ' + Blick_shelve_filename )
    
    L2data_key = instrument_name + 's1_' + Short_location_name + '_L2Tot_rsut2p1' # eg. saved L2data name: Pandora108s1_Downsview_L2Tot_rsut2p1
    for key in my_shelf:
        if key == L2data_key:
            globals()['df_Blick']=my_shelf[key]
    my_shelf.close()
    
#    for key in my_shelf:
#        globals()[key]=my_shelf[key]
#    my_shelf.close()    
#    import pandas as pd
#    df_Blick = pd.concat([Pandora108s1_Downsview_L2Tot_rsut2p1,Pandora108s1_FortMcKay_L2Tot_rsut2p1], ignore_index = True)
#    df_Blick = pd.concat([Pandora123s1_Downsview_L2Tot_rsut2p1,Pandora123s1_FortMcKay_L2Tot_rsut2p1], ignore_index = True)
    #%% ************* 2. serch for corresponding column names in L2 data *********************
    
    [AMF_column_nm, VCD_column_nm, VCD_err_column_nm, L2_fit_quality_column_nm, integration_time_column_nm] = L2_data_column_nm_search(useful_column_strs,df_Blick)
    
    #%% ************* 3. filtering the data *********************
    initial_size = len(df_Blick)

    df_Blick = df_Blick[df_Blick[L2_fit_quality_column_nm] <= 1]
    #df_Blick = df_Blick[df_Blick[integration_time_column_nm] <= 500]
    #df_Blick = df_Blick[df_Blick[AMF_column_nm] <= 5]
    #df_Blick = df_Blick[df_Blick[VCD_err_column_nm] < 0.35]
    
    #df_Blick_2mu = df_Blick[df_Blick[AMF_column_nm] <= 2]
    #df_Blick_3mu = df_Blick[df_Blick[AMF_column_nm] > 2][df_Blick[AMF_column_nm] <= 3]
    #df_Blick_5mu = df_Blick[df_Blick[AMF_column_nm] > 3][df_Blick[AMF_column_nm] <= 5]
    #df_Blick_2mu = df_Blick_2mu[df_Blick_2mu[integration_time_column_nm] <= 100]
    #df_Blick_3mu = df_Blick_3mu[df_Blick_3mu[integration_time_column_nm] <= 300]    
    #df_Blick = pd.concat([df_Blick_2mu,df_Blick_3mu,df_Blick_5mu], ignore_index = True)
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
    
    [new_df, calibration_factors] = calibration_function(calibration_method,df_Blick,gas_type,VCD_column_nm,AMF_column_nm,plot_path)         
        
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
    #sys.path.insert(0, 'C://Users//ZhaoX//Pandora_onGit//local_inputs')
    sys.path.insert(0, 'C:\\Users\\ZhaoX\\Documents\\GitHub\\Pandora_onGit\\local_inputs')
    from BlickP_SO2_correction_inputs import *
    main()




