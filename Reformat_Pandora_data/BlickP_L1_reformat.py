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
instrument_no = 108
location = 'Downsview'
lat = 43.7810
lon = -79.4680
alt = 187
L1_file_path = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\'  + str(instrument_no) + '\\Blick\\L1\\'
spe_file_path = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\'  + str(instrument_no) + '\\Blick\\spe\\'


sites_list_LTC = {'Downsview': 'America/Toronto', 'FortMcKay': 'America/Edmonton', 'StGeorge':'America/Toronto'}
sites_list_LSC = {'Downsview': 'EST', 'FortMcKay': 'MST', 'StGeorge':'EST'}
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




#%%
def read_BlickP_L1(file_nm):
    
    f = open(file_nm,'r')
    header_part_ind = 0 # use the '----' symble as header identification
    No_header_lines = 0
    column_names = []
    read_column_names = False
    while header_part_ind != 2: # the data part start after read in '----' twice
        header = f.readline() # read in a line of the file
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
    return df

#%%
def check_ZS_modes(full_file_name, df):
   df_sp = df[['Column 1: Two letter code of measurement routine','Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)']]
   df_sp['datetime'] = pd.to_datetime(df_sp['Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)'])
   TF = (df_sp['Column 1: Two letter code of measurement routine'] == 'ZO') | (df_sp['Column 1: Two letter code of measurement routine'] == 'ZU')
   no_ZS = sum(TF)
   return no_ZS

#%% 
def QDOAS_ASCII_formater_header(df):
        df_sp = df[['Column 1: Two letter code of measurement routine',
                'Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)',
                'Column 6: Total duration of measurement set in seconds',
                'Column 7: Data processing type index',
                'Column 8: Integration time [ms]',
                'Column 14: Pointing zenith angle in degree, absolute or relative (see next column), 999=tracker not used',
                'Column 15: Zenith pointing mode: zenith angle is... 0=absolute, 1=relative to sun, 2=relative to moon',
                'Column 16: Pointing azimuth in degree, increases clockwise, absolute (0=north) or relative (see next column), 999=tracker not used',
                'Column 17: Azimuth pointing mode: like zenith angle mode but also fixed scattering angles relative to sun (3) or moon (4)',
                'Column 61: Scale factor for data, to obtain unscaled output divide data by this number',
                'Column 63: Level 1 data type, data are... 1=corrected count rate [s-1], 2=radiance [W/m2/nm/sr], 3=irradiance [W/m2/nm]'
                ]]

        df_sp['datetime'] = pd.to_datetime(df_sp['Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)'], utc = True)
        

        # add timestamp
        print('Convert ISO 8601 time to Python-dateutil datetime')
        df_sp['time'] = list(map(dateutil.parser.parse, df_sp['Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)']))
        # add UTC and LTC
        print('Add UTC column to dataframe')              
        df_sp['UTC'] = df_sp.time.dt.tz_convert('UTC')
        if location in sites_list_LSC.keys():
            #print('Add LTC column to dataframe')              
            #df_sp['LTC'] = df_sp.time.dt.tz_convert(sites_list_LTC[location])
            print('Add LSC column to dataframe')              
            df_sp['LSC'] = df_sp.time.dt.tz_convert(sites_list_LSC[location])
       
        # calcuate SZA
        print('Add SZA and SAA column to dataframe')  
        df_sp['SZA'] = '' 
        df_sp['SAA'] = '' 
        for i in range(len(df_sp)):
            SZA = 90 - get_altitude(lat, lon, df_sp.LSC[i])
            df_sp.SZA[i] = SZA
            SAA = get_azimuth(lat, lon, df_sp.LSC[i])
            df_sp.SAA[i] = SAA
        
        df_output = pd.DataFrame()
        df_output['UTC'] = df_sp.UTC
        df_output['Date'] = df_output.UTC.dt.strftime('%d/%m/%Y')
        df_output['time'] = df_output.UTC.dt.strftime('%H:%M:%S')
        df_output['Exposure'] = df_sp['Column 8: Integration time [ms]']/1000 # QDOAS need exposure time in sec
        df_output['Total_Measurement_Time'] = df_sp['Column 6: Total duration of measurement set in seconds']
        df_output['SZA'] = df_sp.SZA # solar zenith angle [deg]
        df_output['SAA'] = df_sp.SAA # solar azimuth angle [deg]
        df_output['VAA'] = '' # viewing azimuth angle angle [deg]
        df_output['VEA'] = ''# viewing elevation angle angle [deg]
        df_output['fd'] = ''
        df_output['Scale_factor'] = df_sp['Column 61: Scale factor for data, to obtain unscaled output divide data by this number']
        
        # make measurement type column
        df_output['Measurement_Type_Index'] = df_sp['Column 7: Data processing type index'] # this is Pandora L1 data type, 2 = direct-sun, 3 = direct-moon, 4 = zenith-sky, 6 = profile, 7 = almucantar
        df_output['Measurement_Type'] = ''
        for i in range(len(df_sp)):
            df_output.Measurement_Type[i] = Measurement_Type_Index_dict[df_output.Measurement_Type_Index[i]]
            
        # make elevation viewing angle column
        for i in range(len(df_sp)):
            if df_sp['Column 15: Zenith pointing mode: zenith angle is... 0=absolute, 1=relative to sun, 2=relative to moon'][i] == 0:
                df_output.VEA[i] = 90 - df_sp['Column 14: Pointing zenith angle in degree, absolute or relative (see next column), 999=tracker not used'][i]
            elif df_sp['Column 15: Zenith pointing mode: zenith angle is... 0=absolute, 1=relative to sun, 2=relative to moon'][i] == 1:
                df_output.VEA[i] = 90 - df_sp.SZA[i] - df_sp['Column 14: Pointing zenith angle in degree, absolute or relative (see next column), 999=tracker not used'][i]
            elif df_sp['Column 15: Zenith pointing mode: zenith angle is... 0=absolute, 1=relative to sun, 2=relative to moon'][i] == 2:
                print('Warning: we do not calcualte moon location!')  
                df_output.VEA[i] = 'NaN'
        # make azimuth viewing angle column        
        for i in range(len(df_sp)):
            if df_sp['Column 17: Azimuth pointing mode: like zenith angle mode but also fixed scattering angles relative to sun (3) or moon (4)'][i] == 0:
                df_output.VAA[i] = df_sp['Column 16: Pointing azimuth in degree, increases clockwise, absolute (0=north) or relative (see next column), 999=tracker not used'][i]
            elif df_sp['Column 17: Azimuth pointing mode: like zenith angle mode but also fixed scattering angles relative to sun (3) or moon (4)'][i] == 1:
                df_output.VAA[i] = df_sp.SAA[i] - df_sp['Column 16: Pointing azimuth in degree, increases clockwise, absolute (0=north) or relative (see next column), 999=tracker not used'][i]
            elif df_sp['Column 17: Azimuth pointing mode: like zenith angle mode but also fixed scattering angles relative to sun (3) or moon (4)'][i] == 2:
                print('Warning: we do not calcualte moon location!')  
                df_output.VAA[i] = 'NaN'     
        
        # make fractional day column
        #for i in range(len(df_sp)):
        #    hh = df_sp['UTC'][i].hour
        #    mm = df_sp['UTC'][i].minute
        #    ss = df_sp['UTC'][i].second
        #    df_output.fd[i] = float(pd.datetime.strftime(df_sp.LSC[i],'%j')) -1 + hh/24 + mm/24/60 + ss/24/60/60
            
        return df_output    
#%%
def QDOAS_ASCII_formater_write(df_header,df_spec,file_name):
    spefilename = spe_file_path + file_name[:-4] + '.spe'
    with open(spefilename, 'w') as f:
        
        f.write('# Station = ' + location + '(lat ' + str(lat) + ' , lon ' + str(lon) + ')' + '\n')
        f.write('# Institute = Environment and Climate Change Canada' + '\n')
        f.write('# PI name = Vitali Fioletov (vitali.fioletov@canada.ca)' + '\n')
        f.write('# Instrument = Pandora ' + str(instrument_no) + '\n')
        f.write('# Size of the detector = 2048 (the size of the detector as indication)' + '\n')
        f.write('# Total number of records = ' + str(len(df_header)) + '\n')
        
        for i in range(len(df_header)):
            f.write('Date(DD/MM/YYY) = ' + str(df_header.Date[i]) + '\n')
            #f.write('UTC Time (hh:mm:ss) = ' + str(df_header.time[i]) + '\n')
            f.write('UTC Start Time (hh:mm:ss) = ' + str(df_header.time[i]) + '\n')

            f.write('Viewing Elevation Angle (deg) = ' + str(df_header.VEA[i]) + '\n') 
            f.write('Viewing Azimuth Angle (deg) = ' + str(df_header.VAA[i]) + '\n')
            f.write('Measurement Type (OFFAXIS/DIRECT SUN/ALMUCANTAR/ZENITH) = ' + df_header.Measurement_Type[i] + '\n')
            f.write('Total Measurement Time (sec) = ' + str(df_header.Total_Measurement_Time[i]) + '\n')
            
            f.write('Exposure Time(sec) = ' + str(df_header.Exposure[i]) + '\n')
            f.write('Solar Zenith Angle (deg) = ' + str(df_header.SZA[i]) + '\n')
            f.write('Solar Azimuth Angle (deg) = ' + str(df_header.SAA[i])  + ' (North=0, East=90)' + '\n')
            
            height, width = df_spec.shape
            for j in range(width):
                spec = df_spec.iloc[i,:]/df_header.Scale_factor[i]
                f.write('\t' + str(spec[j]) + '\n')
#%%
import os
import shutil
total_ZS = 0
src_files = os.listdir(str(L1_file_path))
for idx, file_name in enumerate(src_files):
    full_file_name = os.path.join(L1_file_path, file_name) # creat full file name (including path)
    if (os.path.isfile(full_file_name)): # only get files
        if (full_file_name.find('Pandora' + str(instrument_no)) != -1) & (full_file_name.find('L1') != -1): # only get files that have name "PandoraXXX" and "L1"
            if not os.path.getsize(full_file_name) == 0: # only copy non-zero size L0 file
                print(' >>> Formating ' + file_name + '[' +str(idx/len(src_files)*100) + ']')
                print('     read BlickP L1 file ... ')
                df = read_BlickP_L1(full_file_name)
                print('     prepare header of the spe file ... ')
                df_header = QDOAS_ASCII_formater_header(df)
                print('     prepare spectrum of the spe file ... ')
                df_spec = df.iloc[:,63:2111]
                print('     writting to QDOAS spe file ... ')
                QDOAS_ASCII_formater_write(df_header,df_spec,file_name)
                
                #no_ZS = check_ZS_modes(full_file_name, df)
                #total_ZS += no_ZS
                
                

#print(str(total_ZS))
