# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)
"""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson
import pandas as pd
import dam_wind
import seaborn as sns


def plot_counts(year_st, year_en, years, counts, name='BERMUDA'):
    """
    This function is used for plotting the time series of annual number of 
    storms that came within 185km of Bermuda
    :param: years: array/list with the years
    :param: counts: array/list with the annual counts of storms
    :param: name: name of location (used for title and for saving)
    :param: year_st: beginning of the period
    :param: year_en: end of the period
    """
    
    plt.figure(figsize=(8,6))
    plt.plot(years, counts)
    plt.xlabel('Years')
    plt.ylabel('Counts')
    plt.title('Number of storms within \n 185km from %s' %name, fontsize=14)
    plt.xticks(np.arange(year_st, year_en+2, 20))
    plt.yticks(np.arange(0, max(counts)+1,1))
    plt.xlim(year_st, year_en+2)
    plt.ylim(0)
    plt.savefig('DATA/%s/PLOTS/Counts.png' %name, bbox_inches='tight')
    plt.show()
    
    return

def plot_counts_moving_mean(name):
    
    infile = 'DATA/%s/185KM/Counts.csv' %name # BDA time series

    # EXTRACTING DATA 
    data = pd.read_csv(infile, usecols=(0,1), header=None) # BDA
    
    # CALCULATING MEAN
    mu = np.mean(data[1])
    
    # CALCULATING CENTRED 10-YEAR MOVING AVERAGES
    ma_10 = data[1].rolling(window=10, center=True).mean()

    # CALCULATING MEAN OF THE 10-YEAR MOVING AVERAGES
    ma_10_m = np.nanmean(ma_10)
    
    # PLOTTING THE TIME SERIES (ts), THE MEAN (m), MEAN +- STD (std), THE 10-YEAR 
    # MOVING AVERAGE (10), MEAN OF 10-YEAR MOVING AVERAGE (m10), MEAN +- STD (std10)
    # OF MOVING AVERAGE
    # LINE PLot for BDA
    plt.figure(figsize=(8,6))
    plt.plot(data[0], data[1], label = 'All TCs mean= %s' %round(mu,2)) # ts
    plt.plot(data[0], ma_10, 'r', label='10yr mean') # 10
    plt.axhline(ma_10_m, c='r', linestyle='--', label='$\mu_{10}$= %.2f' %ma_10_m) # m10
    plt.legend(loc=1, ncol=2)
    plt.xlabel('Years')
    plt.ylabel('Counts')
    plt.title('Bermuda')
    plt.xlim(data[0][data.index[0]]-1, data[0][data.index[-1]]+1)
    if (data[0][data.index[-1]]- data[0][data.index[0]]) > 30:
        plt.xticks((np.arange(data[0][data.index[0]], data[0][data.index[-1]]+2, 20)))
    else:
        plt.xticks((np.arange(data[0][data.index[0]], data[0][data.index[-1]]+2, 5)))
    plt.yticks((np.arange(min(data[1]), max(data[1])+2, 1)))
    plt.ylim(0)
    plt.savefig('DATA/%s/PLOTS/Counts_moving10.png' %name, bbox_inches='tight')
    #plt.grid()
    plt.show()
    
    return



def plot_gen(sim_ev, phase, name='BERMUDA'):
    """
    This function is used for generating a graph of the time series of new 
    simulated events for the scenario we want to check.
    
    :param: sim_ev: the time series of new simulated events for the scenario
            phase: string indicating the type of scenario
            name: string of the name of the place relevant to the study
    """
    
    size = np.size(sim_ev)
    
    # Plotting new generated time series
    plt.figure(figsize=(12,4))
    plt.plot(sim_ev)
    plt.xlabel('Years')
    plt.ylabel('Count of events')
    plt.title('Simulated events per year')
    plt.xlim(-1, size+1)
    plt.ylim(0)
    plt.savefig("DATA/%s/PLOTS/Sim_events%s_phase.png" %(name, phase), bbox_inches='tight')
    plt.show()
    
    return
    

def plot_ts_bar(years, counts, mu, phase, name='BERMUDA'):
    """
    This function is used for generating a graphs for the scenario we want to
    check: The part of the original time series of TC counts we want to check,
            along with the average annual number of TCs for the scenario we 
            want to check.
    :param: years: the years of the part of the original time series we want to check
            counts: the counts of the part of the original time series we want to check
            mu: average annual number of TCs for the scenario we want to check
            phase: string indicating the type of scenario
            name: string of the name of the place relevant to the study
    """
    
    # Plotting time series for Bermuda with mean
    fig, ax = plt.subplots(figsize=(8,6))
    ax.bar(years, counts, edgecolor='k', label='Mean= %s' %round(mu,2), color='k', alpha=0.5)
    plt.legend()
    ax.set_yticks(np.arange(0, max(counts)+1,1))
    ax.set_xlabel('Years')
    ax.set_ylabel('Counts')
    ax.set_title('Time series for Bermuda')#: %s - %s' %(str(years[0]), str(years[-1])))
    
    
    if type(years) == np.ndarray:
        if years[-1] - years[0] >30:
            ax.set_xticks(np.arange(years[0], years[-1]+1, 20))
        else:
            ax.set_xticks(np.arange(years[0], years[-1]+1, 2))
        plt.savefig("DATA/%s/PLOTS/TS_BDA%s_phase_%s_%s.png" %(name, phase,
                                years[0],
                                years[-1]), bbox_inches='tight')
    else:
        if (years[years.index[-1]] - years[years.index[0]]) > 30:
            ax.set_xticks(np.arange(years[years.index[0]], years[years.index[-1]]+1, 20))
        else:
            ax.set_xticks(np.arange(years[years.index[0]], years[years.index[-1]]+1, 2))
        plt.savefig("DATA/%s/PLOTS/TS_BDA%s_phase_%s_%s.png" %(name, phase,
                                years[years.index[0]],
                                years[years.index[-1]]), bbox_inches='tight')
   
    plt.show()
    
    return
    
    
def plot_Poisson(x, mu, phase, year_l, year_u, name='BERMUDA'):
    """
    This function is used for generating a graphs for the scenario we want to
    check: The part of the original time series of TC counts we want to check,
            along with the average annual number of TCs for the scenario we 
            want to check.
    :param: mu: average annual number of TCs for the scenario we want to check
            x: array of potential numbers of hurricanes per year based on mu 
            phase: string indicating the type of scenario
            name: string of the name of the place relevant to the study
    """
    
    # Plotting the Poisson rate of probabilities
    fig, ax = plt.subplots(1, 1, figsize=(6,4))
    ax.plot(x, poisson.pmf(x, mu), 'bo', ms=8, label='poisson pmf')
    ax.plot(x, poisson.pmf(x, mu))
    ax.vlines(x, 0, poisson.pmf(x, mu), colors='b', lw=5, alpha=0.5)
    plt.xlabel('Number of events')
    plt.ylabel('Probability')
    plt.title('Poisson Rate Probability of \n Numbers of Hurricanes')
    plt.savefig("DATA/%s/PLOTS/Poisson%s_phase_%s_%s.png" %(name, phase,
                                                            year_l, year_u), 
                bbox_inches='tight')
    plt.show()

    return


def plot_dam_wind():
    """
    This function is used for plotting the wind-damage relationship and fitting
    the Miller et al., 2013 figure 12 data. THe wind-damage relationship
    is given by the damage index, f. 
    """
    
    # Reading the Miller data
    infile = 'DATA/Miller.csv' 
    data = np.genfromtxt(infile, delimiter=',', skip_header=1)
    
    x = data[:,0]
    y = data[:,1]

    # Array for wind speeds.
    w_test = np.arange(35, 95.1, 0.1)
    
    # Plotting the 
    plt.figure()
    plt.plot(w_test, dam_wind.wind_dam_curve(w_test, v_half=77, v_thresh = 37.5)*100,
             label='V_half = 77 $ms^{-1}$')
    plt.plot(w_test, dam_wind.wind_dam_curve(w_test, v_half=85, v_thresh = 37.5)*100,
             label='V_half = 85 $ms^{-1}$')
    plt.plot(w_test, dam_wind.wind_dam_curve(w_test, v_half=95, v_thresh = 37.5)*100, 
             'm', label='V_half = 95 $ms^{-1}$')
    plt.plot(x,y, 'o', c='k')
    plt.legend()
    plt.xlabel(r"Wind speed ($ms^{-1}$)")
    plt.ylabel('Damage ratio (%)')
#    plt.ylim(-0.5, 30.15)
    plt.xlim(30, 95)
    plt.grid()
    plt.savefig("DATA/BERMUDA/PLOTS/Wind_dam_Eman.png", bbox_inches='tight')
    plt.show()
    
    return


def plot_distance_windspeed(distance, fit_curve, windspeed, coefficients,
                            name='BERMUDA'):
    """
    This function is used for plotting the relationship between the distance 
    of a storm from the location and the estimated windspeed at the location.
    The function plots the actual data in dots with a fitted logarithmic 
    curve as caclulated by the dist_wind_curve in the dist_wind.py script.
    :param: distance: array containing the distance of each point from Bermuda
            fit_curve: array containing the fitted curve
            windspeed: array of estimated wind speed at Bermuda
            coefficient: the coefficients of the fitted curve (used for the title)
            name: string of the name of the place relevant to the study
    
    """
    
    # PLOTTING THE DATA AND THE FITTED CURVE
    plt.figure(figsize=(8,4))
    plt.plot(distance, fit_curve, label="Fitted Curve") 
    plt.scatter(distance, windspeed, c='orange', label = 'Obs')
    plt.legend(loc='upper right')
    plt.ylabel('Estimated wind speed \n at BDA (m/s)')
    plt.xlabel('Distance from BDA (km)')
    plt.xlim([distance[0]-1, distance[-1] + 1 ])
    tex = '%s %s*log(x)' % (round(coefficients[0],2), round(coefficients[1],2))
    plt.title('f(x)= %s' %(tex),fontsize=16)
    plt.savefig('DATA/%s/PLOTS/Wind_dist.png' %name, bbox_inches='tight')
    plt.show()
    
    
#    fig, ax = plt.subplots()
#    sns.kdeplot(windspeed, color='r')
#    ax2 = ax.twinx()
#    ax2.hist(windspeed, edgecolor='r')
#    plt.xlabel('Wind speed at BDA (m/s)')
#    plt.ylabel('Frequency')
#    plt.title('Distribution of \n wind speeds at Bermuda')
##    plt.savefig()
#    plt.show()
#    
#    
#    plt.figure()
#    sns.kdeplot(windspeed, color='r')
#    plt.hist(windspeed, normed=True, edgecolor='r')
#    plt.xlabel('Wind speed at BDA (m/s)')
#    plt.ylabel('Frequency')
#    plt.title('Normalilsed distribution of \n wind speeds at Bermuda')
##    plt.savefig()
#    plt.show()
    
    return
