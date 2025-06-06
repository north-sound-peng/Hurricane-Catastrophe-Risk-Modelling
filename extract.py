# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: dell

This script contains a function for extracting the right data in the 
correct form.
"""

from __future__ import division
import numpy as np


def extract(data):
    """
    This function takes the data as read from the file and extracts the 
    relevant information.
    :param: data
    :return: 
        Num_storms: number of storms during the year
        max_num: maximum number of track points
        num_track: number of track points of each storm
        lons: array for longitude
        lats: array for latitude
        inten: array for intensity
        track_ids: array for track ids
        time: array for time stamps
    """
   
    Num_storms = int(float(data[0,1])) # Checking how many storms there were 
                                       # during the year
   
    track_ids = []                          # Creating an array for track ids
    num_track = []                          # Creating an array that contains
    for i in np.arange(len(data[:,0])):     # the number of track points of  
        if data[i,0] == 'POINT_NUM':        # each storm
            num_track.append(int(float(data[i,1])))
        if data[i,0] == 'TRACK_ID':
            track_ids.append(data[i,1])
            
    max_num = max(num_track)        # Finding the maximum number of track points
 
    longitude = []          # Initializing char arrays for longitude,
    latitude = []           # latitude
    intensity = []          # intensity (vorticity or pressure)
    timing = []
    for i in np.arange(len(data[:,0])): # Loop for extracting the correct data
        if data[i,0] == 'POINT_NUM':
            ind = i
            n_tr = int(float(data[i,1]))
            longitude.append(data[ind+1 : ind+1 + n_tr, 1])
            latitude.append(data[ind+1 : ind+1 + n_tr, 2])
            intensity.append(data[ind+1 : ind+1 + n_tr, 3])
            timing.append(data[ind+1 : ind+1 + n_tr, 0])
    
    lons = np.zeros((max_num, Num_storms))  # Initializing float arrays
    lats = np.zeros((max_num, Num_storms))
    inten = np.zeros((max_num, Num_storms))
    time = np.zeros((max_num, Num_storms), dtype=int)
 
    for i in np.arange(len(longitude)):    # From string to float
        for j in np.arange(len(longitude[i])):
            lons[j,i] = float(longitude[i][j]) + 0.
            lats[j,i] = float(latitude[i][j]) + 0.
            inten[j,i] = float(intensity[i][j]) + 0.
            time[j,i] = (timing[i][j])
              
    for i in xrange(0, Num_storms):     # When there are 0 or missing values
        for j in xrange(0, max_num):    # to be empty with nan            
            if j >= num_track[i]:
                lons[j,i] = 'nan'
                lats[j,i] = 'nan'
                inten[j,i] = 'nan'
#                time[j,i] = 'nan'
    
    return Num_storms, max_num, num_track, lons, lats, inten, track_ids, time