# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)

This script is used for getting a relationship between distance of a storm 
from Bermuda and wind speed estimate at Bermuda using two functions. 
"""

from __future__ import division
import numpy as np
#import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import plotting


def dist_wind(x, a, b):
    """
    This function returns a logarithmic curve.
    """
    return a+b*np.log(x)

def dist_wind_curve(name='BERMUDA'):
    """
    This function is used for finding a relationship (fitting a curve) between
    distance of a storm from Bermuda and wind speed estimate at Bermuda. 
    """
    # HIGHEST WIND SPEEDS FOR THE STORMS THAT CAME WITHIN 185KM OF BERMUDA 
    infile_wind = 'DATA/%s/185KM/FINAL_f.csv' %name
    data_wind = np.genfromtxt(infile_wind, delimiter=',', skip_header=1)
    D_BDA = data_wind[:,9] # array containing the distance of each point from Bermuda
    V_BDA = data_wind[:,10] # array of estimated wind speed at Bermuda

    # SORTING THE WIND SPEED DATA IN TERMS OF DISTANCE
    yx = zip(D_BDA, V_BDA)    
    yx.sort()
    yx

    distance = [] # list for distances
    windspeed = [] # list for wind speeds
    for i in xrange(len(yx)):
		distance.append(yx[i][0])
		windspeed.append(yx[i][1])
    
	# MAKING THE CURVE FOR THE RELATION BETWEEN DISTANCE AND WIND SPEED   
    # fitting a logarithmic curve (getting the coefficients
    popt, pcov = curve_fit(dist_wind, distance, windspeed) 
    
    # Using the relationship calculated above, for each element in the
    # array of distances caclulate the wind speed.
    fitted = dist_wind(distance, *popt)
    
    # Plotting the fitted curve agains the actual data
    plotting.plot_distance_windspeed(distance, fitted, windspeed, popt,
                            name='BERMUDA')
	        
    return popt
