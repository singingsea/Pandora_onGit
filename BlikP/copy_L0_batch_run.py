# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 10:29:48 2017

@author: ZhaoX

This code will copy Pandora L0 data from PanPS L1 folder to BlickP L0 folder
"""
# now lets' find the weekday of today, and perform sechdualed step 0
# please note, the L0 file we will copy is the files will be processed "today", so we need use "auto_processing_schedual_step1", and make sure this "copy_L0_batch_run" will be performed before step 1
from datetime import datetime, timedelta
from  auto_processing_schedual import auto_processing_schedual_step1, datetime_weekday
weekday_of_today = datetime_weekday[str(datetime.today().weekday())]
instrument_no = auto_processing_schedual_step1[weekday_of_today][-3:] # find which instrument will be processed for this day

L0_source_filepath =  '\\\\wdow05dtmibroh\\GDrive\\Pandora\\' + instrument_no + '\\L1\\' # use Pandora L0 data folder! Note: currently our BlickP type L0 data are saved in PanPS L1 folder!
BlickP_L0_path = '\\\\wdow05dtmibroh\\GDrive\\Pandora\\'  + instrument_no + '\\Blick\\L0\\'

import os
import shutil
src_files = os.listdir(L0_source_filepath)
for file_name in src_files:
    full_file_name = os.path.join(L0_source_filepath, file_name)
    if (os.path.isfile(full_file_name)): # only copy files
        if (full_file_name.find('Pandora' + instrument_no) != -1) & (full_file_name.find('L0.txt') != -1): # only copy files that have name "PandoraXXX" end "L0.txt"
            if not os.path.exists(os.path.join(BlickP_L0_path, file_name)): # check if the file has already existed in BlickP L0 foler
                if not os.path.getsize(full_file_name) == 0: # only copy non-zero size L0 file
                    shutil.copy(full_file_name, BlickP_L0_path)