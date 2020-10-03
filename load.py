import os
import sys
import time
import numpy as np
import matplotlib.pyplot as plt
import resource as lr
from datetime import datetime


path = os.getcwd()
if not os.path.exists(path + r'\datafile_mcs.xlsx'):
    print("The Script was not executed in the same directory as the datafiles.")
    print("Current working directory is {}.".format(os.path.dirname(path)))
    time.sleep(60) 
    #Console auto exits by windows default 
    #to display the error message the script instead waits for a minute
    sys.exit()

elif os.path.exists(path + r'\datafile_mcs.xlsx'):
    #___________________________________________________________________
    #Michigan Consumer Survey Data MCS

    #NEXT YEAR DATA
    path_data_msc = path + r'\datafile_mcs.xlsx'
    values = lr.load_xlsx(path_data_msc, "C",5) #load from excel
    values = lr.NA_convert(values,"NA")         
    values = lr.string_convert(values)          #make sure the format isnt string
    nextyearmsc = values #assign vatiable name
    nextyearmsc_delta = [nextyearmsc[t+1] - nextyearmsc[t] for t in range(len(nextyearmsc)-1)]

    #NEXT 5 YEARS DATA
    path_data_msc = path + r'\datafile_mcs.xlsx'
    values = lr.load_xlsx(path_data_msc, "D",5) #load from excel
    values = lr.NA_convert(values,"NA")
    values = lr.string_convert(values)          #make sure the format isnt string
    next5yearsmsc = values #assign vatiable name
    next5yearsmsc_delta = [next5yearsmsc[t+1] - next5yearsmsc[t] for t in range(len(next5yearsmsc)-1)]#first differences
    
    #DATES
    path_data_msc = path + r'\datafile_mcs.xlsx'
    values = lr.load_multicolumn_xlsx(path_data_msc,"A","B",5) #load from excel

    datesmsc = np.array([datetime.strptime(i,'%B%Y') for i in values])#convert the format from string to datetime


    #___________________________________________________________________

    #OECD Inflation data

    path_inflation_data_oecd = path + r'\Inflation_Rate_monthly_oecd.xlsx'
    values = np.array(lr.load_xlsx(path_inflation_data_oecd,"C",0))

    inflation_oecd = values




