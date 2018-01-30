# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 11:28:00 2018

@author: ZhaoX
"""

# this function is intent to reformat BlickP processed L1 data to QDOAS readable files

import pandas as pd
instrument_no = 123

L1_file_path = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\'  + str(instrument_no) + '\\Blick\\L1\\'



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
def check_ZS_modes(full_file_name):
   df = read_BlickP_L1(full_file_name)
   df_sp = df[['Column 1: Two letter code of measurement routine','Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)']]
   df_sp['datetime'] = pd.to_datetime(df_sp['Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)'])
   TF = (df_sp['Column 1: Two letter code of measurement routine'] == 'ZO') | (df_sp['Column 1: Two letter code of measurement routine'] == 'ZU')
   no_ZS = sum(TF)
   return no_ZS
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
                no_ZS = check_ZS_modes(full_file_name)
                total_ZS += no_ZS
                
                print(str(idx/len(src_files)*100))
print(str(total_ZS))
