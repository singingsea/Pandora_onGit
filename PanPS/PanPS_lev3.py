# -*- coding: utf-8 -*-
"""
Created on Wed Oct  4 10:14:19 2017

@author: ZhaoX
"""
from IPython import get_ipython ## house keeping, first two lines to clear workspace
get_ipython().magic('reset -sf') 

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import dateutil.parser
import numpy as np

#%%
def load_files(): # will only load lev3.txt file
    from os import listdir
    from os.path import isfile, join
    
    onlyfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
    onlytxtfiles = []
    for f in onlyfiles:
        if f.find('lev3.txt') != -1:
            onlytxtfiles.append(f)
    return onlytxtfiles

#%%
def read_BlickP_lev3(file_nm):
    
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
    #print(No_header_lines)
    f.close()           
                          
    df = pd.read_csv(file_nm, sep='\s+', header=None, names = column_names, skiprows= No_header_lines) # read in data use Pandas frame
    #df = pd.read_csv(file_nm, sep='\s+', header=None, names = column_names, skiprows= No_header_lines, parse_dates = ['Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)']) # read in data use Pandas frame
    df = df.replace([-9e99],np.NaN)
    
    # add location
    if file_nm.find('Downsview') != -1:
        df['location'] = 'Downsview'
    elif file_nm.find('FortMcKay') != -1:
        df['location'] = 'FortMcKay'
    elif file_nm.find('StGeorge') != -1:
        df['location'] = 'StGeorge'
    elif file_nm.find('Envcanad') != -1:
        df['location'] = 'Downsview'
    else:
        df['location'] = 'UnKnown'
        
    return df


#%%

def concat_lev3():
    global filepath
    
    lev3files = load_files()
    
    first_run = True    
    i = 0
    for file_nm in lev3files:
        df_1day = read_BlickP_lev3(filepath + file_nm)
        
        # check if the file is empty
        if len(df_1day['Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)']) != 0:
            # add timestamp to the dataframe
            df_1day['time'] = list(map(dateutil.parser.parse, df_1day['Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)']))
            if first_run == True:
                df = df_1day
                first_run = False
            else:
                df= pd.concat([df, df_1day], ignore_index = True)
                
        i += 1
        
        # display progress 
        p_finished = format(i/len(lev3files)*100,'.0f')        
        s = ['%.0f' % s for s in np.linspace(5,100,20)]        
        if p_finished in s:
            print( str(p_finished) + ' % lev3 concated  ... ')


    return df
#%%
def add_datetime(df):
    
    # add timestamp
    print('Convert ISO 8601 time to Python-dateutil datetime')
    df['time'] = list(map(dateutil.parser.parse, df['Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)']))
    # add UTC and LTC
    print('Add UTC column to dataframe')              
    df['UTC'] = df.time.dt.tz_convert('UTC')
    
    # group data by measurement locations
    groups = df.groupby(['location'],as_index=False)
    first_location = True
    # for each location we will assign a local time
    for location_name, group in groups:
        # check if the location name (found from lev3 data file name) is recogonized in our site list
        if location_name in sites_list.keys():
            print('Add LTC column to dataframe [location = ' + location_name +']') 
            # add local time to a group
            #group['LTC'] = group.time.dt.tz_convert(sites_list[location_name])  
            group.loc[:,'LTC'] = group.time.dt.tz_convert(sites_list[location_name])  
            # combine the results of each group back to dataframe    
            if first_location == True:
                df_output = group
                first_location = False
            else:
                df_output = pd.concat([df_output,group])
        else:
            print('\n')
            print('-------- Warnning: -----------')
            print('Do not know timezone for the new measurement location (not in measurement location lists) : "' + location + '"')
            print('No local time (LTC) column created for this site.')
            print('------------------- \n')  
    
    return df_output

#%%
def plot_PanPS_lev3(df,gas_type):
    global filepath, plotpath
    df = df[df['Column 21: Fitting result index: 1,2=no error, >2=error'] <=2 ] # quality control
    #df_SO = df[df['Column 1: Two letter code of measurement routine'] == 'SO']
    #df_SU = df[df['Column 1: Two letter code of measurement routine'] == 'SU']
    
    if gas_type == 'SO2':
        df = df[df['Column 14: Fitting window index, unique number for each fitting window'] == 9] # fitting window selection
        df = df[df['Column 23: rms of unweighted spectral fitting residuals, negative value=fitting not successfull'] <= 0.2] # quality control
        df = df[df['Column 34: Uncertainty of sulfur dioxide slant column amount [Dobson Units], negative value=not fitted or fitting not successfull'] > 0 ] # quality control
        df = df[df.SO2_VCD >= -50] # quality control        
        df = df[df.SO2_VCD <= 50] # quality control        
        df = df[df['Column 35: Geometrical sulfur dioxide air mass factor'] <=3 ] # quality control
        y = df.SO2_VCD
        #y_rms = df['Column 24: Normalized rms of weighted spectral fitting residuals, negative value=fitting not successfull']
        y_rms = df['Column 23: rms of unweighted spectral fitting residuals, negative value=fitting not successfull']
        ylabel_1 = gas_type
    elif gas_type == 'O3':
        df = df[df['Column 14: Fitting window index, unique number for each fitting window'] == 5] # fitting window selection
        df = df[df['Column 23: rms of unweighted spectral fitting residuals, negative value=fitting not successfull'] <= 0.2] # quality control
        df = df[df['Column 28: Uncertainty of ozone slant column amount [Dobson Units], negative value=not fitted or fitting not successfull'] > 0 ] # quality control
        df = df[df.O3_VCD >= -400] # quality control        
        df = df[df.O3_VCD <= 600] # quality control
        df = df[df['Column 29: Geometrical ozone air mass factor'] <=3 ] # quality control
        y = df.O3_VCD
        #y_rms = df['Column 24: Normalized rms of weighted spectral fitting residuals, negative value=fitting not successfull']
        y_rms = df['Column 23: rms of unweighted spectral fitting residuals, negative value=fitting not successfull']
        ylabel_1 = gas_type
    elif gas_type == 'NO2':
        df = df[df['Column 14: Fitting window index, unique number for each fitting window'] == 2] # fitting window selection
        df = df[df['Column 23: rms of unweighted spectral fitting residuals, negative value=fitting not successfull'] <= 0.2] # quality control
        df = df[df['Column 31: Uncertainty of nitrogen dioxide slant column amount [Dobson Units], negative value=not fitted or fitting not successfull'] > 0 ] # quality control
        df = df[df.NO2_VCD >= -1] # quality control        
        df = df[df.NO2_VCD <= 3] # quality control
        df = df[df['Column 32: Geometrical nitrogen dioxide air mass factor'] <=3 ] # quality control
        y = df.NO2_VCD
        #y_rms = df['Column 24: Normalized rms of weighted spectral fitting residuals, negative value=fitting not successfull']
        y_rms = df['Column 23: rms of unweighted spectral fitting residuals, negative value=fitting not successfull']
        ylabel_1 = gas_type
        
    x = list(map(dateutil.parser.parse, df['Column 2: UT date and time for beginning of measurement, yyyymmddThhmmssZ (ISO 8601)']))
    
    font = {'family' : 'DejaVu Sans', 'weight' : 'bold', 'size'   : 12}
    plt.rc('font', **font)
    fig = plt.figure(figsize=(22, 18), dpi=200, facecolor='w', edgecolor='k') 
    cm = plt.cm.get_cmap('jet')
    gs = gridspec.GridSpec(2, 2, height_ratios=[3, 1], width_ratios=[3, 1]) 
    
    ax0 = plt.subplot(gs[0])
    sc = ax0.scatter(x, y, c=df['Column 6: Solar zenith angle at the center-time of the measurement in degree'], s=10, cmap=cm)
    plt.colorbar(sc).set_label('SZA')
    ax0.grid()
    ax0.set_ylabel(ylabel_1 + ' VCD [DU]')
    ax0.set_xlabel('Time')
    ax0.legend()
    ax0.set_title(filepath)
    
    ax1 = plt.subplot(gs[1])
    hist, bins = np.histogram(y, bins=50, normed=1)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    ax1.grid()
    ax1.set_ylabel('f')
    ax1.set_xlabel(ylabel_1 + ' VCD [DU]')   
        
    ax2 = plt.subplot(gs[2])    
    ax2.plot(x, y_rms,'k.', label = 'RMS')
    #sc = ax2.scatter(x, y_rms, c=df['Column 6: Solar zenith angle at the center-time of the measurement in degree'], s=10, cmap=cm)
    #plt.colorbar(sc).set_label('SZA')
    ax2.grid()
    ax2.set_ylabel('RMS')
    #ax2.set_ylim([0, 0.02])    
    ax2.set_xlabel('Time')
    ax2.legend()
    
    ax3 = plt.subplot(gs[3])    
    hist, bins = np.histogram(y_rms, bins=50, normed=1)
    width = 0.7 * (bins[1] - bins[0])
    center = (bins[:-1] + bins[1:]) / 2
    plt.bar(center, hist, align='center', width=width)
    ax3.grid()
    ax3.set_ylabel('f')
    ax3.set_xlabel('RMS')   
    
    plt.tight_layout()
    plt.savefig(plotpath +'lev3_'+ ylabel_1 + '.png')
    #plt.show()
    plt.close()


#%%
    
import sys
sys.path.insert(0, 'E:\\Pandora_onGit\\BlikP')
sys.path.insert(0, 'C:\\Users\\ZhaoX\\Documents\\GitHub\\Pandora_onGit\\BlikP')
from sites_list import sites_list    

#filepath =  '\\\\wdow05dtmibroh\\GDrive\\Pandora\\108\\L3\\' # Pandora108 data on Brewer server
#plotpath = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\108\\L3_plots\\' # Pandora108 data on Brewer server
#filepath =  '\\\\wdow05dtmibroh\\GDrive\\Pandora\\109\\L3\\' # Pandora108 data on Brewer server
#plotpath = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\109\\L3_plots\\' # Pandora108 data on Brewer server
#filepath =  '\\\\wdow05dtmibroh\\GDrive\\Pandora\\123\\L3\\' # Pandora108 data on Brewer server
#plotpath = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\123\\L3_plots\\' # Pandora108 data on Brewer server
#filepath =  'E:\\Projects\\Zenith_NO2\\Pan_level3data_V2\\' 
#plotpath = 'E:\\Projects\\Zenith_NO2\\Pan_level3data_V2_plots\\'
filepath =  'C:\\Projects\\Zenith_NO2\\Pan_level3data_P103\\' 
plotpath = 'C:\\Projects\\Zenith_NO2\\Pan_level3data_P103_plots\\'
shelve_filename = plotpath + 'lev3' + '.out'

# read in all PanPS level 3 data (daily files) and then concat them to a single dataframe
df_lev3 = concat_lev3()
# calculate O3, NO2, SO2, and HCHO VCDs
df_lev3['O3_VCD'] = df_lev3['Column 27: Ozone slant column amount [Dobson Units], -9e99=not fitted or fitting not successfull']/df_lev3['Column 29: Geometrical ozone air mass factor']
df_lev3['NO2_VCD'] = df_lev3['Column 30: Nitrogen dioxide slant column amount [Dobson Units], -9e99=not fitted or fitting not successfull']/df_lev3['Column 32: Geometrical nitrogen dioxide air mass factor']
df_lev3['SO2_VCD'] = df_lev3['Column 33: Sulfur dioxide slant column amount [Dobson Units], -9e99=not fitted or fitting not successfull']/df_lev3['Column 35: Geometrical sulfur dioxide air mass factor']
df_lev3['HCHO_VCD'] = df_lev3['Column 36: Formaldehyde slant column amount [Dobson Units], -9e99=not fitted or fitting not successfull']/df_lev3['Column 38: Geometrical formaldehyde air mass factor']
# add datetime
df_lev3 = add_datetime(df_lev3)
# plot VCD time serise
plot_PanPS_lev3(df_lev3,'SO2')
plot_PanPS_lev3(df_lev3,'O3')
plot_PanPS_lev3(df_lev3,'NO2')


# save data to shelve
import shelve
my_shelf = shelve.open(shelve_filename,'n') # 'n' for new
print(dir())
for key in dir():
    print(key)
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

