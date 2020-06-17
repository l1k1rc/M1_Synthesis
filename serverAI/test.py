#!/usr/bin/env python

import os
import warnings

import numpy as np
import pandas as pd

import serverAI.ML_SARIMA_Forecasting as ia
from serverAI.IA_final_dataframe import Forecasting
from serverAI.ML_SARIMA_Forecasting import getData


class Style:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


'''
Main program for calling methods for prediction and build objects.
'''

warnings.filterwarnings("ignore")
# SARIMA = #, #, p, d ,q, P, D, Q, seasonal_length
# Retrieve data from logs files
day = "Monday"
# For the execution from the IDE
# y = pd.DataFrame(getData("../data/log_lundi.csv"))
# y2 = pd.DataFrame(getData("../data/log_lundi_bw.csv"))

# For the execution from the terminal
y = pd.DataFrame(getData("data/log_lundi.csv"))
y2 = pd.DataFrame(getData("data/log_lundi_bw.csv"))

data_nbClient = ia.build_forecast(y, 120, 1, 1, 3, 1, 1, 3, 24, "nbCLient", day)
data_bandwidth = ia.build_forecast(y2, 120, 0, 1, 1, 0, 1, 1, 24, "Bandwidth_Mo.s", day)
data_per_day = np.array_split(data_nbClient, 5)
data_per_day2 = np.array_split(data_bandwidth, 5)
print(Style.OKBLUE+"Estimated data found for CLIENT :"+ str(abs(data_per_day[4]))+Style.ENDC)
print(Style.HEADER+"Estimated data found for BANDWIDTH :"+ str(abs(data_per_day2[4]))+Style.ENDC)
# hyperparameters_optimization(y2, 2)

forecast = Forecasting(6, 8, 20)
forecast.add(abs(data_per_day2[4]), abs(data_per_day[4]), day)
forecast.predict(day)
forecast.graphics(day)

path = os.getcwd()
repn = os.path.basename(path)

print(Style.BOLD+Style.OKGREEN+"All images and data generated by the artificial intelligence are saved in the folder : : " + path + repn+Style.ENDC)
# print(forecast.daysD["Monday"].get_frct_nbClient(13))  # +1h
# print(forecast.daysD[day].toString())
