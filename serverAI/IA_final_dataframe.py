import matplotlib.pyplot as plt

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

    def addEnd(self, data):
        self.mixresult.append(data)

    def getMixresult(self):
        return self.mixresult

    def toString(self):
        for v in self.mixresult:
            print(v)


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

    def add(self, forecasting_bandnwidth, forecasting_nbClient, days_):
        for i in range(len(forecasting_bandnwidth)):
            self.daysD[days_] = Globalforecasting(forecasting_bandnwidth, forecasting_nbClient)

    def predict(self, days_):
        interval = heuristic.Interval(self.ap, self.client, self.bandwidth)
        interval.config()
        interval.build()
        for i in range(23): #interval.expect(
            self.daysD[days_].addEnd(interval.expect(
                interval.define(self.daysD[days_].get_frct_nbClient(i), self.daysD[days_].get_frct_bandwidth(i))))

    def graphics(self, days_):
        hour = range(len(self.daysD[days_].getMixresult()))
        fig, ax = plt.subplots(figsize=(19, 8))
        ax.bar(hour, self.daysD[days_].getMixresult())
        ax.set_xlabel('Heures')
        ax.set_ylabel('Nb. Points d\'accès')
        ax.set_title('Nombre de bornes WIFI idéal du '+days_)
        fig.tight_layout()
        plt.show()


'''forecast = Forecasting(15,5,30)
frct1=[4,6,7,9]
frct2=[10,4,23,24]
forecast.add(frct2,frct1,"Monday")
print(forecast.daysD["Monday"].get_frct_nbClient(0))#1h
forecast.graphics(2)'''
