# -*- coding: utf-8 -*-
"""
Created on Tue Sep 26 13:53:49 2017

@author: ZhaoX
"""

def linear_fit(x,y,location):
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.stats import linregress
    #location = 'FortMcKay'
    
    font = {'family' : 'normal', 'weight' : 'bold', 'size'   : 12}
    plt.rc('font', **font)
    plt.figure(num=None, figsize=(10, 10), dpi=200, facecolor='w', edgecolor='k')
    
    
    plt.scatter(x,y)
    fit = np.polyfit(x,y,1)
    fit_fn = np.poly1d(fit) 
    # fit_fn is now a function which takes in x and returns an estimate for y
    plt.plot(x,y, 'k.', x, fit_fn(x), '--r')
    details = linregress(x,y)
    
    
    plt.xlabel('BlickP ozone [DU]')
    plt.xlim([200,500])
    plt.ylabel('PanPS ozone [DU]')
    plt.ylim([200,500])
    plt.grid()
    plt.title('Pandora108 @' + location)
    plt.text(250,450,'y = ' + str(details.slope) + 'x + ' + str(details.intercept) )
    plt.text(250,400,'R = ' + str(details.rvalue))
    plt.savefig( 'Blick_vs_Pan_summarynew_O3_scatter_' + location + '.png')
    plt.show()
    print(details)
    return details
 #%%
details = linear_fit(Ozone_Blick_Pan_Downsview['ozone_Blick'],Ozone_Blick_Pan_Downsview['ozone_Pan'],'Downsview')
#linear_fit(data['ycolumn1'],data['ycolumn2'],'FortMcKay')