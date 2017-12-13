# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 15:20:02 2017

@author: ZhaoX
"""

# 
auto_processing_schedual_step1 = {
        'Monday': 'Pandora103', 
        'Tuesday': 'Pandora104', 
        'Wednesday':'Pandora108' ,
        'Thursday':'Pandora109' ,
        'Friday':'Pandora122' ,
        'Saturday':'Pandora123' 
        }

# 
auto_processing_schedual_step2 = {
        'Tuesday': 'Pandora103', 
        'Wednesday':'Pandora104' ,
        'Thursday':'Pandora108' ,
        'Friday':'Pandora109' ,
        'Saturday':'Pandora122' ,
        'Sunday' : 'Pandora123',
        }

# python datetime weekday --> Monday is 0, Tuesday is 1

datetime_weekday = {
        '0' : 'Monday', 
        '1' : 'Tuesday', 
        '2' : 'Wednesday',
        '3' : 'Thursday' ,
        '4' : 'Friday' ,
        '5' : 'Saturday',
        '6' : 'Sunday'
        }