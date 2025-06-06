# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)
"""

from __future__ import division
import numpy as np

def count_ts(year_st, year_en, name='BERMUDA'):
    """
    This function is used to create the time series of annual TC counts. 
    Counting how many storms were in the year is performed using the track id.
    :param: year_st: beginning of the period
    :param: year_en: end of the period
    :param: name: used for reading and writting files
    :return: years: array of years
             COUNTS: list of number of storms per year
    """
    
    
    track_ids = [] # initialising list for reading track ids
    years = np.arange(year_st, year_en+1) # creating the array for the years
     
    # Getting track ids
    for it in xrange(year_st, year_en+1):   
        infile = "DATA/%s/185KM/%s.csv" %(name, str(it)) 
        data = np.genfromtxt(infile, delimiter=',', skip_header=1, dtype=float, usecols=0)
        track_ids.append(data)
      
    COUNTS =[] # initialising list for the annual counts
    for i in xrange(len(track_ids)):
        # If the size of the element of the list is equal to 0, then there were 
        # no storms during that year
        if np.size(track_ids[i]) == 0:
            count = 0
        # If the size of the element of the list is greated than 2, then there 
        # were either mutliple storms or just one storm with multiple track points
        elif np.size(track_ids[i]) >2:
            count = 1
            for j in xrange(1, np.size(track_ids[i])):
                if track_ids[i][j-1] != track_ids[i][j]:
                    count = count + 1
        # Otherwise, there was just one storm with only one track point
        else:
            count = 1
        COUNTS.append(count)
    
    # Saving the time series
    file = open("DATA/%s/185KM/Counts.csv" %name , 'w')  
    for r in xrange(len(years)):
        file.write('%s,' %years[r])
        file.write('%s,' %COUNTS[r])
        file.write("\n")
    file.close()
    
    return years, COUNTS