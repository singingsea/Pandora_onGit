# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 12:09:14 2017

@author: ZhaoX
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 09:33:10 2017

@author: ZhaoX
"""
f#rom IPython import get_ipython ## house keeping, first two lines to clear workspace
#get_ipython().magic('reset -sf') 

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import dateutil.parser
import numpy as np

#%%
def load_files(mypath):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    onlytxtfiles = []
    for f in onlyfiles:
        if f.find('.txt') != -1:
            onlytxtfiles.append(f)
    return onlytxtfiles

#%%
def read_BlickP_L2(file_nm):
    
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
    return df

#%%
def plot_BlickP_L2(df,file_nm):
    # L2 data quality flag for fitted gas : 0=high quality, 1=medium quality, 2=low quality 
    L2_QF = 0 
    
    if file_nm.find('rout0') != -1:
        df = df[:][df['Column 11: L2 data quality flag for ozone: 0=high quality, 1=medium quality, 2=low quality'] <= L2_QF]
        y = df['Column 8: Ozone total vertical column amount [Dobson Units], -9e99=retrieval not successful']
        y_rms = df['Column 21: Normalized rms of spectral fitting residuals weighted with measured uncertainty, -9=fitting not successful or no uncertainty given']
        ylabel_1 = 'Ozone'
    elif file_nm.find('rnvs0') != -1:
        df = df[:][df['Column 11: L2 data quality flag for nitrogen dioxide: 0=high quality, 1=medium quality, 2=low quality'] <= L2_QF]
        y = df['Column 8: Nitrogen dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful']
        y_rms = df['Column 15: Normalized rms of spectral fitting residuals weighted with measured uncertainty, -9=fitting not successful or no uncertainty given']
        ylabel_1 = 'NO2'
    elif file_nm.find('rfus0') != -1:
        df = df[:][df['Column 11: L2 data quality flag for formaldehyde: 0=high quality, 1=medium quality, 2=low quality'] <= L2_QF]
        y_rms = df['Column 15: Normalized rms of spectral fitting residuals weighted with measured uncertainty, -9=fitting not successful or no uncertainty given']
        y = df['Column 8: Formaldehyde total vertical column amount [Dobson Units], -9e99=retrieval not successful']
        ylabel_1 = 'HCHO'
    elif file_nm.find('rsut1') != -1:
        df = df[:][df['Column 17: L2 data quality flag for sulfur dioxide: 0=high quality, 1=medium quality, 2=low quality'] <= L2_QF]
        y = df['Column 14: Sulfur dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful']
        y_rms = df['Column 21: Normalized rms of spectral fitting residuals weighted with measured uncertainty, -9=fitting not successful or no uncertainty given']
        ylabel_1 = 'SO2'
    elif file_nm.find('rsut2') != -1:
        df = df[:][df['Column 17: L2 data quality flag for sulfur dioxide: 0=high quality, 1=medium quality, 2=low quality'] <= L2_QF]
        y = df['Column 14: Sulfur dioxide total vertical column amount [Dobson Units], -9e99=retrieval not successful']
        y_rms = df['Column 21: Normalized rms of spectral fitting residuals weighted with measured uncertainty, -9=fitting not successful or no uncertainty given']
        ylabel_1 = 'SO2'
        
    x = list(map(dateutil.parser.parse, df['Column 1: UT date and time for center of measurement, yyyymmddThhmmssZ (ISO 8601)']))
    
    font = {'family' : 'DejaVu Sans', 'weight' : 'bold', 'size'   : 12}
    plt.rc('font', **font)
    fig = plt.figure(figsize=(22, 18), dpi=200, facecolor='w', edgecolor='k') 
    
    gs = gridspec.GridSpec(2, 2, height_ratios=[3, 1], width_ratios=[3, 1]) 
    
    ax0 = plt.subplot(gs[0])
    ax0.plot(x, y,'r.', label = 'VCD')
    ax0.grid()
    ax0.set_ylabel(ylabel_1 + ' VCD [DU]')
    ax0.set_xlabel('Time')
    ax0.legend()
    ax0.set_title(file_nm)
    ax0.legend(['L2 data : quality flag <= ' + str(L2_QF)])
    
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
    plt.savefig(file_nm[0:-4] + '.png')
    #plt.show()
    plt.close()

#%%

# [add site name to this list, otherwise the code will try to interprete the site name from file name (may give wrong site name!)
#sites_list = {'Downsview': 'America/Toronto', 'FortMcKay': 'America/Edmonton', 'StGeorge':'America/Toronto'}
from sites_list import sites_list
# rcode in this list can be ploted by "plot_BlickP_L2", if a new rcode is used in retrieval, please add its name here and also relative information (eg. target trace gas column number) to "plot_BlickP_L2"
#retrieval_rcodes = ['rout0' , 'rnvs0', 'rfus0', 'rsut1', 'rsut2']
from rcodes_list import retrieval_rcodes
from instruments_list import instruments_list

for instrument_no in instruments_list.values():
    filepath =  ['\\\\wdow05dtmibroh\\GDrive\\Pandora\\' + instrument_no + '\\Blick\\L2\\'] # Pandora108 Ozone, NO2 data on Brewer server
        
    plotpath = filepath
    shelve_filename = filepath + 'Blick_L2' + '.out' 
    
    
    
    onlytxtfiles = load_files(filepath)
    for file_nm in onlytxtfiles:
        # read in data as dataframe
        print('\n \n ')
        print('Read in data from file : \n' + filepath + file_nm)
        df = read_BlickP_L2(filepath + file_nm)       
        
        # add instrument name
        print('Add instrument name to dataframe')
        df['instrument'] = file_nm[file_nm.rfind('Pandora'):file_nm.find('Pandora') + len('Pandora')+3]
        
        # add location
        print('Add location info. to dataframe')
        site_found = False
        for site in sites_list.keys():
            if file_nm.find(site) != -1:
                df['location'] = site
                site_found = True
                location = site
        if site_found == False:
            try:
                new_location = file_nm[file_nm.find('_')+1:file_nm.find('_L2')]
                df['location'] = new_location
                print('\n')
                print('-------- Warnning: -----------')
                print('A new measurement location (not in measurement location lists) is found: "' + new_location + '"')
                print('IF this is a new site, please add this location to site list in future.')
                print('------------------- \n')
            except:
                df['location'] = 'UnKnown'
                print('\n')
                print('-------- Warnning: -----------')
                print('The measurement location is not recognized, please check and add new location info.')
                print('------------------- \n')
     
        # add timestamp
        print('Convert ISO 8601 time to Python-dateutil datetime')
        df['time'] = list(map(dateutil.parser.parse, df['Column 1: UT date and time for center of measurement, yyyymmddThhmmssZ (ISO 8601)']))
        # add UTC and LTC
        print('Add UTC column to dataframe')              
        df['UTC'] = df.time.dt.tz_convert('UTC')
        if location in sites_list.keys():
            print('Add LTC column to dataframe')              
            df['LTC'] = df.time.dt.tz_convert(sites_list[location])
        else:
           print('\n')
           print('-------- Warnning: -----------')
           print('Do not know timezone for the new measurement location (not in measurement location lists) : "' + new_location + '"')
           print('No local time (LTC) column created for this site.')
           print('------------------- \n')
            
     
        rcode_found = False      
        for retrieval_rcode in  retrieval_rcodes:
            if file_nm.find(retrieval_rcode) != -1:
                #exec(file_nm[0:-6] + '= df')
                print('Plotting data (retrieved by rcode: ' + retrieval_rcode +') ... ')
                plot_BlickP_L2(df,filepath + file_nm)
                rcode_found = True
        if rcode_found == False:
            print('\n')
            print('-------- Warnning: -----------')
            print('An L2 file was not identified: "' + file_nm + '"')
            print('This file is not ploted (but dataframe will be saved).Please check output format and add information about this file (eg. target trace gas column number) to  function "plot_BlickP_L2". ')
            print('------------------- \n')
            
        
        exec(file_nm[0:-6] + '= df')# rename dataframe
    
    # save data
    print('\nSave dataframes:')
    import shelve    
    my_shelf = shelve.open(shelve_filename,'n') # 'n' for new
    for key in dir():     
        if key.find('Pandora') != -1:
            try:
                my_shelf[key] = globals()[key]
                print(key + ' saved as dataframe! ')
            except TypeError:
                print('ERROR shelving: {0}'.format(key))
    my_shelf.close()
    
    # reload data
    my_shelf = shelve.open(shelve_filename)
    for key in my_shelf:
        globals()[key]=my_shelf[key]
    my_shelf.close()
