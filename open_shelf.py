# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 12:34:31 2017

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
shelve_filename = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P103_correction3\\lev3_corrected.out'
open_shelf(shelve_filename)