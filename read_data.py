# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)

This script contains a function in order to read the files containing the data.
"""

from __future__ import division
import numpy as np


def read_NH(year, flag):
    """
    This function is used to read the file containing the data for the 
    reanalysis for the NH.
    :param year: integer with the year
    :param flag: depending on the indicator, we choose which columns to read
        indicator:  V - Vorticity -> column 3
                    P - Pressure -> column 51
                    W - Wind speed at 10m -> column 63
                    W - Wind speed at 925hPa -> column 57               
    """
            
    infile = "DATA/JRA55/NH/Storms_%s.csv" %str(year)
    
    if flag == "W":
        data = np.genfromtxt(infile, delimiter = ",", skip_header = 2, 
                         dtype = str, usecols = (0, 1, 2, 57))
    else:
        raise TypeError("Use W (winds)")

    return data

