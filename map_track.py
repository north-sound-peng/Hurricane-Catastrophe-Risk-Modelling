# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)

This scriptis used for plotting the tracks of storms that passed within a 
certain distance from a specific location.
"""

import numpy as np
import geog
import shapely.geometry
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.path import Path
import matplotlib.patches as patches
import read_data as re_da
import extract as extr


def storms_in_pol_map(year_st, year_en, lat=32.36, lon=-64.68, 
                      meters=185., name='BERMUDA'):
    """
    Given latitude and longitude coordinates as well as a "radius" around the
    latitude and longitude coordinates, this function plots the tracks of 
    storms that passed within a distance from the location.
    :param year_st: start of the period 
    :param year_en: end of the period
    :param lat: latitude coordinate for location
    :param lon: longitude coordinate for location
    :param name: name of location for saving purposes
    :param meters: radius around location
    """

    #25.761681, -80.191788 MIAMI
    #29.951065, -90.071533 # New Orleans
       
    x1 = lat # latitude of location
    if lon >0:
        y1 = lon
    else:
        y1 = 360. + lon # longitude of location
    
    # making the lat and lon coordinates of the location into a point
    p = shapely.geometry.Point([y1, x1]) 

    # Creating a polygon around the location
    n_points = 100 # with 100 points
    d = meters * 1000  # meters, 185km = 100nm 
    angles = np.linspace(0, 360, n_points)
    polygon = geog.propagate(p, angles, d)
    POL = shapely.geometry.Polygon(polygon)

    # Lower and upper bounds for latitude and longitude used for the map
    llon = round(y1 - 10.) # lower bound for lon
    ulon = round(y1 + 10.) # upper bound for lon
    llat = round(x1 - 10.) # lower bound for lat
    ulat = round(x1 + 10.) # upper bound for lat
    
    # Plotting the map
    font = {'weight' : 'normal', 'size': 16}
    plt.rc('font', **font)
    
    fig = plt.figure(figsize=(18, 18))     
    ax = fig.add_subplot(111)
    plt.subplots_adjust(bottom=0.6) 
    m = Basemap(llcrnrlat=llat, urcrnrlat=ulat, llcrnrlon=llon, urcrnrlon=ulon)
    m.drawparallels(np.arange(llat, ulat, 5.), labels=[0, 1, 0, 0])
    m.drawcoastlines(color='grey')
    m.drawcountries()
    m.drawmeridians(np.arange(llon, ulon, 5.), labels=[0, 0, 0, 1])
    plt.plot(polygon[:,0], polygon[:,1], 'k', linewidth=3)
    plt.plot(y1,x1,'k+',ms=20, mew=3)


    flag = 'W'  # indicating that the intensity is in terms of wind-speed    
    
    for it in xrange(year_st, year_en+1):
    
        data = re_da.read_obs_NH(it, flag)  # reading data
        num_storms, max_num, num_track, lons, lats, inten, \
                track_ids, time = extr.extract(data) # extracting data    
    
        # Plotting the track points using the paths package
        # We need to check the points
        for j in xrange(0, num_storms):
            for i in xrange(0, max_num-1):
                # making lat and lon coordinates into a point
                poin = shapely.geometry.Point([lons[i,j], lats[i,j]])
        
                if POL.contains(poin): # Checking if the polygon contains the point
            
            # In case the track needs to separate in the two sides of the map
            # we use a white line to connect the points
                    if (lons[i,j]>340 and lons[i,j]<360 and lons[i+1,j]>0 and lons[i+1,j]<20):
                        verts = [(lons[i,j], lats[i,j]), (lons[i+1,j], lats[i+1,j])]
                        codes = [Path.MOVETO, Path.LINETO]
                        path = Path(verts, codes)
                        patch = patches.PathPatch(path, color='white', lw=1, alpha=0.2)
                        ax.add_patch(patch)
            # In case the track needs to separate in the two sides of the map
            # we use a white line to connect the points
                    elif (lons[i,j]>0 and lons[i,j]<20 and lons[i+1,j]>340 and lons[i+1,j]<360):
                        verts = [(lons[i,j], lats[i,j]), (lons[i+1,j], lats[i+1,j])]
                        codes = [Path.MOVETO, Path.LINETO]
                        path = Path(verts, codes)
                        patch = patches.PathPatch(path, color='white', lw=1, alpha=0.2)
                        ax.add_patch(patch)
                # Otherwise we use a black line
                    else:
                        verts = [(lons[i,j], lats[i,j]), (lons[i+1,j], lats[i+1,j])]
                        codes = [Path.MOVETO, Path.LINETO]
                        path = Path(verts, codes)
                        patch = patches.PathPatch(path, color='black', lw=1, alpha=0.2)
                        ax.add_patch(patch)
                    m.scatter(lons[:,j],lats[:,j],s=15,c=inten[:,j], cmap='viridis') # showing intensity
                    m.plot(lons[0, j], lats[0, j], "+",  ms=8, markeredgewidth=2 ,color='red') # location of genesis
    m.plot(lons[0, 0], lats[0, 0], "+", label='Cyclogenesis', ms=8, 
           markeredgewidth=2 ,color='red')   # location of genesis for the 1st point
    clb = plt.colorbar(aspect=70, orientation = 'vertical',fraction=0.05)
    clb.set_label('Wind speed (m$s^{-1}$)', fontsize=16)
    #clb.set_title('Intensity')#('Power')
    plt.xlabel('\n \n Longitude',fontsize=16)
    plt.ylabel('\n Latitude',fontsize=16)
    plt.title('%s' %name)
    legend_properties = {'weight':'bold'}
    plt.legend(loc='lower right',prop=legend_properties)
    plt.savefig('DATA\%s\PLOTS\%s_tracks.png' %(name, name), bbox_inches='tight')
    plt.show()

    return

#storms_in_pol_map(29.951065, -90.071533, 'New Orleans')