# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:28:00 2018

@author: ZhaoX
"""

# this function is intent to reformat BlickP processed L1 data to QDOAS readable files

import pandas as pd
from pysolar.solar import *
import datetime
import dateutil.parser
import numpy as np
instrument_no = 108 # the instrument serieal number
process_PanPS_lev2 = False # if True, process PanPS lev2 data, if False process BlickP L1 data
process_all_files = False # process all files in L1 folder, or just for a period

start_date = '2018-07-19' # use 'yyyy-mm-dd' format, this only used if process_all_files = False  
end_date = '2018-07-19' # use 'yyyy-mm-dd' format, this only used if process_all_files = False
# the location, lat, lon, and alt information will be direactly read from L1 file

# provide the file path, L1 file or lev2 file
L1_file_path = '\\\\WONTLABJ105896\\G\\Pandora\\'  + str(instrument_no) + '\\Blick\\L1\\'
#lev2_file_path = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\'  + str(instrument_no) + '\\L2\\'
lev2_file_path = '\\\\WONTLABJ105896\\G\\Pandora\\'  + str(instrument_no) + '\\L2\\FortMcKay\\'
#lev2_file_path = '\\\\wdow05dtmibroh.ncr.int.ec.gc.ca\\GDrive\\Pandora\\zipfiles\\Pan_level2data\\'

# provide the output file path
#spe_file_path = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\'  + str(instrument_no) + '\\Blick\\spe_lev2_from_Vitali_2013_2014\\'
#spe_file_path = '\\\\wdow05dtmibroh\\G\\Pandora\\'  + str(instrument_no) + '\\Blick\\spe_BlickP_L1\\'
spe_file_path = '\\\\WONTLABJ105896.ncr.int.ec.gc.ca\\G\\Pandora\\' + str(instrument_no) + '\\Blick\\spe_BlickP_L1\\'
#spe_file_path = '\\\\WONTLABJ105896\\G\\Pandora\\'  + str(instrument_no) + '\\spe_PanPS_lev2\\FortMacKay\\'

# please update the site list, this is used to interpret local standard time 
#sites_list_LTC = {'Downsview': 'America/Toronto', 'FortMcKay': 'America/Edmonton',  'Fort McKay': 'America/Edmonton', 'StGeorge':'America/Toronto', 'Toronto':'America/Toronto', 'Egbert':'America/Toronto'}
sites_list_LSC = {'Downsview': 'EST', 'FortMcKay': 'MST', 'Fort McKay': 'MST', 'StGeorge':'EST', 'Toronto' : 'EST', 'Egbert':'EST'}


Measurement_Type_Index_dict = {
        0 : 'ONLYL1',
        1 : 'NOL1',
        2 : 'DIRECT SUN',
        3 : 'DIRECT MOON',
        4 : 'ZENITH',
        5 : 'TARGET',
        6 : 'OFFAXIS',
        7 : 'ALMUCANTAR',
        8 : 'LAMP',
        9 : 'SPECIAL'
        }

# Use this dict to interpret the two letter routine code to measurement type. This is only used for old PanPS lev2 data, for BlickP L1 data, we can directly use measurement type index dict 
Measurement_Routine_Index_dict = {
        'AO' : 'ALMUCANTAR',
        'AU' : 'ALMUCANTAR',
        'ZO' : 'ZENITH',
        'ZU' : 'ZENITH',
        'SO' : 'DIRECT SUN',
        'SU' : 'DIRECT SUN'        
        }
#%%
def read_BlickP_L1(file_nm):
    
    f = open(file_nm,'r')
    header_part_ind = 0 # use the '----' symble as header identification
    No_header_lines = 0
    column_names = []
    read_column_names = False
    while header_part_ind != 2: # the data part start after read in '----' twice
        header = f.readline() # read in a line of the file
        if header.find('Instrument number: ') != -1: # find instrument number    
            instrument_no = float(header[len('Instrument number: '):])
        if header.find('Short location name: ') != -1: # find 'Short location name'
            location = header[len('Short location name: '):]
            if location.find('\n'):
                location = location[:-1]
        if header.find('Location latitude [deg]: ') != -1: # find 'latitude'    
            lat = float(header[len('Location latitude [deg]: '):])
        if header.find('Location longitude [deg]: ') != -1: # find 'longitude'    
            lon = float(header[len('Location longitude [deg]: '):])
        if header.find('Location altitude [m]: ') != -1: # find 'altitude'    
            alt = float(header[len('Location altitude [m]: '):])
            
        No_header_lines += 1 # count how many lines belong to header
        if header.find('----') != -1: # find '----' symble
            header_part_ind += 1
            if header_part_ind == 1:
                read_column_names = True # the lines after first '----' is considered as column names
            else:
                read_column_names = False
        if read_column_names == True:
            column_names.append(header.strip()) # save column names           
    del column_names[0]
    del column_names[-1:-3]
    
    for spec_data_column in list(range(64,6207)):
        column_names.append('L1_' + str(spec_data_column)) 
        
  
       
    #print(No_header_lines)
    f.close()           
                          
    df = pd.read_csv(file_nm, sep='\s+', header=None, names = column_names, skiprows= No_header_lines) # read in data use Pandas frame
   
    return df, instrument_no, location, lat, lon, alt
#%%
def read_PanPS_lev2(file_nm):
    
    f = open(file_nm,'r')
    header_part_ind = 0 # use the '----' symble as header identification
    No_header_lines = 0
    column_names = []
    read_column_names = False
    while header_part_ind != 2: # the data part start after read in '----' twice
        header = f.readline() # read in a line of the file
        if header.find('Pandora #') != -1: # find instrument number    
            instrument_no = float(header[len('Pandora #'):len('Pandora #')+3])
        if header.find('at Envcanad(') != -1: # find 'Short location name'
            location = header[len('at Envcanad('):header.find(')')]
            lat = float(header[header.find('Lat ')+4:header.find(', Long')-1])
            lon = float(header[header.find('Long ')+4:header.find('Long ')+4+7])  
            alt = float(header[header.find('m a.s.l.')-4:header.find('m a.s.l.')])
            
        No_header_lines += 1 # count how many lines belong to header
        if header.find('----') != -1: # find '----' symble
            header_part_ind += 1
            if header_part_ind == 1:
                read_column_names = True # the lines after first '----' is considered as column names
            else:
                read_column_names = False
        if read_column_names == True:
            column_names.append(header.strip()) # save column names           
    del column_names[0]
    del column_names[-1:-3]
    for spec_data_column in list(range(54,4149)):
        column_names.append('L1_' + str(spec_data_column)) 
        
  
       
    #print(No_header_lines)
    f.close()           
                          
    df = pd.read_csv(file_nm, sep='\s+', header=None, names = column_names, skiprows= No_header_lines,index_col = False) # read in data use Pandas frame
   
    return df, instrument_no, location, lat, lon, alt

#%%
def check_ZS_modes(full_file_name, df):
   df_sp = df[['Column 1: Two letter code of measurement routine','Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)']]
   df_sp['datetime'] = pd.to_datetime(df_sp['Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)'])
   TF = (df_sp['Column 1: Two letter code of measurement routine'] == 'ZO') | (df_sp['Column 1: Two letter code of measurement routine'] == 'ZU')
   no_ZS = sum(TF)
   return no_ZS

#%% 
def QDOAS_ASCII_formater_header(df,process_PanPS_lev2):
        if process_PanPS_lev2 == False:
            column_nm_dict = {
                    'Column 1: Two letter code of measurement routine':'measurement_routine',
                    'Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)':'ISO_time',
                    'Column 6: Total duration of measurement set in seconds':'measurement_time',
                    'Column 7: Data processing type index':'Data_processing_type',# this is Pandora L1 data type, 2 = direct-sun, 3 = direct-moon, 4 = zenith-sky, 6 = profile, 7 = almucantar
                    'Column 8: Integration time [ms]':'Int_time',
                    'Column 12: Effective position of filterwheel #1, 0=filterwheel not used, 1-9 are valid positions':'FW_1',
                    'Column 13: Effective position of filterwheel #2, 0=filterwheel not used, 1-9 are valid positions':'FW_2',
                    'Column 14: Pointing zenith angle in degree, absolute or relative (see next column), 999=tracker not used':'PZA',
                    'Column 15: Zenith pointing mode: zenith angle is... 0=absolute, 1=relative to sun, 2=relative to moon':'ZPM',
                    'Column 16: Pointing azimuth in degree, increases clockwise, absolute (0=north) or relative (see next column), 999=tracker not used':'PAA',
                    'Column 17: Azimuth pointing mode: like zenith angle mode but also fixed scattering angles relative to sun (3) or moon (4)':'APM',
                    #'Column 61: Scale factor for data, to obtain unscaled output divide data by this number':'scale_factor',# for Blick1.3
                    'Column 78: Scale factor for data, to obtain unscaled output divide data by this number':'scale_factor',# for Blick1.5
                    'Column 63: Level 1 data type, data are... 1=corrected count rate [s-1], 2=radiance [W/m2/nm/sr], 3=irradiance [W/m2/nm]':'data_type'# for Blick1.3
                    #'Column 80: Level 1 data type, data are... 1=corrected count rate [s-1], 2=radiance [uW/m2/nm/sr], 3=irradiance [uW/m2/nm]':'data_type'# for Blick1.5
                    }           
#            df_sp = df[['Column 1: Two letter code of measurement routine',
#                    'Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)',
#                    'Column 6: Total duration of measurement set in seconds',
#                    'Column 7: Data processing type index',
#                    'Column 8: Integration time [ms]',
#                    'Column 12: Effective position of filterwheel #1, 0=filterwheel not used, 1-9 are valid positions',
#                    'Column 13: Effective position of filterwheel #2, 0=filterwheel not used, 1-9 are valid positions',
#                    'Column 14: Pointing zenith angle in degree, absolute or relative (see next column), 999=tracker not used',
#                    'Column 15: Zenith pointing mode: zenith angle is... 0=absolute, 1=relative to sun, 2=relative to moon',
#                    'Column 16: Pointing azimuth in degree, increases clockwise, absolute (0=north) or relative (see next column), 999=tracker not used',
#                    'Column 17: Azimuth pointing mode: like zenith angle mode but also fixed scattering angles relative to sun (3) or moon (4)',
#                    'Column 61: Scale factor for data, to obtain unscaled output divide data by this number',
#                    'Column 63: Level 1 data type, data are... 1=corrected count rate [s-1], 2=radiance [W/m2/nm/sr], 3=irradiance [W/m2/nm]'
#                    ]]
        else:
            column_nm_dict = {
                    'Column 1: Two letter code of measurement routine':'measurement_routine',
                    'Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)':'ISO_time',
                    'Column 5: Total duration of measurement set in seconds':'measurement_time',
                    'Column 5: Total duration of measurement set in seconds (=#, if the line is a comment line)':'measurement_time', # this is for old version of PanPS lev2 data, such as 2013-2014
                    #'Column 7: Data processing type index':'Data_processing_type',# this is Pandora L1 data type, 2 = direct-sun, 3 = direct-moon, 4 = zenith-sky, 6 = profile, 7 = almucantar
                    'Column 6: Integration time [ms]':'Int_time',
                    'Column 9: Position of filterwheel #1, 0=filterwheel not used, 1-9 are valid positions':'FW_1',
                    'Column 10: Position of filterwheel #2, 0=filterwheel not used, 1-9 are valid positions':'FW_2',
                    'Column 11: Pointing zenith angle in degree, absolute or relative (see next column), 999=tracker not used':'PZA',
                    'Column 12: Zenith pointing mode: zenith angle is... 0=absolute, 1=relative to sun, 2=relative to moon':'ZPM',
                    'Column 13: Pointing azimuth in degree, increases clockwise, absolute (0=north) or relative (see next column), 999=tracker not used':'PAA',
                    'Column 14: Azimuth pointing mode: like zenith angle mode but also fixed scattering angles relative to sun (3) or moon (4)':'APM',
                    'Column 51: Scale factor for output data, to obtain unscaled output devide data by this number':'scale_factor',
                    'Column 51: Scale factor for output data (to obtain unscaled output devide data by this number)' : 'scale_factor',# this is for old version of PanPS lev2 data, such as 2013-2014
                    'Column 53: Level 2 data type, data are... 1=corrected count rate [s-1], 2=irradiance [mW/m2/nm], 3=radiance [mW/m2/nm/sr]':'data_type'
                    }    
        df_sp = pd.DataFrame()
        for key in column_nm_dict.keys():
            try:
                df_sp[column_nm_dict[key]] = df[key]
            except:
                pass
            
        df_sp['datetime'] = pd.to_datetime(df_sp['ISO_time'], utc = True)
        

        # add timestamp
        print('     Convert ISO 8601 time to Python-dateutil datetime')
        df_sp['time'] = list(map(dateutil.parser.parse, df_sp['ISO_time']))
        # add UTC and LTC
        print('     Add UTC column to dataframe')              
        df_sp['UTC'] = df_sp.time.dt.tz_convert('UTC')
        if location in sites_list_LSC.keys():
            #print('Add LTC column to dataframe')              
            #df_sp['LTC'] = df_sp.time.dt.tz_convert(sites_list_LTC[location])
            print('     Add LSC column to dataframe')              
            df_sp['LSC'] = df_sp.time.dt.tz_convert(sites_list_LSC[location])
        else:
            print('     Warning: the location of the measurements was not included in sites list!')   
            print('     ' + location)   
        # calcuate SZA
        print('     Add SZA and SAA column to dataframe')  
        df_sp['SZA'] = '' 
        df_sp['SAA'] = '' 
        
        calculated_SZA = np.zeros(shape=(len(df_sp),1))
        calculated_SAA = np.zeros(shape=(len(df_sp),1))
        for i in range(len(df_sp)):
            calculated_SZA[i] = 90 - get_altitude(lat, lon, df_sp.LSC[i])          
            calculated_SAA[i] = get_azimuth(lat, lon, df_sp.LSC[i])
        # assign the calculated SZA and SAA to dataframe   
        df_sp.SZA = calculated_SZA
        df_sp.SAA = calculated_SAA
        
        
        df_output = pd.DataFrame()
        df_output['UTC'] = df_sp.UTC
        df_output['Date'] = df_output.UTC.dt.strftime('%d/%m/%Y')
        df_output['time'] = df_output.UTC.dt.strftime('%H:%M:%S')
        df_output['Exposure'] = df_sp['Int_time']/1000 # QDOAS need exposure time in sec
        df_output['Total_Measurement_Time'] = df_sp['measurement_time']
        df_output['SZA'] = df_sp.SZA # solar zenith angle [deg]
        df_output['SAA'] = df_sp.SAA # solar azimuth angle [deg]
        df_output['VAA'] = '' # viewing azimuth angle angle [deg]
        df_output['VEA'] = ''# viewing elevation angle angle [deg]
        df_output['fd'] = ''
        df_output['Scale_factor'] = df_sp['scale_factor']
        df_output['FW1'] = df_sp['FW_1']
        df_output['FW2'] = df_sp['FW_2']
        
        if process_PanPS_lev2 == False:        
            # make measurement type column
            df_output['Measurement_Type_Index'] = df_sp['Data_processing_type'] # this is Pandora L1 data type, 2 = direct-sun, 3 = direct-moon, 4 = zenith-sky, 6 = profile, 7 = almucantar
            df_output['Measurement_Type'] = ''
            for i in range(len(df_sp)):
                col_num = df_output.columns.get_loc('Measurement_Type')
                try:
                    df_output.iat[i,col_num] = Measurement_Type_Index_dict[df_output.Measurement_Type_Index[i]]
                except:
                    print(str(df_output.Measurement_Type_Index[i]))
        else:
            df_output['Measurement_Type_Index'] = df_sp['measurement_routine']
            df_output['Measurement_Type'] = ''
            for i in range(len(df_sp)):
                col_num = df_output.columns.get_loc('Measurement_Type')
                try:
                    df_output.iat[i,col_num] = Measurement_Routine_Index_dict[df_output.Measurement_Type_Index[i]]
                except:
                    print(str(df_output.Measurement_Type_Index[i])) 
                    
                    
        # make elevation viewing angle column
        col_nm_VEA = df_output.columns.get_loc('VEA')
        col_nm_VAA = df_output.columns.get_loc('VAA')
        col_nm_PZA = df_sp.columns.get_loc('PZA')
        col_nm_PAA = df_sp.columns.get_loc('PAA')
        col_nm_SZA = df_sp.columns.get_loc('SZA')
        col_nm_SAA = df_sp.columns.get_loc('SAA')
        for i in range(len(df_sp)):
            if df_sp['ZPM'][i] == 0:               
                df_output.iat[i,col_nm_VEA] = 90 - df_sp.iat[i,col_nm_PZA]
            elif df_sp['ZPM'][i] == 1:
                df_output.iat[i,col_nm_VEA] = 90 - df_sp.iat[i,col_nm_SZA] - df_sp.iat[i,col_nm_PZA]
            elif df_sp['ZPM'][i] == 2:
                print('Warning: we do not calcualte moon location!')  
                df_output.iat[i,col_nm_VEA] = 'NaN'
                
        # make azimuth viewing angle column        
        for i in range(len(df_sp)):            
            if df_sp['APM'][i] == 0:
                df_output.iat[i,col_nm_VAA] = df_sp.iat[i,col_nm_PAA]
            elif df_sp['APM'][i] == 1:
                df_output.iat[i,col_nm_VAA] = df_sp.iat[i,col_nm_SAA] - df_sp.iat[i,col_nm_PAA]
            elif df_sp['APM'][i] == 2:
                print('Warning: we do not calcualte moon location!')  
                df_output.iat[i,col_nm_VAA] = 'NaN'     
        
        # make fractional day column
        #for i in range(len(df_sp)):
        #    hh = df_sp['UTC'][i].hour
        #    mm = df_sp['UTC'][i].minute
        #    ss = df_sp['UTC'][i].second
        #    df_output.fd[i] = float(pd.datetime.strftime(df_sp.LSC[i],'%j')) -1 + hh/24 + mm/24/60 + ss/24/60/60
            
        return df_output    

#%%
def QDOAS_ASCII_formater_write(df_header,df_spec,file_name, instrument_no, location, lat, lon, alt):
    spefilename = spe_file_path + file_name[:-4] + '.spe'
    with open(spefilename, 'w') as f:
        # write the general header
        f.write('# Station = ' + location + '(lat ' + str(lat) + ' , lon ' + str(lon) + ')' + '\n')
        f.write('# Institute = Environment and Climate Change Canada' + '\n')
        f.write('# PI name = Vitali Fioletov (vitali.fioletov@canada.ca)' + '\n')
        f.write('# Instrument = Pandora ' + str(instrument_no) + '\n')
        f.write('# Size of the detector = 2048 (the size of the detector as indication)' + '\n')
        f.write('# Total number of records = ' + str(len(df_header)) + '\n')
        f.write('# Filter wheel 1 positions = ' + str(pd.unique(df_header.FW1)) + '\n')
        f.write('# Filter wheel 2 positions = ' + str(pd.unique(df_header.FW2)) + '\n')

        # loop over for all spectra
        for i in range(len(df_header)):
            # write the header for each spectrum
            f.write('Date(DD/MM/YYY) = ' + str(df_header.Date[i]) + '\n')
            f.write('UTC Time (hh:mm:ss) = ' + str(df_header.time[i]) + '\n')
            #f.write('UTC Start Time (hh:mm:ss) = ' + str(df_header.time[i]) + '\n')

            f.write('Viewing Elevation Angle (deg) = ' + str(df_header.VEA[i]) + '\n') 
            f.write('Viewing Azimuth Angle (deg) = ' + str(df_header.VAA[i]) + '\n')
            f.write('Measurement Type (OFFAXIS/DIRECT SUN/ALMUCANTAR/ZENITH) = ' + df_header.Measurement_Type[i] + '\n')
            f.write('Total Measurement Time (sec) = ' + str(df_header.Total_Measurement_Time[i]) + '\n')
            
            f.write('Exposure Time(sec) = ' + str(df_header.Exposure[i]) + '\n')
            f.write('Solar Zenith Angle (deg) = ' + str(df_header.SZA[i]) + '\n')
            f.write('Solar Azimuth Angle (deg) = ' + str(df_header.SAA[i])  + ' (North=0, East=90)' + '\n')
            
            f.write('Latitude = ' + str(lat) + '\n')
            f.write('Longitude = ' + str(lon) + '\n')
            f.write('Altitude = ' + str(alt) + '\n')

            # calculate un-scaled spec
            spec = df_spec.iloc[i,:]/df_header.Scale_factor[i]
            # make a dataframe to store spec
            df_spec_4write = pd.DataFrame(columns = ['place_holder','spec'])
            df_spec_4write['spec'] = spec
            # write the spec dataframe into file
            df_spec_4write.to_csv(f, mode = 'a', sep = '\t',index = False,header = False)

#%%
import os
import shutil
total_ZS = 0
if process_PanPS_lev2 == False:
    src_file_path = L1_file_path       
else:
    src_file_path = lev2_file_path
src_files = os.listdir(str(src_file_path))

if process_all_files == False:
    start_date = pd.to_datetime(start_date,utc=True)
    end_date = pd.to_datetime(end_date,utc=True)
    
for idx, file_name in enumerate(src_files):  
    if process_PanPS_lev2 == False:
        date_on_filename = file_name[file_name.find('_L1')-8:file_name.find('_L1')]
    else:
        date_on_filename = file_name[file_name.find('_lev2')-8:file_name.find('_lev2')]
    date_on_filename = pd.to_datetime(date_on_filename,utc=True)
    
    # check if we want process all files in the L1 data folder, or just for a period
    process_this_L1_file = False
    if process_all_files == True:
        process_this_L1_file = True
    else:
        if (date_on_filename >= start_date) & (date_on_filename <= end_date):
           process_this_L1_file = True     
    
    full_file_name = os.path.join(src_file_path, file_name) # creat full file name (including path)
    if (os.path.isfile(full_file_name)): # only get files
        if (full_file_name.find('Pandora' + str(instrument_no)) != -1): # only get files that have name "PandoraXXX" and "L1"
            if not os.path.getsize(full_file_name) == 0: # only copy non-zero size L0 file
                if process_this_L1_file == True:
                    if process_all_files == True:
                        print(' >>> Formating ' + file_name + ' [' +str(idx/len(src_files)*100) + '% finished ... ]')
                    else:
                        print(' >>> Formating ' + file_name )
                    print('     read BlickP L1 file ... ')
                    
                    #### if we reformat BlickP L1 data ###
                    if process_PanPS_lev2 == False:
                        df, instrument_no_infile, location, lat, lon, alt = read_BlickP_L1(full_file_name) # read L1 file
                        
                        # check if we have same instrument number as indicated 
                        if instrument_no_infile != instrument_no: 
                            print('     Warning, instrument number found in L1 file does not match with input value! Will record the true value found in L1 file into spe file. ')
                            instrument_no = instrument_no_infile  
                           
                        height, width = df.shape
                        if height == 0: # check if the L1 file is "empty"
                            print('     an empty L1 file, escape from reformat ... ')
                        else: 
                            print('     prepare header of the spe file ... ')
                            df_header = QDOAS_ASCII_formater_header(df,process_PanPS_lev2) # prepare header part of the spe file
                            print('     prepare spectrum of the spe file ... ')
                            df_spec = df.iloc[:,63:2111] # prepare spectrum  part of the spe file, note here the spec is scaled value!
                            print('     writting to QDOAS spe file ... ')
                            
                            # speration of modes
                            Measurement_Types = pd.unique(df_header.Measurement_Type)
                            #FW1_Types = pd.unique(df_header.FW1)
                            FW2_Types = pd.unique(df_header.FW2)
                            # loop over all measurement types found in this L1 file
                            for Measurement_Type in Measurement_Types:   
                                # loop over all Filter wheel #2 positions found in this L1 file
                                for FW2_Type in FW2_Types:
                                    TF1 = df_header.Measurement_Type == Measurement_Type
                                    TF2 = df_header.FW2 == FW2_Type
                                    TF = TF1 & TF2
                                    if sum(TF) !=0: # if a combination of measurement type and FW2 position is not empty, then we will write it to an spe file
                                        if (FW2_Type == 2) | (FW2_Type == 5): # note, Filter wheel #2 index = 2 or 5 used U340 filter. This might be changed, so, verify this information from Pandora OF file!
                                            seperation_label = Measurement_Type.replace(' ','_') + '_U340_' # again, FW2 = 2 or 5 used U340! 
                                        else:
                                            seperation_label = Measurement_Type.replace(' ','_') + '_OPEN_' # this means no U340 used, but a ND or diffuser might be!
                                        print('     writting ' + seperation_label + ' type file ... ')    
                                        # get header part of one type of measurement
                                        df_header_subset = df_header[df_header.Measurement_Type == Measurement_Type][df_header.FW2 == FW2_Type]
                                        # get spectrum part of one type of measurement
                                        df_spec_subset = df_spec[df_header.Measurement_Type == Measurement_Type][df_header.FW2 == FW2_Type]
                                        # reset subsets' index
                                        df_header_subset.reset_index(drop=True,inplace = True)
                                        df_spec_subset.reset_index(drop=True,inplace = True)
                                        # give the subset a unique name
                                        file_name_subset = seperation_label + file_name
                                        # write the subset to spe file
                                        QDOAS_ASCII_formater_write(df_header_subset,df_spec_subset,file_name_subset, instrument_no, location, lat, lon, alt)
                            del df_header, df_spec
                        del df, location, lat, lon, alt 
                    
                    ### if we process PanPS lev2 data ###
                    else:
                        df, instrument_no_infile, location, lat, lon, alt = read_PanPS_lev2(full_file_name) # read L1 file
                        # check if we have same instrument number as indicated 
                        if instrument_no_infile != instrument_no: 
                            print('     Warning, instrument number found in L1 file does not match with input value! Will record the true value found in L1 file into spe file. ')
                            instrument_no = instrument_no_infile  
                           
                        height, width = df.shape
                        if height == 0: # check if the L1 file is "empty"
                            print('     an empty lev2 file, escape from reformat ... ')
                        else: 
                            print('     prepare header of the spe file ... ')
                            df_header = QDOAS_ASCII_formater_header(df,process_PanPS_lev2) # prepare header part of the spe file
                            print('     prepare spectrum of the spe file ... ')
                            df_spec = df.iloc[:,53:2101] # prepare spectrum  part of the spe file, note here the spec is scaled value!
                            print('     writting to QDOAS spe file ... ')
                            
                            # speration of modes
                            Measurement_Types = pd.unique(df_header.Measurement_Type)
                            FW1_Types = pd.unique(df_header.FW1)
                            #FW2_Types = pd.unique(df_header.FW2)
                            # loop over all measurement types found in this lev2 file
                            for Measurement_Type in Measurement_Types:   
                                # loop over all Filter wheel #1 positions found in this lev2 file
                                for FW1_Type in FW1_Types:
                                    TF1 = df_header.Measurement_Type == Measurement_Type
                                    TF2 = df_header.FW1 == FW1_Type
                                    TF = TF1 & TF2
                                    if sum(TF) !=0: # if a combination of measurement type and FW1 position is not empty, then we will write it to an spe file
                                        if (FW1_Type == 3) | (FW1_Type == 5): # note, Filter wheel #1 index = 3 or 5 used U340 filter. This might be changed, so, verify this information from Pandora OF file!
                                            seperation_label = Measurement_Type.replace(' ','_') + '_U340_' # again, FW1 = 3 or 5 used U340! 
                                        elif (FW1_Type == 4) : # note, Filter wheel #1 index = 4 used BP300 filter. 
                                            seperation_label = Measurement_Type.replace(' ','_') + '_BP300_' 
                                        else:
                                            seperation_label = Measurement_Type.replace(' ','_') + '_OPEN_' # this means no U340 used, but a ND or diffuser might be!
                                        print('     writting ' + seperation_label + ' type file ... ')    
                                        # get header part of one type of measurement
                                        df_header_subset = df_header[df_header.Measurement_Type == Measurement_Type][df_header.FW1 == FW1_Type]
                                        # get spectrum part of one type of measurement
                                        df_spec_subset = df_spec[df_header.Measurement_Type == Measurement_Type][df_header.FW1 == FW1_Type]
                                        # reset subsets' index
                                        df_header_subset.reset_index(drop=True,inplace = True)
                                        df_spec_subset.reset_index(drop=True,inplace = True)
                                        # give the subset a unique name
                                        file_name_subset = seperation_label + file_name
                                        # write the subset to spe file
                                        QDOAS_ASCII_formater_write(df_header_subset,df_spec_subset,file_name_subset, instrument_no, location, lat, lon, alt)
                            del df_header, df_spec
                        del df, location, lat, lon, alt 


                
                    #no_ZS = check_ZS_modes(full_file_name, df)
                    #total_ZS += no_ZS
                
                

#print(str(total_ZS))
