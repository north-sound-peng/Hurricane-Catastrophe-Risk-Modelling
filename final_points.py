# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)
"""

from __future__ import division
import numpy as np


def final_points(year_st, year_en, name='BERMUDA'):
    """"
    This function is used for creating files which contain information about 
    the track points which had the highest estimated wind speed at Bermuda for
    each storm for each year. 
    :param:
        year_st: beginning of the period
        year_en: end of the period
        name: name of location for saving purposes
    """

    for it in xrange(year_st, year_en+1):
        # Reading the file with track points of storms that passed within 185km
        # of Bermuda for each year
        infile = "DATA/%s/185KM/%s.csv" %(name, str(it))
        data = np.genfromtxt(infile, delimiter=',', skip_header=1)

        if len(data.shape) == 1: # If the file we read is empty, or if there is 
                                 # only one track point in the current year
            if len(data) == 0: # If the file we read is empty
                file = open("DATA/%s/185KM/%s_f.csv" %(name, str(it)), 'w')  
                file.write('TRACK_ID,')
                file.write('TIME,')
                file.write('LONG,')
                file.write('LAT,')
                file.write('INTEN,')
                file.write('BERM_LONG,')
                file.write('BERM_LAT,')
                file.write('Rmax,')
                file.write('DIST_BDA,')
                file.write('V_BERM')
                file.write('\n')    
            
            if len(data) != 0:  # If there is only one track point in the current 
                                # year, we take is as the point that had the 
                                # highest estimated intensity at Bermuda
                # Extracting
                track_ids = data[0]
                time = data[1]
                lon = data[2]
                lat = data[3]
                inten = data[4]
                b_lon = data[5]
                b_lat = data[6]
                rmax = data[7]
                d_bda = data[8]
                v_bda = data[9]
  
                # Writing the new file for the given year, which contains
                # information for the track point we extracted
                file = open("DATA/%s/185KM/%s_f.csv" %(name, str(it)), 'w')  
                file.write('TRACK_ID,')
                file.write('TIME,')
                file.write('LONG,')
                file.write('LAT,')
                file.write('INTEN,')
                file.write('BERM_LONG,')
                file.write('BERM_LAT,')
                file.write('Rmax,')
                file.write('DIST_BDA,')
                file.write('V_BERM')
                file.write('\n')
                file.write('%s,' %track_ids)
                file.write('%s,' %time)
                file.write('%s,' %lon)
                file.write('%s,' %lat)
                file.write('%s,' %inten)
                file.write('%s,' %b_lon)
                file.write('%s,' %b_lat)
                file.write('%s,' %rmax)
                file.write('%s,' %d_bda)
                file.write('%s,' %v_bda)
                file.write('\n')

        if len(data.shape) == 2: # If there were multiple points, either from a
                                 # single storm or multiple storms in a given year
            # Extracting
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
    
            # We need to find the track point which had the highest estimated
            # wind speed at Bermuda for each storm in the given year.
            track_id = np.append(track_ids, 0)
            time = np.append(time, 0)
            lon = np.append(lon, 0)
            lat = np.append(lat, 0)
            inten = np.append(inten, 0)
            b_lon = np.append(b_lon, 0)
            b_lat = np.append(b_lat, 0)
            rmax = np.append(rmax, 0)
            d_bda = np.append(d_bda, 0)
            v_bda = np.append(v_bda, 0)
    
            # Definining lists for saving the information for the track points
            TRACK = [] 
            TIME = []
            LONG = []
            LAT = []
            INTEN = []
            B_LON = []
            B_LAT = []
            RMAX = []
            D_BDA = []
            V_BDA = []

            for j in xrange(len(track_ids)):
                if track_id[j] != track_id[j+1]:
                    TRACK.append(track_id[track_id==track_id[j]])
                    TIME.append(time[track_id==track_id[j]])
                    LONG.append(lon[track_id==track_id[j]])
                    LAT.append(lat[track_id==track_id[j]])
                    INTEN.append(inten[track_id==track_id[j]])
                    B_LON.append(b_lon[track_id==track_id[j]])
                    B_LAT.append(b_lat[track_id==track_id[j]])
                    RMAX.append(rmax[track_id==track_id[j]])
                    D_BDA.append(d_bda[track_id==track_id[j]])
                    V_BDA.append(v_bda[track_id==track_id[j]])
    
            # Writing files
            file = open("DATA/%s/185KM/%s_f.csv" %(name, str(it)), 'w') 
            file.write('TRACK_ID,')
            file.write('TIME,')
            file.write('LONG,')
            file.write('LAT,')
            file.write('INTEN,')
            file.write('BERM_LONG,')
            file.write('BERM_LAT,')
            file.write('Rmax,')
            file.write('DIST_BDA,')
            file.write('V_BERM')
            file.write('\n')
            for i in xrange(len(TRACK)):
        
                file.write('%s,' % TRACK[i][V_BDA[i][:] == np.max(V_BDA[i])][0])
                file.write('%s,' % TIME[i][V_BDA[i][:] == np.max(V_BDA[i])][0])
                file.write('%s,' % LONG[i][V_BDA[i][:] == np.max(V_BDA[i])][0])
                file.write('%s,' % LAT[i][V_BDA[i][:] == np.max(V_BDA[i])][0])
                file.write('%s,' % INTEN[i][V_BDA[i][:] == np.max(V_BDA[i])][0])
                file.write('%s,' % B_LON[i][V_BDA[i][:] == np.max(V_BDA[i])][0])
                file.write('%s,' % B_LAT[i][V_BDA[i][:] == np.max(V_BDA[i])][0])
                file.write('%s,' % RMAX[i][V_BDA[i][:] == np.max(V_BDA[i])][0])
                file.write('%s,' % D_BDA[i][V_BDA[i][:] == np.max(V_BDA[i])][0])
                file.write('%s,' % V_BDA[i][V_BDA[i][:] == np.max(V_BDA[i])][0])
                file.write('\n')
            
    return

#final_points()