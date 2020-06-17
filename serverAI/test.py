import numpy as np
import pandas as pd

import serverAI.ML_SARIMA_Forecasting as ia
from serverAI.IA_final_dataframe import Forecasting
from serverAI.ML_SARIMA_Forecasting import getData

'''
Main program for calling methods for prediction and build objects.
'''
# SARIMA = #, #, p, d ,q, P, D, Q, seasonal_length
# Retrieve data from logs files
day = "Monday"
y = pd.DataFrame(getData("../data/log_lundi.csv"))
y2 = pd.DataFrame(getData("../data/log_lundi_bw.csv"))

data_nbClient = ia.build_forecast(y, 120, 1, 1, 3, 1, 1, 3, 24, "nbCLient", day)
data_bandwidth = ia.build_forecast(y2, 120, 0, 1, 1, 0, 1, 1, 24, "Bandwidth_Mo.s", day)
data_per_day = np.array_split(data_nbClient, 5)
data_per_day2 = np.array_split(data_bandwidth, 5)
print("Estimated data found for CLIENT :", abs(data_per_day[4]))
print("Estimated data found for BANDWIDTH :", abs(data_per_day2[4]))
# hyperparameters_optimization(y2, 2)

forecast = Forecasting(6, 8, 20)
forecast.add(abs(data_per_day2[4]), abs(data_per_day[4]), day)
forecast.predict(day)
forecast.graphics(day)
    # print(forecast.daysD["Monday"].get_frct_nbClient(13))  # +1h
    # print(forecast.daysD[day].toString())
