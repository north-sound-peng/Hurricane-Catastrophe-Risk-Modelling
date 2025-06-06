# Hurricane-Catastrophe-Risk-Modelling
This folder contains scripts with functions which form a catastrophe model used for assessing 
the risk associated with hurricanes for Bermuda. The model was written in Windows 10. This 
guide is written for users who are not familiar with Python. 
------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------

A) TO RUN THE MODEL
-------------------
In order for the model to work the following are necessary:

1) Install Python (https://www.anaconda.com/distribution/)

2) Once the installation is completed, certain modules (shapely, basemap, geog) are required 
	to be installed. To install them, the user is advised to launch the Anaconda Prompt 
	(can be found amongst the programs). For installing, type the following:
	a) for shapely: conda install shapely (press enter; if/when asked [y,n], type y)
	b) for basemap: conda install basemap (press enter; if/when asked [y,n], type y) 
	c) for geog: pip install geog (press enter; if/when asked [y,n], type y)

3) The Annual Rental Value data need to be downloaded from the Bermuda Govt. website 
	(www.landvaluation.bm). Click on Download valuation List(s) on the right hand side, 
	scroll down and download the 2009 Valuation List. Save the file in the the folder 
	DATA with the name Val_2009_cap.xlsx. The user will have to correct a problem in 
	line 2696. 

4) Once the installation of the modules and the data downloading is finished, the user should 
	launch Spyder (can be found amongst the programs) and open the main script for the 
	model:
	File > Open > main_official.py

5) The script contains 3 functions named PART_A, PART_B & PART_C.
	PART_A: Used for creating the historical record of TCs affecting Bermuda
	PART_B: Used for generating new simulated events using information from PART_A and 
		calculating corresponding losses
	PART_C: Used for exploring the effect of decedal variability. The user needs to 
		manually specify the decedal phase they want to analyse as well as whether 
		the phase is a high-frequency or a low-frequency scenario. Corresponding 
		lines are 103-108. Upon downloading the model, PART_C will be set to explore 
		a high-frequency scenario for the 2003-2017 period, therefore the lines (106-
		108) for the low-frequency scenario (1964-1980) will be commented out. To run
		for the low-frequency scenario, lines for the high-frequency scenario (103-105)
		need to be commented out (add # at the beginning of the line) and lines for the 
		low-frequency scenario need to be uncommented (remove #).
	
	In the main_official.PY script, the 3 functions can be run by using lines 141, 142 and
	143. Upon downloading the model, lines 142 and 143 will be commented out (#) so that 
	the user can run only PART_A. Lines 138 and 139 indicate the beginning and end of the 
	period for which there are data (e.g. 1958-2017 in DATA > JRA55). 

	To run PART_A, click on the green triangle (a window will open, click Run)

	To run PART_B & PART_C, lines 142 and 143 need to be uncommented (remove #) first. 
	Then, click on the green triangle. 
------------------------------------------------------------------------------------------------

B) Data necessary for the model to run
--------------------------------------
Data can be found in: 
DATA > ERA5: Csv files with the TC tracks from the ERA5 reanalysis dataset
     > JRA55: Csv files with the TC tracks from the JRA55 reanalysis dataset 
     > Miller.csv : Csv file containing the data from figure 13 in Miller et al. (2013)

The model is set to run with the JRA55 data. To change to ERA5 the user needs to:
	1) Open the read_data.py script in Spyder 
	2) In line 26, change the path from DATA/JRA55/ to DATA/ERA5/
	3) In main_official.py, change line 168 from year_st = 1958 to year_st = 1979

If the user wishes to use their own data, they are adviesed to FIRST run the model once.
Then chech the files Counts.csv and FINAL_f.csv in DATA > BERMUDA > 185KM
These two file provide exactly what is needed for the model to run. 

Counts.csv provides a time series of annual TC counts (within 185km of Bermuda). This is
	used for finding the high- and low- frequency scenarios as well as the average
	annual number of hurricanes.

FINAL_f.csv contains information about the track points which had the highest estimated 
	wind speed at Bermuda for each storm for each year. 
	YEAR: Year
    	TRACK: Track ID of the storm
    	TIME: Timestamp of the point
	LONG: Longitude of the point
   	LAT: Latitude of the point
    	INTEN: Intensity of the point (in m/s, 10-min)
    	B_LON: BDA's longitude
    	B_LAT: BDA's latitude
    	RMAX: The radius of maximum wind speed
    	D_BDA: Distance of the point from BDA
    	V_BDA:

Therefore, if the user wishes to use their one data, they are welcome to, as long as they 
end up with files in similar folder like Counts.csv and FINAL_F.csv and comment out the 
relevant functions.
------------------------------------------------------------------------------------------------

C) Data and plots genereted by the model are saved in:
------------------------------------------------------
DATA > BERMUDA 	> 185KM: 
	1) YEAR.csv files: contain information for the track points of storms that passed within 
			   185km of Bermuda each year.
	2) YEAR_f.csv files: contain information for the track points which had the highest 
			    estimated wind speed at Bermuda for each storm, for each year.
	3) FINAL_f.csv: contains all the track points saved in the individual sYEAR_f.csv files.
	4) Counts: contains the time series of annual TC counts of storms that passed within 
		   185km of Bermuda.

DATA > BERMUDA 	> GEN_DATA: 
	1) New_dataset csv files: contain the distances, wind speeds, damage ratios and 
			    	  losses for the new simulated events for each scenario. 
	2) EP csv files: contain the values for the reversed empirical/theoretical exceedance 
			 probability curves and the corresponding reversed empirical/theoretical
			 return periods of catastrophic events.

DATA > BERMUDA 	> PLOTS: Plots generated by the model.
------------------------------------------------------------------------------------------------
