# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)

This is a script is used for: 
    1) finding relationships between the distance of a storm track point from 
        Bermuda and the wind speed at Bermuda
    2) finding relationships between the wind speed at Bermuda and the damage 
        ratio from a study about Hurricane Fabian (2003) by Miller et al., 2013
    3) Generating events for a number of years based on the Poisson 
        distribution, generating random distances for each event, calculating 
        the wind speeds at Bermuda based in the relationship found in 1, then
        calculating the damage ration based on the relationship found in 2
        and lastly calculating the losses based on the ARV data.
       
"""

from __future__ import division
import numpy as np
from scipy.stats import poisson
#import matplotlib.pyplot as plt
import random
#import arv as arv
import dist_wind as dist_wind
import dam_wind as dam_wind
import pandas as pd
#import plotting
   

def calculations(sim_ev, sum_arv, name='BERMUDA'):
    """
    This fuction is used for randomly generating distancesand for calculating
    wind speeds, damage ratios and losses for the each new simulated event 
    using the time series of new events, the distance-intensity and intensity-
    damage (vulnerability) functions and the ARV data.
    :param: sim_ev: time series of new events
            sum_arv: sum of the ARV data
    :return: dist: 2D-array containing the distance for each new event
             wind: 2D-array containing the wind speed for each new event
             dam: 2D-array containing the damage ratio for each new event
             loss: 2D-array containing the loss for each new event
    """
    # Getting the function for the relation between distance and wind speed
    dist_wind_fun = dist_wind.dist_wind_curve(name)  
    

    # INITIALISING 2D-ARRAYS FOR THE GENERATION OF RANDOM DISTANCES,
    # AND FOR CALCULATIONS OF WIND SPEEDS, DAMAGE RATIOS & LOSSES
    # The initialised arrays do not contain any numbers. They are full of np.nan 
    # The first column for each array indicates the year.
    size = np.size(sim_ev)
    dist = np.full((size, max(sim_ev)+1), np.nan)
    dist[:,0] = np.arange(1,size+1)
    
    wind = np.full((size, max(sim_ev)+1), np.nan)
    wind[:,0] = np.arange(1,size+1)
    
    dam = np.full((size, max(sim_ev)+1), np.nan)
    dam[:,0] = np.arange(1,size+1)
    
    loss = np.full((size, max(sim_ev)+1), np.nan)
    loss[:,0] = np.arange(1,size+1)
    
    # Generating distances, wind speeds, damage ratios and losses
    for i in xrange(len(sim_ev)):  # for each year
        for j in xrange(1, sim_ev[i]+1):  # for every event of the given year
            d = random.randint(0,185)  # generating random distance between 0 and 185km
            dist[i, j] = d   # saving the distance value for the event 
        
            if d == 0:       # if the distance is equal to 0 
                w = dist_wind_fun[0]  # then we take the wind to be the intercept
            else:            # otherwise it is calculated from the
                w = dist_wind_fun[0] + dist_wind_fun[1]*np.log(d)  # function of the fitted curve
            wind[i, j] = w  # saving the wind value for the event
            
            
            # Finding damage with damage index
            
            dam[i,j] = dam_wind.wind_dam_curve(wind[i,j])
            loss[i,j] = dam[i,j]*sum_arv
            
    
    return dist, wind, dam, loss


def write_files(sim_ev, quantity, q_name, country, des, par, year_st, year_en):
    """
    This function is used for writting files containing the data for distance,
    wind speed, damage ratio and loss for the new simulated events. 
    :param: sim_ev: time series of new simulated events
            quantity: the quantity we want to write files for (distance / 
                    wind speed / damage ratio / loss )
            q_name: the name of the quantity: 'dist' / 'wind' / 'dam' / loss' /
                    'loss_high' - for a high-frequency scenario / 'loss_low' - 
                    for a low-frequency scenario
            country: name of the country/area we are interested in - for the 
                     purpose of saving the files 
            des: description of property.
            par: name of parish
            year_st: first year
            year_en: last year
    """
    bol = False
    
    # If the quantity we want to save is the loss, then we need another column
    # for summing up the losses at each year. 
    if q_name == 'loss' or q_name == 'loss_high' or q_name == 'loss_low':
        bol = True
        SUM_ARV = np.full(len(sim_ev), np.nan) # initialising array for the sum of losses
    
        for p in xrange(len(SUM_ARV)):
            SUM_ARV[p] = np.nansum(quantity[p,1:]) # summing
        
    # Opening a csv file
    file = open("DATA/%s/GEN_DATA/New_dataset_%s_%s_%s_%s_%s.csv" % 
                (country, q_name, des, par, year_st, year_en), 'w')  
    # Writing the headings e.g. YEAR, EVENT 1, EVENT 2, EVENT 3, etc
    file.write('YEAR,')
    for k in xrange(max(sim_ev)):
        file.write('EVENT %s,' %(k+1))
    
    if bol: # If the quantity we want to write is loss, then we add another 
        file.write('SUM,')  # column heading for summing up the losses
    
    file.write('\n')  # changing line
    
    # Writing the quantity 
    for i in xrange(len(sim_ev)):
        for j in xrange(max(sim_ev)+1):
            file.write('%s,' %quantity[i,j])
        if bol: # If the quantity we want to write is loss, then we also write 
            file.write('%s,' %SUM_ARV[i])  # the aggregated losses in a year
        file.write('\n')  # changing line
    file.close()
       
    return

def get_phase_mu(year_l, year_u):
    """
    This function is used for getting the data for the part of the time series 
    (mean, years, counts) for the scenario (high/low -frequency) we want to check. 
    :param: year_l: first year
            year_u: last year
    :return: phase_mu: mean of the part of time seris we select
             phase_years: years for the part of time series we select
             phase_counts: TC counts for the part of time series we select
    """
    # Reading the time series of counts we created
    infile = "DATA/BERMUDA/185KM/Counts.csv" 
    data = pd.read_csv(infile, usecols=(0,1), header=None)
    
    # Selecting the years and counts we want by finding the indices.
    # Finding the indices
    ind_s = data[data[0][:]==year_l].index.item()
    ind_e = data[data[0][:]==year_u].index.item()
    # Selecting years and counts
    phase_years = data[0][ind_s:ind_e+1]
    phase_counts = data[1][ind_s:ind_e+1]
    
    phase_mu = np.mean(phase_counts) # calculating the mean
		
    return phase_mu, phase_years, phase_counts


	
def poisson_and_sim_events(mu, size=10000):
    """
    This function is used for calculating the Poisson probabilities and for 
    randomnly generating new events from the Poisson distribution for a 
    number of years for the scenario we want to check.
    :param: mu: the average annual number of storms for the scenario
            size: the number of years
    :return: sim_ev: the time series of new simulated events 
             x: array of potential numbers of hurricanes per year based on the 
                 mu
    """
    # Getting the Poisson probabilities
    # Array of potential numbers of hurricanes per year
    x = np.arange(poisson.ppf(0.01, mu), poisson.ppf(0.99, mu)*2)  
    # Probability of each of x occuring 
    prob = poisson.cdf(x, mu)   

    # Checking accuracy of cdf and ppf
    print(np.allclose(x, poisson.ppf(prob, mu))) # must be True

    # GENERATING RANDOM NUMBERS FROM THE POISSON DISTRIBUTION 
    # size = 10000  # choosing how many years of events we want
    sim_ev = poisson.rvs(mu, size=size) # getting the random numbers

    return  sim_ev, x 
