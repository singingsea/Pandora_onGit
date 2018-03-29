# -*- coding: utf-8 -*-
"""
Created on Wed Oct 25 14:02:25 2017

@author: ZhaoX
"""

# rcode in this list can be ploted by "plot_BlickP_L2", if a new rcode is used in retrieval, please add its name here and also relative information (eg. target trace gas column number) to "plot_BlickP_L2"
retrieval_rcodes = ['rout0' , 'rnvs0', 'rfus0', 'rsut2','rnvsa']
# about rcodes represent: [direct-sun o3, direct-sun no2, direct-sun hcho, direct-sun so2, direct-moon no2]

retrieval_trace_gas = {
                    'O3' : 'rout0',
                    'NO2' : 'rnvs0',
                    'HCHO' : 'rfus0',
                    'SO2' : 'rsut2',
                    'NO2_moon' : 'rnvsa'
                       }