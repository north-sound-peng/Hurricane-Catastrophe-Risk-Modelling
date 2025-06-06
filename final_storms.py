# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)
"""

from __future__ import division
import numpy as np


def final_storm_file(year_st, year_en, name='BERMUDA'):
    """
    For every year there is a file named *year*_f.csv  which contains 
    information about the point of the storm that came within 185km of Bermuda
    which has the highest estimated wind speed at Bermuda. 
    This function is used to read the files for all years and save all the 
    points in a file called FINAL_f.csv.
    :param:
        year_st: beginning of the period
        year_en: end of the period
        name: name of location for saving purposes
    """
    
    YEAR = []  # Year
    TRACK = [] # Track ID of the storm
    TIME = []  # Timestamp of the point
    LONG = []  # Longitude of the point
    LAT = []   # Latitude of the point
    INTEN = [] # Intensity of the point (in m/s, 10-min)
    B_LON = [] # BDA's longitude
    B_LAT = [] # BDA's latitude
    RMAX = []  # The radius of maximum wind speed
    D_BDA = [] # Distance of the point from BDA
    V_BDA = [] # Estimated wind speed at BDA
    
    # READING THE FILES
    for it in xrange(year_st, year_en+1):
        infile = "DATA/%s/185KM/%s_f.csv" %(name, str(it))
        data = np.genfromtxt(infile, delimiter=',', skip_header=1)
        
        # There are only three cases of files:
        # 1) A file contains no points
        # 2) A file contains just 1 point for 1 storm
        # 3) A file contains multiple points:
        #    a) for just 1 storm 
        #    b) for multiple storms
        if len(data.shape) == 1:
            # For cases 1 and 2
            if len(data) != 0:
                # If there is only 1 point for just 1 storm (case 2)
                YEAR.append(it)
                TRACK.append(data[0])
                TIME.append(data[1])
                LONG.append(data[2])
                LAT.append(data[3])
                INTEN.append(data[4])
                B_LON.append(data[5])
                B_LAT.append(data[6])
                RMAX.append(data[7])
                D_BDA.append(data[8])
                V_BDA.append(data[9])
            
        if len(data.shape) == 2:
            # For case 3
            track_ids = data[:,0]
            time = data[:,1]
            lon = data[:,2]
            lat = data[:,3]
            inten = data[:,4]
            b_lon = data[:,5]
            b_lat = data[:,6]
            rmax = data[:,7]
            d_bda = data[:,8]
            v_bda = data[:,9]
        
            for i in xrange(len(track_ids)):
                YEAR.append(it)
                TRACK.append(track_ids[i])
                TIME.append(time[i])
                LONG.append(lon[i])
                LAT.append(lat[i])
                INTEN.append(inten[i])
                B_LON.append(b_lon[i])
                B_LAT.append(b_lat[i])
                RMAX.append(rmax[i])
                D_BDA.append(d_bda[i])
                V_BDA.append(v_bda[i])
    
    # WRITTING THE FINAL FILE WHICH CONTAINS THE POINT WITH THE HIGHEST
    # ESTIMATED INTENSITY AT BERMUDA FOR EACH STORM THAT CAME WITHIN 
    # 185KM OF BERMUDA
    file = open("DATA/%s/185KM/FINAL_f.csv" %name, 'w')  
    file.write('YEAR,')
    file.write('TRACK_ID,')
    file.write('TIME,')
    file.write('LONG,')
    file.write('LAT,')
    file.write('INTEN (m/s),')
    file.write('BERM_LONG,')
    file.write('BERM_LAT,')
    file.write('Rmax (km),')
    file.write('DIST_BDA (km),')
    file.write('V_BERM (m/s)')
    file.write('\n')
    for n in xrange(len(TRACK)):
        file.write('%s,' %YEAR[n])
        file.write('%s,' %TRACK[n])
        file.write('%s,' %TIME[n])
        file.write('%s,' %LONG[n])
        file.write('%s,' %LAT[n])
        file.write('%s,' %INTEN[n])
        file.write('%s,' %B_LON[n])
        file.write('%s,' %B_LAT[n])
        file.write('%s,' %RMAX[n])
        file.write('%s,' %D_BDA[n])
        file.write('%s' %V_BDA[n])
        file.write('\n')
    file.close()
    
    return

#final_storm_file()