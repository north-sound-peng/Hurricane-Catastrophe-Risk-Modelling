# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 14:14:44 2019

@author: hr892185
"""
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def get_EP(name, q_name, des, par, year_st, year_en):
    """
    This function is used for getting and plotting the Exceedance Probability 
    (EP) curve of aggregated annual losses from damaging-only events.
    :param: name: name of the location 
    :param: q_name: name of quantity we want (loss / loss_high / loss_low)
    :param: des: description of property.
    :param: par: desired parish
    :param: year_st: beginning of period
    :param: year_en: end of period  
    ref for EP curve: https://matplotlib.org/gallery/statistics/histogram_cumulative.html
    (need to find a better example)
    """
    
    # Reading loss data
    infile = 'DATA/%s/GEN_DATA/New_dataset_%s_%s_%s_%s_%s.csv' % (
            name, q_name, des, par, str(year_st), str(year_en)) 
    # Extracting the data - only the aggregated losses
    data = np.genfromtxt(infile, delimiter=",", usecols=-2, skip_header=1) 
    
    # Sorting the data from high to low loss, multiplying by 50 so that the 
    # values are closest to actual losses
    sort_sum = sorted(data*50, reverse=True) 
    
    
    SORT = [] # Initialising list for saving the losses that were not 0
    count = 0 # Initialising counter if the user wants to know how many years had no losses
    for i in xrange(len(sort_sum)):
        if sort_sum[i] == 0.:
            count = count + 1
        else:
            SORT.append(sort_sum[i]/1e9) # dividing by one billion
        sort_sum[i] = sort_sum[i]/1e9
        

    n_bins = 1000

    mu_nz = np.mean(SORT)
    sigma_nz = np.std(SORT)
    
       
    ######
    # Plotting the empirical cumulative distribution function (CDF) the
    # Sample. Also showing the theoretical CDF.
    # Normalised histogram
    fig, ax1 = plt.subplots(1, 1, figsize=(8,4))
    n, bins, patches = ax1.hist(SORT, bins=n_bins, density=True, 
                           cumulative=True, label='Empirical', 
                           edgecolor=None)  
    
    # Add a line showing the expected distribution.
    y = ((1 / (np.sqrt(2 * np.pi) * sigma_nz)) *
         np.exp(-0.5 * (1 / sigma_nz * (bins - mu_nz))**2))
    y = y.cumsum()
    y /= y[-1]
    
    ax1.plot(bins, y, 'r--', linewidth=1.5, label='Theoretical')
    ax1.legend()
    ax1.set_ylabel('Likelihood of occurrence (%)')
    ax1.set_yticklabels(np.arange(0, 101, 20)) # manually setting the ticks
    
    
    
    plt.figure(figsize=(8,4))
    plt.hist(SORT, bins=n_bins, density=True, cumulative=-1, label='Empirical Rev.',
            edgecolor=None)
    
    plt.plot(bins, 1-y, 'k--', linewidth=1.5, label='Theoretical Rev.')
    plt.xlim(0)
    plt.legend()
    plt.grid()    
    title = '%s phase: %s - %s \n description: %s - parish: %s' %(
            'No', year_st, year_en, des, par)
#    plt.suptitle(title)
    plt.xlabel('Loss ($bn)')
    plt.ylabel('Annual Exceedance \n Probability')
    plt.savefig('DATA/%s/PLOTS/EP_%s_%s_%s_%s_%s.png' %(name,
            des, par, q_name[5:], year_st, year_en), bbox_inches='tight')
    plt.show()
    
    
    # Save the EP curves into files.
    nn = (1-n) # getting the reversed empirical values
    z = (1-y)  # getting the reversed theoretical values 
        
    REV_EMP_EP = []
    REV_EMP_RP = []
    REV_THE_EP =[]
    REV_THE_RP = []
    
    for i in range(len(nn)):
        REV_EMP_EP.append(nn[i]*100)
        REV_EMP_RP.append(1./nn[i]) # reversed empirical return periods
        REV_THE_EP.append(z[i]*100)
        REV_THE_RP.append(1./(z[i])) # reversed theoretical return periods
        
    
    file = open('DATA/%s/GEN_DATA/EP_%s_%s_%s_%s_%s.csv' % (name, q_name,
             des, par, str(year_st), str(year_en)), 'w')
    file.write('REV EMP EP (%),')
    file.write('REV EMP RP,')
    file.write('REV THE EP (%),')
    file.write('REV THE RP,')
    file.write('LOSS ($BN)')
    file.write('\n')
    for i in range(len(nn)):
        file.write("%s," %REV_EMP_EP[i])
        file.write("%s," %REV_EMP_RP[i])
        file.write("%s," %REV_THE_EP[i])
        file.write("%s," %REV_THE_RP[i])
        file.write("%s" %bins[i])
        file.write("\n")
    file.close()
            
    return