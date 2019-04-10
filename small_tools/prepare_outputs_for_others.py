# -*- coding: utf-8 -*-
"""
Created on Thu Jun 14 15:12:36 2018

@author: ZhaoX
"""

def open_shelf(shelve_filename):
    import shelve
    my_shelf = shelve.open(shelve_filename)
    
    for key in my_shelf:
        globals()[key]=my_shelf[key]
    my_shelf.close()  
    

#shelve_filename = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\123\\Blick\\L2\\SO2_correction_monthly_FortMcKay\\BlickP_monthly_calibrated_SO2_Pandora123.out'
#shelve_filename = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\123\\Blick\\L2\\SO2_correction_30days_FortMcKay\\BlickP_monthly_calibrated_SO2_Pandora123.out'
#shelve_filename = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\108\\Blick\\old\\L2\\Blick_L2.out'
#shelve_filename = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\109\\Blick\\L2\\Blick_L2.out'
#shelve_filename = 'E:\\Projects\\Zenith_NO2\\Pan_level3data_V2_plots\\lev3.out'
#shelve_filename = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P103_plots\\lev3.out'
#shelve_filename = '\\\\wdow05dtmibroh.ncr.int.ec.gc.ca\\GDrive\\Pandora\\103\\Blick\\L2\\Blick_L2.out'
#shelve_filename = '\\\\wdow05dtmibroh.ncr.int.ec.gc.ca\\GDrive\\Pandora\\108\\Blick\\L2\\Blick_L2.out'
#shelve_filename = '\\\\wdow05dtmibroh.ncr.int.ec.gc.ca\\GDrive\\Pandora\\122\\Blick\\L2\\Blick_L2.out'
#shelve_filename = '\\\\wdow05dtmibroh.ncr.int.ec.gc.ca\\GDrive\\Pandora\\104\\Blick\\L2\\Blick_L2.out'

shelve_filename = '\\\\WONTLABJ105896.ncr.int.ec.gc.ca\\G\\Pandora\\103\\Blick\\L2\\Blick_L2.out'

open_shelf(shelve_filename)

import pandas as pd
#df = Pandora122s1_FortMcKay_L2Tot_rnvs0p1
df = Pandora103s1_FortMcKay_L2Tot_rnvs0p1

df_output = pd.DataFrame()
df_output['instrument'] = df.instrument
df_output['location'] = df.location
df_output['UTC'] = df.UTC
df_output['LTC'] = df.LTC
df_output['SZA'] = df['Column 4: Solar zenith angle for center of measurement in degree']
df_output['NO2'] = df['Column 8: Nitrogen dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful']
df_output['NO2_err'] = df['Column 9: Uncertainty of nitrogen dioxide total vertical column amount [Dobson Units] based on measured uncertainty, -8=retrieval not successful, -1=cross section is zero in this wavelength range, -3=spectral fitting was done, but no uncertainty could be retrieved']
df_output['L2_quality_flag'] = df['Column 11: L2 data quality flag for nitrogen dioxide: 0=high quality, 1=medium quality, 2=low quality']
df_output['int_time'] = df['Column 31: Integration time [ms]']

df_output = df_output[df_output['L2_quality_flag']<=1]
