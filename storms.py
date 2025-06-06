# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)

Script that checks if any TC track points are within a certain distance from
a specific location. 
"""

from __future__ import division
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import geog
import shapely.geometry
import read_data as re_da
import extract as extr


def storms(year_st, year_en, lat=32.36, lon=-64.68, meters=185., 
           name='BERMUDA'):
    """
    Given latitude and longitude coordinates as well as a "radius" around 
    the latitude and longitude coordinates, this functions checks all the 
    points for all the storms for all the years in the historical record 
    IBTrACS. For example, if a point was within 185km of Bermuda, the point and its 
    intensity are saved. There is one file per year. 
    :param: year_st: beginning of the period
    :param: year_en: end of the period
    :param lat: latitude coordinate for location
    :param lon: longitude coordinate for location
    :param name: name of location for saving purposes
    :param meters: radius around location
    """
    x1 = lat # latitude of BDA's airport
    if lon >0:
        y1 = lon
    else:
        y1 = 360. + lon # longitude of BDA's airport
    r = 6371*1000 # Earth's radius 

    p = shapely.geometry.Point([y1, x1])  # making the lat and lon into a point

    # Creating a polygon around the location
    n_points = 100 # with 100 points
    dist = 1000 * meters  # meters, 185km = 100nm 
    angles = np.linspace(0, 360, n_points)
    polygon = geog.propagate(p, angles, dist)
    POL = shapely.geometry.Polygon(polygon)

   
    flag = 'W'

    for it in xrange(year_st, year_en+1):
        
        data = re_da.read_NH(it, flag)  # reading data
        num_storms, max_num, num_track, lons, lats, inten, \
            track_id, time = extr.extract(data)  # extracting data
    
        # CREATING FILES FOR EACH YEAR
        # SAVING THE POINTS THAT CAME WITHING 185KM OF BDA
        file = open("DATA/%s/185KM/%s.csv" %(name, str(it)), 'w')  
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
        for j in xrange(num_storms):
            for i in xrange(max_num):
                # combining lon and lat coordinates into a point
                poin = shapely.geometry.Point([lons[i,j], lats[i,j]])  
            
                # Cheacking wheather the polygon contains the point of the storm
                # Also, the intensity must be a valid value
                # The intensity is in m/s
                # According to the intensity, a value of Rmax is assigned
                if POL.contains(poin) and inten[i,j]<1e25:# and inten[i,j]>33:
                    if inten[i,j] <= 17:
                        rmax = 200*1000
                    elif inten[i,j] > 17 and inten[i,j] <=32:
                        rmax = 125*1000
                    elif inten[i,j] > 32 and inten[i,j] <=42:
                        rmax = 95*1000
                    elif inten[i,j] > 42 and inten[i,j] <=49:
                        rmax = 50*1000
                    elif inten[i,j] > 49 and inten[i,j] <=58:
                        rmax = 30*1000
                    elif inten[i,j] > 58 and inten[i,j] <=70:
                        rmax = 25*1000
                    elif inten[i,j] > 70 :
                        rmax = 20*1000
    
                    # FOR DISTANCE OF THE POINT IN THE POLYGON FROM BERMUDA
                    dlon = abs(radians(y1) - radians(lons[i,j])) # difference in lon
                    dlat = abs(radians(x1) - radians(lats[i,j])) # difference in lat
                    
                    # The Haversine formula
                    a = sin(dlat / 2)**2 + cos(radians(lats[i,j])) * cos(
                            radians(x1)) * sin(dlon / 2)**2
                    c = 2 * atan2(sqrt(a), sqrt(1 - a))

                    dist = r*c # The distane between the point the Bermuda

                    # Calculating the wind at Bermuda using the Rankine vortex
                    if dist > rmax:
                        v_ber = (inten[i,j])*((rmax/dist)**(0.5))
                        
                    else:
                        v_ber = inten[i,j]
                        
                
                    # Saving the information for each point
                    file.write('%s,' %track_id[j])
                    file.write('%s,' %time[i,j])
                    file.write('%s,' %lons[i,j])
                    file.write('%s,' %lats[i,j])
                    file.write('%s,' %(round((inten[i,j]),2))) 
#                    file.write('%s,' %(round((inten[i,j]*1.13),2))) # Converting from 10-min to 1-min 
                    file.write('%s,' %y1)
                    file.write('%s,' %x1)
                    file.write('%s,' %(round(rmax/1000,2))) # writing rmax in km
                    file.write('%s,' %(round(dist/1000,2))) # writing dist in km
                    file.write('%s' %(round(v_ber,2)))
                    file.write('\n')
        file.close()
 
    return   

#storms()  