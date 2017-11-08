# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 14:56:28 2017

@author: ZhaoX
"""

from IPython import get_ipython ## house keeping, first two lines to clear workspace
get_ipython().magic('reset -sf') 

#%%
import shelve
import pandas as pd
from matplotlib import pyplot as plt

#%% manually inputs
#gas_type = 'SO2'
gas_type = 'HCHO'

#monthly_file = 'C:\\Users\\ZhaoX\\Pandora\\comparision\\BlickP_SO2_monthly_calibration\\BlickP_monthly_calibrated_SO2_Pandora 108.out'
#thirtydays_file = 'C:\\Users\\ZhaoX\\Pandora\\comparision\\BlickP_SO2_30days_calibration_v2\\BlickP_monthly_calibrated_SO2_Pandora 108.out'
monthly_file = 'C:\\Users\\ZhaoX\\Pandora\\comparision\\BlickP_HCHO_monthly_calibration\\BlickP_monthly_calibrated_HCHO_Pandora 108.out'
thirtydays_file = 'C:\\Users\\ZhaoX\\Pandora\\comparision\\BlickP_HCHO_30days_calibration\\BlickP_monthly_calibrated_HCHO_Pandora 108.out'

#%%
load_files = [monthly_file,thirtydays_file]
#load_files = [thirtydays_file]

for i, file in enumerate(load_files):
    my_shelf = shelve.open(file)
    print('Loading BlickP dataframe from: ' + file )
    for key in my_shelf:
        globals()[key]=my_shelf[key]
    my_shelf.close()
    if i == 0:
        calibration_factors_m = calibration_factors.copy()
        df_m = new_df.copy()
        del calibration_factors, new_df
    elif i == 1:
        calibration_factors_30d = calibration_factors.copy()
        df_30d = new_df.copy()
        del calibration_factors, new_df

calibration_factors_m = calibration_factors_m.append(calibration_factors_m[-1:])
calibration_factors_m.reset_index(inplace=True,drop=True)
calibration_factors_m.day[-1:] = 30
calibration_factors_m['time'] = pd.to_datetime(calibration_factors_m[['year','month','day']])

calibration_factors_m.index = calibration_factors_m.time
calibration_factors_m = calibration_factors_m.asfreq(freq='D',method='ffill')
del calibration_factors_m['time'] 
calibration_factors_m.reset_index(inplace = True)

#%% 
def plot_xDays_Calibration_Factor(calibration_factors_m, calibration_factors_30d, gas_type):

    calibration_factors_m = calibration_factors_m[calibration_factors_m.intercept != 0]
    calibration_factors_30d = calibration_factors_30d[calibration_factors_30d.intercept != 0]
    
    fig1= plt.figure(figsize=[15,7], dpi=120, facecolor=[1,1,1])
    ax = plt.gca()
    ax2 = ax.twinx()
    #x_time_stamp = {'year': calibration_factors_m.year, 'month': calibration_factors_m.month, 'day': calibration_factors_m.day}
    x_time_stamp = {'year': calibration_factors_m.time.dt.year, 'month': calibration_factors_m.time.dt.month, 'day': calibration_factors_m.time.dt.day}
    x_30d_time_stamp = {'year': calibration_factors_30d.year, 'month': calibration_factors_30d.month, 'day': calibration_factors_30d.day}
    
    x_time = pd.to_datetime(x_time_stamp)
    x_30d_time = pd.to_datetime(x_30d_time_stamp)
    p1, = ax.plot(x_time,calibration_factors_m.intercept,'b-',label = 'intercept [monthly]')
    p1_30d, = ax.plot(x_30d_time,calibration_factors_30d.intercept,'rx',label = 'intercept [30days]')
    p2, = ax2.plot(x_time,calibration_factors_m.slop,'g-',label = 'slop [monthly]')
    p2_30d, = ax2.plot(x_30d_time,calibration_factors_30d.slop,'kx',label = 'slop [30days]')
    
    ax.set_xlabel('Time', size = 16)
    ax.set_ylabel('Intercept [DU]', size = 16)
    ax2.set_ylabel('Slop [1/AMF]', size = 16)
    
    ax.yaxis.label.set_color(p1.get_color())
    ax2.yaxis.label.set_color(p2.get_color())
   
    lines = [p1, p1_30d, p2, p2_30d]
    ax.legend(lines, [l.get_label() for l in lines])
    
    plt.grid()
    plt.tight_layout()
    plt.savefig('calibration_factors_monthly_vs_30days_' + gas_type + '.png')
    #plt.show()
    plt.close(fig1)
    plt.clf()
    
    
    fig2= plt.figure(figsize=[15,7], dpi=120, facecolor=[1,1,1])
    ax = plt.gca()
    #ax2 = ax.twinx()
    #x_time_stamp = {'year': calibration_factors_m.year, 'month': calibration_factors_m.month, 'day': calibration_factors_m.day}
    #x_30d_time_stamp = {'year': calibration_factors_30d.year, 'month': calibration_factors_30d.month, 'day': calibration_factors_30d.day}
    
    #x_time = pd.to_datetime(x_time_stamp)
    #x_30d_time = pd.to_datetime(x_30d_time_stamp)
    VCD_correction_value_mu2 = -calibration_factors_m.intercept/2-calibration_factors_m.slop
    VCD_correction_value_mu3 = -calibration_factors_m.intercept/3-calibration_factors_m.slop
    VCD_correction_value_mu4 = -calibration_factors_m.intercept/4-calibration_factors_m.slop
    
    VCD_correction_value_mu2_30d = -calibration_factors_30d.intercept/2-calibration_factors_30d.slop
    VCD_correction_value_mu3_30d = -calibration_factors_30d.intercept/3-calibration_factors_30d.slop
    VCD_correction_value_mu4_30d = -calibration_factors_30d.intercept/4-calibration_factors_30d.slop
    
    p1, = ax.plot(x_time,VCD_correction_value_mu2,'-',label = '\mu = 2 [monthly]')
    p1_30d, = ax.plot(x_30d_time,VCD_correction_value_mu2_30d,'x',label = '\mu = 2 [30days]')
    p2, = ax.plot(x_time,VCD_correction_value_mu3,'-',label = '\mu = 3 [monthly]')
    p2_30d, = ax.plot(x_30d_time,VCD_correction_value_mu3_30d,'x',label = '\mu = 3 [30days]')
    p3, = ax.plot(x_time,VCD_correction_value_mu4,'-',label = '\mu = 4 [monthly]')
    p3_30d, = ax.plot(x_30d_time,VCD_correction_value_mu4_30d,'x',label = '\mu = 4 [30days]')
    #p2, = ax2.plot(x_time,calibration_factors_m.slop,'g.--',label = 'slop')
    
    ax.set_xlabel('Time', size = 16)
    ax.set_ylabel('Correction to VCD [DU]', size = 16)
    #ax2.set_ylabel('Slop [1/AMF]', size = 16)
    
    ax.yaxis.label.set_color(p1.get_color())
    #ax2.yaxis.label.set_color(p2.get_color())
   
    lines = [p1, p1_30d, p2, p2_30d, p3, p3_30d]
    ax.legend(lines, [l.get_label() for l in lines])
    
    plt.grid()
    plt.tight_layout()
    plt.savefig('calibration_factors_monthly_vs_30days_' + gas_type + '_VCD_correction_values.png')
    #plt.show()
    plt.close(fig2)
    plt.clf()

    fig3= plt.figure(figsize=[15,7], dpi=120, facecolor=[1,1,1])
    ax = plt.gca()
    ax2 = ax.twinx()
    
    p1, = ax.plot(x_time,calibration_factors_m.No_days,'b-',label = 'No. of days [monthly]')
    p1_30d, = ax.plot(x_30d_time,calibration_factors_30d.No_days,'bx',label = 'No. of days [30days]')
    p2, = ax2.plot(x_time,calibration_factors_m.No_points,'g-',label = 'No. of meas. points [monthly]')
    p2_30d, = ax2.plot(x_30d_time,calibration_factors_30d.No_points,'gx',label = 'No. of meas. points [30days]')

    
    ax.set_xlabel('Time', size = 16)
    ax.set_ylabel('No. of days used in cali.', size = 16)
    ax2.set_ylabel('No. of meas. points used in cali.', size = 16)
    
    ax.yaxis.label.set_color(p1.get_color())
    ax2.yaxis.label.set_color(p2.get_color())
   
    lines = [p1, p1_30d, p2, p2_30d]
    ax.legend(lines, [l.get_label() for l in lines])
    
    plt.grid()
    plt.tight_layout()
    plt.savefig('calibration_factors_monthly_vs_30days_' + gas_type + '_info_calibration.png')
    #plt.show()
    plt.close(fig3)
    plt.clf()
#%%
plot_xDays_Calibration_Factor(calibration_factors_m, calibration_factors_30d, gas_type)