# -*- coding: utf-8 -*-
"""
Created on Thu Aug 22 10:14:45 2019

@author: dell
"""

import numpy as np
import matplotlib.pyplot as plt


def read_extract(infile):
    
    
    data = np.genfromtxt(infile, delimiter=",", usecols=-2, skip_header=1)
    
    sort_sum = sorted(data*50, reverse=True)
    
    no_zeros = []
            
    count = 0

    for i in xrange(len(sort_sum)):
        if sort_sum[i] == 0.:
            count = count + 1
        else:
            no_zeros.append(sort_sum[i]/1e9)
        sort_sum[i] = sort_sum[i]/1e9
    
   
    mu_nz = np.mean(no_zeros)
    sigma_nz = np.std(no_zeros)
    
    return no_zeros, mu_nz, sigma_nz


def plot_EP_curve(no_zeros, num_bins, mu, sigma, year_s, year_e, des, par, 
                  phase):
    
    fig, ax = plt.subplots(figsize=(8, 4))
    # plot the cumulative histogram
    n, bins, patches = ax.hist(no_zeros, num_bins,                                density=True, 
                                 cumulative=-1, label='Reversed emp.', 
                                 edgecolor='b', 
                                 histtype='step')    
    # Add a line showing the expected distribution.
    y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
         np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
    y = y.cumsum()
    y /= y[-1]
    
    theor = 1-y
    
    ax.plot(bins, theor, 'k--', linewidth=1.5, label='Theoretical')
    ax.legend(loc=0)
#    ax.set_xlim(0,12)
    plt.grid()
    ax.set_xlabel('Loss Amount ($bn)')
    ax.set_ylabel('Annual Exceedance Probability')
    title = '%s phase: %s - %s' %(phase, year_s, year_e)
    plt.title('%s \n Description: %s \n Parish: %s' %(
            title, des, par))
#    plt.savefig('G:\INTERNSHIP\DATA\BERMUDA\GEN_DATA\EP_%s_%s.pdf' %(
#            year_s, year_e), bbox_inches='tight')
    plt.show()

    return bins, theor, n



des = 'ALL'
par = 'ALL'


infile1 = 'DATA/BERMUDA/GEN_DATA/New_dataset_loss%s_%s_%s_%s_%s.csv' %(
            '',  des, par, 1958, 2017)

infile1_h1 = 'DATA/BERMUDA/GEN_DATA/New_dataset_loss%s_%s_%s_%s_%s.csv' %(
            '_high',  des, par, 2005, 2017)
    
infile1_l1 = 'DATA/BERMUDA/GEN_DATA/New_dataset_loss%s_%s_%s_%s_%s.csv' %(
            '_low',  des, par, 1960, 1975)


loss_n1,mu_n1, sigma_n1 = read_extract(infile1)
loss_h_1_o, mu_h_1_o, sigma_h_1_o = read_extract(infile1_h1)
loss_l_1_o, mu_l_1_o, sigma_l_1_o = read_extract(infile1_l1)


n_bins = 1000 
bins_no1, theor_no1, n_no1 = plot_EP_curve(loss_n1, n_bins, mu_n1, sigma_n1, 1958, 2017, 
                                  des, par, 'No_o')

bins_h_1_o, theor_h_1_o, n_h1_o = plot_EP_curve(loss_h_1_o, n_bins, mu_h_1_o, sigma_h_1_o, 2005, 
                                    2017, des, par, 'High')

bins_l_1_o, theor_l_1_o, n_l1_o = plot_EP_curve(loss_l_1_o, n_bins, mu_l_1_o, sigma_l_1_o, 1960, 
                                    1975, des, par, 'Low')


plt.figure()
plt.plot(bins_no1, theor_no1, 'k', linewidth=1.5, label='%s' %('No: 1958 - 2017'))
plt.plot(bins_h_1_o, theor_h_1_o, 'r', linewidth=1.5, label='%s' %('H: 2005 - 2017'))
plt.plot(bins_l_1_o, theor_l_1_o, 'g', linewidth=1.5, label='%s' %('L: 1960 - 1975'))
plt.legend(loc=0)
#plt.xlim(0, 6)
plt.ylim(0.0, 1)
plt.grid()
plt.ylabel('Annual Exceedance \n Probability')
plt.xlabel('Loss Amount ($bn)')
plt.savefig('DATA\BERMUDA\PLOTS\EP_all.png', bbox_inches='tight')
plt.show()