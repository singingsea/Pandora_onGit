# -*- coding: utf-8 -*-
"""
Created on Fri Mar  9 13:54:46 2018

@author: xiaoy
"""

from IPython import get_ipython ## house keeping, first two lines to clear workspace
get_ipython().magic('reset -sf') 

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import dateutil.parser
import numpy as np

#%%
def load_files(): # will only load QDOAS .dat file
    from os import listdir
    from os.path import isfile, join
    
    onlyfiles = [f for f in listdir(filepath) if isfile(join(filepath, f))]
    onlytxtfiles = []
    for f in onlyfiles:
        if f.find('.dat') != -1:
            onlytxtfiles.append(f)
    return onlytxtfiles

#%%
def read_QDOAS(file_nm):
    
    f = open(file_nm,'r')
    f.close()           
                          
    df_QDOAS = pd.read_csv(file_nm, sep='\t', header=1, skiprows= 0, parse_dates = [[8, 9]])# read in data use Pandas frame
    #df = df.replace([-9e99],np.NaN)
    
    return df_QDOAS

#%%

#file_nm = 'E:\Projects\Zenith_NO2\QDOAS_outputs\\Pandora103_NDACC_O3_NO2.dat'
file_nm = 'C:\Projects\Zenith_NO2\QDOAS_outputs\\Pandora103_NDACC_O3_NO2_ref20160619.dat'
#outputpath = 'E:\Projects\Zenith_NO2\QDOAS_outputs\\'
outputpath = 'C:\Projects\Zenith_NO2\QDOAS_outputs\\'
location = 'Toronto'
shelve_filename = outputpath + 'QDOAS_outputs_ref20160619' + '.out'

df_QDOAS = read_QDOAS(file_nm)


# save data to shelve
import shelve
my_shelf = shelve.open(shelve_filename,'n') # 'n' for new
print(dir())
for key in dir():
    print(key)
    if key.find('df_QDOAS') != -1:
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

