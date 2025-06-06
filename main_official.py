# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 15:14:06 2019

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)

This script serves as the main script of the model.

# IMPORTANT note
# This code is designed to give representative results ONLY for Bermuda. 
# In order to get representative results for other locations, property exposure
# and vulnerability information for those locations needs to be introduced, 
# otherwise the code will run using the information for Bermuda to give results
# for the other locations.

"""

from __future__ import division
import numpy as np
import map_track
import storms
import count_ts
import plotting
import final_storms
import final_points
import gen_dataset_new
import arv
import EP


#lat = [29.951065, 25.761681, 32.36, 35.250538, 26.633, 19.313299]
#lon = [-90.071533, -80.191788, -64.68, -75.528824, -78.417, -81.254601]
#place = ['NEW_ORLEANS', 'MIAMI', 'BERMUDA', 'N_CAROLINA', 'BAHAMAS', 'CAYMAN']

def PART_A(year_l, year_u, lat = 32.36, lon = -64.68, place = 'BERMUDA'):   
    
    
    # PART A: Creating the historical record of TCs for the location
    ################################################################
    
    # Making map with the polygon around the location and the storm tracks
#    map_track.storms_in_pol_map(year_st, year_en, lat, lon, 185., place) 
    
    # Checking which storms came within 185km of the location
    storms.storms(year_l, year_u, lat, lon, 185., place)
    
    # Creating the time series of annual numbers for the location
    years, counts = count_ts.count_ts(year_l, year_u, place)
    
    # Saving the points with the highest estimated intensity (for each storm)
    final_points.final_points(year_l, year_u, place)
    
    # Saving all the above points in one file
    final_storms.final_storm_file(year_l, year_u, place)

    # Plotting the time series of TC counts for the location
    plotting.plot_counts(year_l, year_u, years, counts, place)
    plotting.plot_counts_moving_mean(place)
    plotting.plot_ts_bar(years, counts, np.mean(counts), 
                         "_no",  name=place)
        
    return    

def PART_B(year_l, year_u, phase = '_no', place = 'BERMUDA'):
    
    # PART B: Calculating the losses
    #################################
    # Choosing the description of the property and the parish we are interested in.
    # If the user wants to choose a specific description of property and/or parish,
    # it is best they have a look at the file containing the ARV data.
    
    phase_mu, phase_years, phase_counts = gen_dataset_new.get_phase_mu(
            year_l, year_u)
    
    print("\n")
    print("Part B")
    print("Investigating period %s - %s (phase%s)" %(year_l, year_u, phase))
    print("Mean of the time series of TC counts: ", phase_mu)
    
    # Creating new events for 10000 years
    simulated, x = gen_dataset_new.poisson_and_sim_events(phase_mu, size=10000)
    
    plotting.plot_Poisson(x, phase_mu, phase, year_l, year_u)
    
    
    des = 'ALL' # description of property. Choosing all properties
    par = 'ALL' # desired parish . Choosing all parishes

    # Calculating the sum of ARV according to criteria for place, description of 
    # property and parish.
    # Getting the ARV values, descriptions of properties and names of parishes
    ARV, DES, PAR = arv.read_val_data() 
    
    # Getting the sum of the ARV we want
    sum_arv = arv.choose_descr(des, par, ARV, DES, PAR) 

       
    # Getting distances, wind speeds, damage ratios and losses for the new events
    DIST, WIND, DAM, LOSS = gen_dataset_new.calculations(simulated, sum_arv, place)
    
    # Writting the files for the distances, wind speeds, damage ratios and losses
    gen_dataset_new.write_files(simulated, DIST, 'dist', place, des, par, year_l, year_u)
    gen_dataset_new.write_files(simulated, WIND, 'wind', place, des, par, year_l, year_u)
    gen_dataset_new.write_files(simulated, DAM, 'dam', place, des, par, year_l, year_u)
    gen_dataset_new.write_files(simulated, LOSS, 'loss', place, des, par, year_l, year_u)
    
    # Plotting the time series of new events
    plotting.plot_gen(simulated, phase, name=place)

    # Getting the EP curve for the selected type of property and parish (aggragated
    # annual losses for damaging-only events)
    EP.get_EP(place, 'loss', des, par, year_l, year_u)
    
    return des, par, sum_arv


def PART_C(phase, year_l, year_u, des, par, sum_arv, place='BERMUDA'):
    
    # PART C: Decadal Variability
    #############################
    # For this part, the user needs to look at the time series of TC counts for 
    # the location and manually select the period they want to examine
    # For example, by having a look at time series for TC counts for Bermuda, 
    # the 10-year-moving average was greater than the mean of the moving average 
    # for the period 2003 - 2017. Therefore, the period is considered a 
    # high-frequency phase. 


    # Getting the data (mean, years, counts) for the phase we want to check
    phase_mu, phase_years, phase_counts =  gen_dataset_new.get_phase_mu(year_l, year_u)
    
    print("\n")
    print("Part C")
    print("Investigating period %s - %s (phase%s)" %(year_l, year_u, phase))
    print("Mean of the time series of TC counts: ", phase_mu)
    
    
    plotting.plot_ts_bar(phase_years, phase_counts, phase_mu, 
                         phase,  name=place)
    
    # Creating new events for 10000 years
    sim, x = gen_dataset_new.poisson_and_sim_events(phase_mu, size=10000)

    # Plotting the time series of the new events
    plotting.plot_gen(sim, phase, place)
    
    plotting.plot_Poisson(x, phase_mu, phase, year_l, year_u)
    
    # Getting the distances, wind speeds, damage retions and losses for each even
    DIST, WIND, DAM, LOSS = gen_dataset_new.calculations(sim, sum_arv, place)

    # Writing the files for the distances, wind speeds, damage retions and losses
    gen_dataset_new.write_files(sim, DIST, 'dist%s' %phase, place, des, par, year_l, year_u)
    gen_dataset_new.write_files(sim, WIND, 'wind%s' %phase, place, des, par, year_l, year_u)
    gen_dataset_new.write_files(sim, DAM, 'dam%s' %phase, place, des, par, year_l, year_u)
    gen_dataset_new.write_files(sim, LOSS, 'loss%s' %phase, place, des, par, year_l, year_u)
    
    # Getting the EP curve for the selected type of property and parish (aggragated
    # annual losses for damaging-only events)
    EP.get_EP('BERMUDA', 'loss%s' %phase, des, par, year_l, year_u)	   
    
    return 


if __name__ == '__main__':
    
    # Running using the JRA55 data 
    year_st = 1958 
    year_en = 2017                                        

    PART_A(year_st, year_en)
    des, par, sum_ARV = PART_B(year_st, year_en)
    
    plotting.plot_dam_wind()
    
#    PART_C('_high', 2005, 2017, des, par, sum_ARV)
#    PART_C('_low', 1960, 1975, des, par, sum_ARV)
    
    