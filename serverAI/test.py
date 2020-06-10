import numpy as np
import pandas as pd

import serverAI.ML_SARIMA_Forecasting as ia
from serverAI.IA_final_dataframe import Forecasting
from serverAI.ML_SARIMA_Forecasting import getData

def convert(list):
    for d in list:
        if d<0:
            d= abs(d)
    return list

'''
Main program for calling methods for prediction and build objects.
'''
# SARIMA = #, #, p, d ,q, P, D, Q, seasonal_length
if __name__ == '__main__':
    # Retrieve data from logs files
    y = pd.DataFrame(getData("../data/log_mardi.csv"))
    y2 = pd.DataFrame(getData("../data/final_bandwidth.csv"))
    data_nbClient = ia.build_forecast(y, 120, 1, 1, 3, 1, 1, 3, 24)
    data_bandwidth = ia.build_forecast(y2, 120, 0, 1, 1, 0, 1, 1, 24)
    data_per_day = np.array_split(data_nbClient, 5)
    data_per_day2 = np.array_split(data_bandwidth, 5)
    print("Données prévisionnelles CLIENT trouvées :", abs(data_per_day[4]))
    print("Données prévisionnelles BANDWIDTH trouvées :", abs(data_per_day2[4]))
    # hyperparameters_optimization(y2, 2)

    forecast = Forecasting(6, 8, 20)
    forecast.add(abs(data_per_day2[4]), abs(data_per_day[4]), "Monday")
    forecast.predict("Monday")
    forecast.graphics("Monday")
    # print(forecast.daysD["Monday"].get_frct_nbClient(13))  # +1h
    print(forecast.daysD["Monday"].toString())
