# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)

This script is used for getting a relationship between wind speed estimate at 
Bermuda and damage ratio based on the study by Miller et al., 2013. 
"""

from __future__ import division
import numpy as np


def wind_dam_curve(wind, v_half=95, v_thresh = 37.5):
    """
    This function is used for calculating the damage index, f. 
    :param: wind: value or array of estimated wind speeds at Bermuda
            v_half: threshold at which half of the building is damaged (
            for Bermuda use 95 m/s)
            v_thresh: threshold belowe which no damaged occurs (based on 
            the Miller et al., 2013 figure 12 data, use 37.5 m/s)
    :return: f_dam: the damage index (value or array)
    
    """
    
    
    if type(wind) == list or type(wind) == np.ndarray:
        
        u = np.zeros(len(wind))
        f_dam = np.zeros(len(wind))
        
        for i in range(len(wind)):
            u[i] = max((wind[i]-v_thresh),0)/(v_half-v_thresh)

            f_dam[i] = u[i]**3/(1+u[i]**3)
    else:
        
        u = max((wind-v_thresh),0)/(v_half-v_thresh)

        f_dam = u**3/(1+u**3)
    
    
    return f_dam
