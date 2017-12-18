# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 15:20:02 2017

@author: ZhaoX
"""

# this is for setting schedual for run BlickP.exe, more details can be found in auto_BlickP_precess.py, 
auto_processing_schedual_step1 = {
        'Monday': 'Pandora108', 
        'Tuesday': 'Pandora104', 
        'Wednesday':'Pandora108' ,
        'Thursday':'Pandora109' ,
        'Friday':'Pandora122' ,
        'Saturday':'Pandora123' 
        }

# this is for setting schedual for reformat BlickP L2 data and making daily plots
# more details can be found in BlickP_L2_batch_run.py and BlickP_daily_VCD_plot_batch_run.py
auto_processing_schedual_step2 = {
        'Monday': 'Pandora108', 
        'Tuesday': 'Pandora103', 
        'Wednesday':'Pandora104' ,
        'Thursday':'Pandora108' ,
        'Friday':'Pandora109' ,
        'Saturday':'Pandora122' ,
        'Sunday' : 'Pandora123',
        }

# python datetime weekday --> Monday is 0, Tuesday is 1
# Do NOT change this "datetime_weekday" dict! Unless you know what you want to do for sure!
# for changing scheduals, you only need modify "auto_processing_schedual_step1" and "auto_processing_schedual_step2"
datetime_weekday = {
        '0' : 'Monday', 
        '1' : 'Tuesday', 
        '2' : 'Wednesday',
        '3' : 'Thursday' ,
        '4' : 'Friday' ,
        '5' : 'Saturday',
        '6' : 'Sunday'
        }