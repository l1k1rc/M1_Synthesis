import matplotlib.pyplot as plt
import numpy as np

import serverAI.IA_interval as heuristic

'''This class allows to retrieve from the heuristic a dataframe which contains all informations about
the forecasting, where whe have for each line, a day in a week and a previsionnal number calculated
by the heuristic which represent the number of access point we want for this hour of this day.'''


class Globalforecasting:
    def __init__(self, forecasting_bandwidth, forecasting_nbClient):
        self.frct_bandwidth = forecasting_bandwidth
        self.frct_nbClient = forecasting_nbClient
        self.mixresult = []

    def get_frct_bandwidth(self, hour):
        return self.frct_bandwidth[hour]

    def get_frct_nbClient(self, hour):
        return self.frct_nbClient[hour]


class Forecasting:
    def __init__(self, nbAP, capacity_client_per_AP, capacity_bandwith_per_AP):
        self.ap = nbAP
        self.client = capacity_client_per_AP
        self.bandwidth = capacity_bandwith_per_AP
        self.daysD = dict(
            {"Monday": Globalforecasting,
             "Tuesday": Globalforecasting,
             "Wednesday": Globalforecasting,
             "Thursday": Globalforecasting,
             "Friday": Globalforecasting,
             "Saturday": Globalforecasting,
             "Sunday": Globalforecasting}
        )

    def heuritic(self):
        nbrOfAP = 5
        interval1 = heuristic.Interval(nbrOfAP, self.capacity_client_per_AP, self.capacity_bandwith_per_AP)
        interval1.config()
        interval1.build()
        print(interval1.getListOfSegm())
        print(interval1.expect(80.16))

    def add(self, forecasting_bandnwidth, forecasting_nbClient, days_):
        for i in range(len(forecasting_bandnwidth)):
            self.daysD[days_] = Globalforecasting(forecasting_bandnwidth, forecasting_nbClient)

    def graphics(self, data):
        data =[4,6,7,8,9,4,5,8]
        hour=range(len(data))
        fig, ax = plt.subplots(figsize=(19, 8))
        ax.bar(hour,data)
        ax.set_xlabel('Smarts')
        ax.set_ylabel('Probability density')
        ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')
        fig.tight_layout()
        plt.show()

forecast = Forecasting(15,5,30)
frct1=[4,6,7,9]
frct2=[10,4,23,24]
forecast.add(frct2,frct1,"Monday")
print(forecast.daysD["Monday"].get_frct_nbClient(0))
forecast.graphics(2)