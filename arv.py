# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 2021

@author: PINELOPI LOIZOU (BIOS INTERNSHIP)

This script is used for extracting the Annual Rental Value data and for 
choosing the ARV we want according to description of property or parish. 
"""

from __future__ import division
import numpy as np
import xlrd 

def read_val_data():
    """
    This function is used for extracting the Annual Rental Value data
    returns: 
        ARV: the Annual Rental Value data
        DES: the description of the property e.g. HOUSE/APARTMENT 
        PAR: the parish where the property is
    """
  
    infile = "DATA//Val_2009_cap.xlsx"   # filename
    wb = xlrd.open_workbook(infile)  # opening the file
    sheet = wb.sheet_by_index(0)   # getting the worksheet we need

    # INITIALIZING ARRAY & LISTS FOR ARV & DESCRIPTIONS AND PARISHES
    ARV = np.full(sheet.nrows-1, np.nan) 
    DES = [] 
    PAR = [] 
    for i in xrange(1, sheet.nrows):  # saving the values
        ARV[i-1] = sheet.cell_value(i,1)
        DES.append(sheet.cell_value(i,2))
        PAR.append(sheet.cell_value(i,5))
    
    return ARV, DES, PAR
              
def choose_descr(val_d, val_p, arv, des, par):
    """
    This function is used for choosing the annual rental value data we want.
    Different choices for descriptions of properties and parishes can be input.
    params: 
        val_d: input value for description of property.
             : must be all in capital lettes
             : if the user doesnt want to specify description, must put ALL
        val_p: input value for parish.
             : must be all in capital lettes
             : if the user doesnt want to specify parish, must put ALL
    return: 
        sum_arv: one value for the sum of the ARV data
    """
    
    if val_d == "ALL" and val_p == "ALL":   # sum of all arv regardless of 
        sum_arv = np.sum(arv)               # type of property or parish
    elif val_d == "ALL" and val_p != "ALL": # sum of all properties' arv in a 
        sum_arv = 0                         # a given parish
        for i in xrange(len(par)):
            if par[i] == val_p:
                sum_arv = sum_arv + arv[i]
    elif val_d != "ALL" and val_p == "ALL": # sum of ARVs of a specific type of 
        sum_arv = 0                         # property regardless of parish
        for i in xrange(len(des)):
            if des[i] == val_d:
                sum_arv = sum_arv + arv[i]
    elif val_d != "ALL" and val_p != "ALL": # sum of ARVs of a specific type 
        sum_arv = 0                         # of property in a specifi parish
        for i in xrange(len(des)):
            if par[i] == val_p and des[i] == val_d:
                sum_arv = sum_arv + arv[i]
    
    return sum_arv           


#ARV, DES, PAR = read_val_data()
#print choose_descr("HOUSE", "CITY OF HAMILTON", ARV, DES, PAR)
#print choose_descr("ALL", "ALL", ARV, DES, PAR)