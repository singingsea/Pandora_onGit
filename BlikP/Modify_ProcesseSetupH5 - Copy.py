# -*- coding: utf-8 -*-
"""
Created on Wed Sep 27 10:47:44 2017

@author: ZhaoX
This is the function used to modify BlickOTP processing setup file
"""
from IPython import get_ipython ## house keeping, first two lines to clear workspace
get_ipython().magic('reset -sf') 

import h5py
import numpy as np
from shutil import copy

def modify_h5(original_f_nm,new_f_nm):
    copy(original_f_nm,new_f_nm)
    with h5py.File(new_f_nm,'r+') as f:
        print('Found the following keys in the H5 file: ')
        print(list(f.keys()))
        print('\n \n \n')
        
        #%% this block adding new sut1 f code into the h5 file
        print('\t ************ #1 *************')
        values = f['/f_codes'].value
        print('Old f codes values : (No. of codes: ' + str(len(values)) + ')')
        print('--------------------')
        print(values)
        print( )
#        input values used to generate "Blick_ProcessingSetups_so2.h5"  
#        new_values = np.asarray([
#                [ (b'fuh0', b'Sky HCHO setup referencing to largest viewing zenith angle', b'PROFILE', b'U340', b'MeasHigh', b'325', b'360', 3, 1, 1, -1, b'O3,NO2,HCHO,O2O2', b'Daumont4TGOME,Vandaele,MellMoort2000,HermansNewnham', b'1,1,1,1', b'225,254.5,256.9,262.0', b'NO,NO,NO,NO', b'YES', b'NO', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'fuh0', b'11-May-2017', b'Martin Tiefengraber')],
#                [ (b'fus0', b'Direct sun HCHO setup using synthetic reference', b'SUN', b'U340', b'SyntU340', b'332', b'359', 4, 1, 1, -1, b'O3,NO2,HCHO,O2O2', b'Daumont4TGOME,Vandaele,MellMoort2000,HermansNewnham', b'1,1,1,1', b'225,254.5,256.9,262.0', b'NO,NO,NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'fus0', b'11-May-2017', b'Martin Tiefengraber')],
#                [ (b'nvh0', b'Sky NO2 setup referencing to largest viewing zenith angle', b'PROFILE', b'OPEN', b'MeasHigh', b'435', b'490', 4, 1, 1, -1, b'O3,NO2,O2O2,H2O', b'Daumont4TGOME,Vandaele,HermansNewnham,HITRAN', b'1,1,1,1', b'225,254.5,262.0,273.1', b'NO,NO,NO,NO', b'YES', b'NO', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'nvh0', b'20-Jan-2017', b'Alexander Cede')],
#                [ (b'nvs0', b'Original direct sun NO2 setup using synthetic reference', b'SUN', b'OPEN', b'SyntOPEN', b'400', b'440', 4, 0, 1, -1, b'O3,NO2', b'Daumont4TGOME,Vandaele', b'1,1', b'225,254.5', b'NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'nvs0', b'20-Jan-2017', b'Alexander Cede')],
#                [ (b'nvsa', b'Original direct moon NO2 setup using synthetic reference', b'MOON', b'OPEN', b'SyntOPEN', b'400', b'440', 4, 0, 1, -1, b'O3,NO2', b'Daumont4TGOME,Vandaele', b'1,1', b'225,254.5', b'NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'nvsa', b'31-Jul-2017', b'Martin Tiefengraber')],
#                [ (b'ouh0', b'Sky O3 setup referencing to largest viewing zenith angle, longer fitting window', b'PROFILE', b'U340', b'MeasHigh', b'307', b'360', 3, 1, 1, -1, b'O3,NO2,SO2,HCHO,O2O2', b'Daumont4TGOME,Vandaele,Vandaele,MellMoort2000,HermansNewnham', b'1,1,1,1,1', b'225,254.5,259.2,256.9,262.0', b'NO,NO,NO,NO,NO', b'YES', b'NO', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'ouh0', b'12-May-2017', b'Martin Tiefengraber')],
#                [ (b'out0', b'Original direct sun O3 setup using extraterrestrial reference', b'SUN', b'U340', b'ExtRef', b'310', b'330', 4, 0, 1, -1, b'O3,NO2,SO2,HCHO', b'Daumont4TGOME,Vandaele,Vandaele,MellMoort2000', b'1,1,1,1', b'225,254.5,259.2,256.9', b'NO,NO,NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'out0', b'20-Jan-2017', b'Alexander Cede')] ,
#               [ (b'sut1', b'Direct sun SO2 setup using extraterrestrial reference', b'SUN,MOON', b'U340', b'ExtRef', b'306', b'330', 4, 0, 1, -1, b'O3,NO2,SO2,HCHO', b'Daumont4TGOME,Vandaele,Vandaele,MellMoort2000', b'1,1,1,1', b'225,254.5,259.2,256.9', b'NO,NO,NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'NO', b'NO', b'ALL', b'out0', b'27-Sep-2017', b'Xiaoyi Zhao')],
#               #[ (b'sut1', b'Direct sun SO2 setup using extraterrestrial reference', b'SUN,MOON', b'U340', b'ExtRef', b'306', b'330', 4, 0, 1, -1, b'O3,NO2,SO2,HCHO', b'Daumont4TGOME,Vandaele,Vandaele,Meller', b'1,1,1,1', b'225,254.5,259.2,256.9', b'NO,NO,NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'NO', b'NO', b'ALL', b'out0', b'27-Sep-2017', b'Xiaoyi Zhao')],
#               [ (b'sut2', b'Direct sun SO2 setup using synthetic reference', b'SUN,MOON', b'U340', b'SyntU340', b'306', b'330', 4, 0, 1, -1, b'O3,NO2,SO2,HCHO', b'Daumont4TGOME,Vandaele,Vandaele,MellMoort2000', b'1,1,1,1', b'225,254.5,259.2,256.9', b'NO,NO,NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'NO', b'NO', b'ALL', b'out0', b'11-Oct-2017', b'Xiaoyi Zhao')]
#               #[ (b'sut2', b'Direct sun SO2 setup using synthetic reference', b'SUN,MOON', b'U340', b'SyntU340', b'306', b'330', 4, 0, 1, -1, b'O3,NO2,SO2,HCHO', b'Daumont4TGOME,Vandaele,Vandaele,Meller', b'1,1,1,1', b'225,254.5,259.2,256.9', b'NO,NO,NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'NO', b'NO', b'ALL', b'out0', b'11-Oct-2017', b'Xiaoyi Zhao')]
#               ], 
        new_values = np.asarray(
                [[ (b'fuh0', b'Sky HCHO setup referencing to largest viewing zenith angle', b'PROFILE', b'U340', b'MeasHigh', b'325', b'360', 3, 1, 1, -1, b'O3,NO2,HCHO,O2O2', b'Harmonics2013,Vandaele,MellMoort2000,HermansNewnham', b'1,1,1,1', b'225,254.5,256.9,262.0', b'NO,NO,NO,NO', b'YES', b'NO', b'NO', b'MEAS', b'mca1', b'NO', b'NO', b'ALL', b'fuh0', b'11-May-2017', b'Martin Tiefengraber')],
                [ (b'fus0', b'Direct sun HCHO setup using synthetic reference U340', b'SUN', b'U340', b'SyntU340', b'332', b'359', 4, 1, 1, -1, b'O3,NO2,HCHO,O2O2', b'Harmonics2013,Vandaele,MellMoort2000,HermansNewnham', b'1,1,1,1', b'225,254.5,256.9,262.0', b'NO,NO,NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'fus0', b'11-May-2017', b'Martin Tiefengraber')],
                [ (b'fus1', b'Direct sun HCHO setup using synthetic reference OPEN', b'SUN', b'OPEN', b'SyntOPEN', b'332', b'359', 4, 1, 1, -1, b'O3,NO2,HCHO,O2O2', b'Harmonics2013,Vandaele,MellMoort2000,HermansNewnham', b'1,1,1,1', b'225,254.5,256.9,262.0', b'NO,NO,NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'fus0', b'12-Jul-2018', b'Martin Tiefengraber')],
                [ (b'nvh0', b'Sky NO2 setup referencing to largest viewing zenith angle', b'PROFILE', b'OPEN', b'MeasHigh', b'435', b'490', 4, 1, 1, -1, b'O3,NO2,O2O2,H2O', b'Harmonics2013,Vandaele,HermansNewnham,HITRAN', b'1,1,1,1', b'225,254.5,262.0,273.1', b'NO,NO,NO,NO', b'YES', b'NO', b'NO', b'MEAS', b'mca1', b'NO', b'NO', b'ALL', b'nvh0', b'20-Jan-2017', b'Alexander Cede')],
                [ (b'nvs0', b'Original direct sun NO2 setup using synthetic reference', b'SUN', b'OPEN', b'SyntOPEN', b'400', b'440', 4, 0, 1, -1, b'O3,NO2', b'Harmonics2013,Vandaele', b'1,1', b'225,254.5', b'NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'nvs0', b'20-Jan-2017', b'Alexander Cede')],
                [ (b'nvs1', b'Modified direct sun NO2 setup using synthetic reference', b'SUN', b'OPEN', b'SyntOPEN', b'400', b'480', 5, 0, 1, -1, b'O3,NO2', b'Harmonics2013,Vandaele', b'1,1', b'225,254.5', b'NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'nvs0', b'20-Jan-2017', b'Alexander Cede')],
                [ (b'nvsa', b'Original direct moon NO2 setup using synthetic reference', b'MOON', b'OPEN', b'SyntOPEN', b'400', b'440', 4, 0, 1, -1, b'O3,NO2', b'Harmonics2013,Vandaele', b'1,1', b'225,254.5', b'NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'nvsa', b'31-Jul-2017', b'Martin Tiefengraber')],
                [ (b'ouh0', b'Sky O3 setup referencing to largest viewing zenith angle, longer fitting window', b'PROFILE', b'U340', b'MeasHigh', b'307', b'360', 3, 1, 1, -1, b'O3,NO2,SO2,HCHO,O2O2', b'Harmonics2013,Vandaele,Vandaele,MellMoort2000,HermansNewnham', b'1,1,1,1,1', b'225,254.5,259.2,256.9,262.0', b'NO,NO,NO,NO,NO', b'YES', b'NO', b'NO', b'MEAS', b'mca1', b'NO', b'NO', b'ALL', b'ouh0', b'12-May-2017', b'Martin Tiefengraber')],
                [ (b'out0', b'Original direct sun O3 setup using extraterrestrial reference', b'SUN', b'U340', b'ExtRef', b'310', b'330', 4, 0, 1, -1, b'O3,NO2,SO2,HCHO', b'Harmonics2013,Vandaele,Vandaele,MellMoort2000', b'1,1,1,1', b'225,254.5,259.2,256.9', b'NO,NO,NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'OFFMEAS_WLCORR', b'NO', b'ALL', b'out0', b'20-Jan-2017', b'Alexander Cede')],
                [ (b'sut1', b'Direct sun SO2 setup using extraterrestrial reference', b'SUN,MOON', b'U340', b'ExtRef', b'306', b'330', 4, 0, 1, -1, b'O3,NO2,SO2,HCHO', b'Harmonics2013,Vandaele,Vandaele,MellMoort2000', b'1,1,1,1', b'225,254.5,259.2,256.9', b'NO,NO,NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'NO', b'NO', b'ALL', b'out0', b'27-Sep-2017', b'Xiaoyi Zhao')],
                [ (b'sut2', b'Direct sun SO2 setup using synthetic reference', b'SUN,MOON', b'U340', b'SyntU340', b'306', b'330', 4, 0, 1, -1, b'O3,NO2,SO2,HCHO', b'Harmonics2013,Vandaele,Vandaele,MellMoort2000', b'1,1,1,1', b'225,254.5,259.2,256.9', b'NO,NO,NO,NO', b'NO', b'1', b'NO', b'MEAS', b'mca1', b'NO', b'NO', b'ALL', b'out0', b'11-Oct-2017', b'Xiaoyi Zhao')]], 
                 dtype=[('f-code', 'S4'), ('f-Name', 'S100'), ('Process types', 'S50'), ('Filter types', 'S50'), ('Reference', 'S100'), ('WL-starts', 'S50'), ('WL-ends', 'S50'), ('npol', '<i4'), ('noffs', '<i4'), ('nwlc', '<i4'), ('nresc', '<i4'), ('Fitted gases', 'S50'), ('Gas sources', 'S500'), ('Gas OD meths', 'S50'), ('Gas temps', 'S50'), ('Fitted temps', 'S50'), ('Ring', 'S3'), ('Mol scatt', 'S3'), ('Linear fit', 'S3'), ('Uncertainty', 'S5'), ('s-code', 'S4'), ('Diffuse correction', 'S14'), ('Time interpolation', 'S10'), ('Pixels to use', 'S6'), ('qf-code', 'S4'), ('Creation date', 'S11'), ('Author info', 'S50')]
                )
        del f['/f_codes']
        f.create_dataset('/f_codes',data = new_values )
        values = f['/f_codes'].value
        print('\n \n')        
        print('New f codes values : (No. of codes: ' + str(len(new_values)) + ')')
        print('--------------------')
        print(new_values)
        print('\n \n \n')
        
        
        #%% this block adding new sut1 r code into the h5 file
        print('\t ************ #2 *************')
        values = f['/r_codes'].value
        print('Old r codes values : (No. of codes: ' + str(len(values)) + ')')
        print('--------------------')
        print(values)
        print( 'Old r codes length: ' + str(len(values)) )
#        input values used to generate "Blick_ProcessingSetups_so2.h5"  
#        new_values = np.asarray(
#                [[ (b'fuh0', b'Original sky HCHO 325-360nm', b'L2Trop', b'O4RatioSky-Version1', b'HCHO', b'fuh0', b'fuh0', b'11-May-2017', b'Martin Tiefengraber')],
#                [ (b'fus0', b'Direct total HCHO retrieval', b'L2Tot', b'Direct-Version1', b'HCHO', b'fus0', b'fus0', b'11-May-2017', b'Martin Tiefengraber')],
#                [ (b'nvh0', b'Original sky NO2 and H2O 430-495nm', b'L2Trop', b'O4RatioSky-Version1', b'NO2,H2O', b'nvh0,nvh0', b'nvh0', b'20-Jan-2017', b'Alexander Cede')],
#                [ (b'nvs0', b'Original direct total NO2 retrieval', b'L2Tot', b'Direct-Version1', b'NO2', b'nvs0', b'nvs0', b'20-Jan-2017', b'Alexander Cede')],
#                [ (b'nvsa', b'Original direct moon total NO2 retrieval', b'L2Tot', b'Direct-Version1', b'NO2', b'nvsa', b'nvsa', b'31-Jul-2017', b'Martin Tiefengraber')],
#                [ (b'ouh0', b'Original sky O3 307-360nm, longer fitting window', b'L2Trop', b'O4RatioSky-Version1', b'O3,SO2,HCHO', b'ouh0,suh0,fuh0', b'ouh0', b'12-May-2017', b'Martin Tiefengraber')],
#                [ (b'out0', b'Original direct total O3 and SO2 retrieval', b'L2Tot', b'Direct-Version1', b'O3,SO2', b'out0,sut0', b'out0', b'20-Jan-2017', b'Alexander Cede')],
#                [ (b'sut1', b'Direct total SO2 retrieval ExtRef', b'L2Tot', b'Direct-Standard', b'O3,SO2', b'out0,sut0', b'sut1', b'27-Sep-2017', b'Xiaoyi Zhao')],
#                [ (b'sut2', b'Direct total SO2 retrieval SyntU340', b'L2Tot', b'Direct-Standard', b'O3,SO2', b'out0,sut0', b'sut2', b'11-Oct-2017', b'Xiaoyi Zhao')]], 
#                dtype=[('r-code', 'S4'), ('r-Name', 'S100'), ('L2 type', 'S6'), ('Algorithm type', 'S50'), ('Output gases', 'S50'), ('qr-codes', 'S100'), ('f-codes', 'S100'), ('Creation date', 'S11'), ('Author info', 'S50')]
#                )
        new_values = np.asarray(
                [[ (b'fuh0', b'Original sky HCHO 325-360nm', b'L2Trop', b'O4RatioSky-Version1', b'HCHO', b'fuh0', b'fuh0', b'11-May-2017', b'Martin Tiefengraber')],
                [ (b'fus0', b'Direct total HCHO retrieval based on U340', b'L2Tot', b'Direct-Version1', b'HCHO', b'fus0', b'fus0', b'11-May-2017', b'Martin Tiefengraber')],
                [ (b'fus1', b'Direct total HCHO retrieval based on OPEN', b'L2Tot', b'Direct-Version1', b'HCHO', b'fus0', b'fus1', b'12-Jul-2018', b'Martin Tiefengraber')],
                [ (b'nvh0', b'Original sky NO2 and H2O 430-495nm', b'L2Trop', b'O4RatioSky-Version1', b'NO2,H2O', b'nvh0,nvh0', b'nvh0', b'20-Jan-2017', b'Alexander Cede')],
                [ (b'nvs0', b'Original direct total NO2 retrieval', b'L2Tot', b'Direct-Version1', b'NO2', b'nvs0', b'nvs0', b'20-Jan-2017', b'Alexander Cede')],
                [ (b'nvs1', b'Modified direct total NO2 retrieval', b'L2Tot', b'Direct-Version1', b'NO2', b'nvs0', b'nvs1', b'20-Jan-2017', b'Alexander Cede')],
                [ (b'nvsa', b'Original direct moon total NO2 retrieval', b'L2Tot', b'Direct-Version1', b'NO2', b'nvsa', b'nvsa', b'31-Jul-2017', b'Martin Tiefengraber')],
                [ (b'ouh0', b'Original sky O3 307-360nm, longer fitting window', b'L2Trop', b'O4RatioSky-Version1', b'O3,SO2,HCHO', b'ouh0,suh0,fuh0', b'ouh0', b'12-May-2017', b'Martin Tiefengraber')],
                [ (b'out0', b'Original direct total O3 and SO2 retrieval', b'L2Tot', b'Direct-Version1', b'O3,SO2', b'out0,sut0', b'out0', b'20-Jan-2017', b'Alexander Cede')],                
                [ (b'sut1', b'Direct total SO2 retrieval ExtRef', b'L2Tot', b'Direct-Standard', b'O3,SO2', b'out0,sut0', b'sut1', b'27-Sep-2017', b'Xiaoyi Zhao')],
                [ (b'sut2', b'Direct total SO2 retrieval SyntU340', b'L2Tot', b'Direct-Standard', b'O3,SO2', b'out0,sut0', b'sut2', b'11-Oct-2017', b'Xiaoyi Zhao')]], 
                dtype=[('r-code', 'S4'), ('r-Name', 'S100'), ('L2 type', 'S6'), ('Algorithm type', 'S50'), ('Output gases', 'S50'), ('qr-codes', 'S100'), ('f-codes', 'S100'), ('Creation date', 'S11'), ('Author info', 'S50')]
                )
        del f['/r_codes']
        f.create_dataset('/r_codes',data = new_values )
        values = f['/r_codes'].value
        print('\n \n')        
        print('New r codes values : (No. of codes: ' + str(len(new_values)) + ')')
        print('--------------------')
        print(new_values)
        print('\n \n \n')
        
        #%% this block modify fus0 qf code into the h5 file
        print('\t ************ #3 *************')
        values = f['/qf_codes'].value
        print('Old qf codes values : (No. of codes: ' + str(len(values)) + ')')
        print('--------------------')
        print(values)
        print( 'Old qf codes length: ' + str(len(values)) )
#        input values used to generate "Blick_ProcessingSetups_so2.h5"  
#        new_values = np.asarray([
#                [ (b'fuh0', b'Sky HCHO setup referencing to largest viewing zenith angle quality limits', b'0,3', b'1e-2,2e-2', b'0.2,0.5', b'11-May-2017', b'Martin Tiefengraber')],
#                [ (b'fus0', b'Original direct sun HCHO setup using synthetic reference quality limits', b'0,3', b'4e-3,8e-3', b'0.1,0.3', b'11-May-2017', b'Martin Tiefengraber')],
#                [ (b'nvh0', b'Sky NO2 setup referencing to largest viewing zenith angle quality limits', b'0,3', b'1e-2,2e-2', b'0.2,0.5', b'20-Jan-2017', b'Alexander Cede')],
#                [ (b'nvs0', b'Original direct sun NO2 setup using synthetic reference quality limits', b'0,3', b'2e-3,5e-3', b'0.2,0.5', b'20-Jan-2017', b'Alexander Cede')],
#                [ (b'nvsa', b'Original direct moon NO2 setup using synthetic reference quality limits', b'0,3', b'5e-3,7e-3', b'0.5,0.7', b'31-Jul-2017', b'Martin Tiefengraber')],
#                [ (b'ouh0', b'Sky O3 setup referencing to largest viewing zenith angle quality limits', b'0,3', b'1e-2,2e-2', b'0.2,0.5', b'12-May-2017', b'Martin Tiefengraber')],
#                [ (b'out0', b'Original direct sun O3 setup using extraterrestrial reference quality limits', b'0,3', b'1e-2,2e-2', b'0.5,1.0', b'20-Jan-2017', b'Alexander Cede')]       
#                ], 
        new_values = np.asarray(
                [[ (b'fuh0', b'Sky HCHO setup referencing to largest viewing zenith angle quality limits', b'0,3', b'1e-2,2e-2', b'0.2,0.5', b'11-May-2017', b'Martin Tiefengraber')],
                [ (b'fus0', b'Original direct sun HCHO setup using synthetic reference quality limits', b'0,3', b'4e-3,8e-3', b'0.1,0.3', b'11-May-2017', b'Martin Tiefengraber')],
                [ (b'nvh0', b'Sky NO2 setup referencing to largest viewing zenith angle quality limits', b'0,3', b'1e-2,2e-2', b'0.2,0.5', b'20-Jan-2017', b'Alexander Cede')],
                [ (b'nvs0', b'Original direct sun NO2 setup using synthetic reference quality limits', b'0,3', b'2e-3,5e-3', b'0.2,0.5', b'20-Jan-2017', b'Alexander Cede')],
                [ (b'nvsa', b'Original direct moon NO2 setup using synthetic reference quality limits', b'0,3', b'5e-3,7e-3', b'0.5,0.7', b'31-Jul-2017', b'Martin Tiefengraber')],
                [ (b'ouh0', b'Sky O3 setup referencing to largest viewing zenith angle quality limits', b'0,3', b'1e-2,2e-2', b'0.2,0.5', b'12-May-2017', b'Martin Tiefengraber')],
                [ (b'out0', b'Original direct sun O3 setup using extraterrestrial reference quality limits', b'0,3', b'1e-2,2e-2', b'0.5,1.0', b'20-Jan-2017', b'Alexander Cede')]], 
                dtype=[('qf-code', 'S4'), ('qf-Name', 'S100'), ('Fitting result', 'S5'), ('wrms limits', 'S15'), ('WL shift limits', 'S11'), ('Creation date', 'S11'), ('Author info', 'S50')]
                )
        
        del f['/qf_codes']
        f.create_dataset('/qf_codes',data = new_values )
        values = f['/qf_codes'].value
        print('\n \n')        
        print('New qf codes values : (No. of codes: ' + str(len(new_values)) + ')')
        print('--------------------')
        print(new_values)
        print('\n \n \n')

        #%% this block adding new sut1 f code into the h5 file
#        print('\t ************ #4 *************')
#        values = f['/s_codes'].value
#        print('Old s codes values : (No. of codes: ' + str(len(values)) + ')')
#        print('--------------------')
#        print(values)
#        print( )

#%%
if __name__ == '__main__':        
    #original_f_nm = 'C:\\Pano_h5\\Blick_ProcessingSetups_twrcIaP.h5'
    original_f_nm = 'C:\\Pano_h5\\Blick_ProcessingSetups_so2.h5'
    new_f_nm = 'C:\\Pano_h5\\Blick_ProcessingSetups_twrcIaP_SO2.h5'
    modify_h5(original_f_nm,new_f_nm)