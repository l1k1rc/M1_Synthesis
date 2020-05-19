import math

import matplotlib.pyplot as plt
import \
    mysql.connector  # pip search mysql-connector | grep --color mysql-connector-pytho | pip install mysql-connector-python (get the last one)
import pandas as pd
import statsmodels.api as sm

mydb = mysql.connector.connect(
    host="localhost",
    user="l1k1",
    passwd="raccoon",
    database="projetM1"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT time, count(*) as NUM FROM csv_data GROUP BY time LIMIT 100")
result_set = mycursor.fetchall()
time = []
user = []
dt = []
for row in result_set:
    dt.append(row)
    # print("%s, %s" % (row[0], row[1]))
    # user.append(row[1])
    # time.append(row[0])

dttime = pd.DataFrame(dt)
dttime.to_csv('../data/new_.csv', index=False, header=True)

# register_matplotlib_converters()
list_daf = []
daf = pd.read_csv('../data/final_ARIMA.csv', parse_dates=['0'], index_col=['0'])
for val in daf['1']:
    list_daf.append(val)

ts = list_daf

print(ts)
y = pd.DataFrame(ts)


def build_forecast(data,train_duration):
    # fit model to data
    res = sm.tsa.statespace.SARIMAX(data,
                                    order=(2, 1, 0),
                                    seasonal_order=(2, 2, 1, 9),
                                    enforce_stationarity=True,
                                    enforce_invertibility=True).fit()

    # in-sample-prediction and confidence bounds
    pred = res.get_prediction(start=0,
                              end=train_duration,
                              dynamic=False,
                              full_results=True)
    # plot in-sample-prediction
    fig = plt.figure(figsize=(19, 7))
    ax = fig.add_subplot(111)
    ax.plot(data[0:], color='#006699', linewidth=3, label='Observation')
    pred.predicted_mean.plot(ax=ax, linewidth=3, linestyle='-', label='Prediction', alpha=.7, color='#ff5318', fontsize=18)
    ax.fill_betweenx(ax.get_ylim(), train_duration, data.index[-1], alpha=.3, zorder=-1, color='pink')
    ax.set_xlabel('Per minutes', fontsize=18)
    ax.set_ylabel('Users', fontsize=18)
    plt.legend(loc='upper left', prop={'size': 20})
    plt.title('Prediction SARIMA', fontsize=22, fontweight="bold")
    plt.savefig('../data/PredictionARIMA3.png')
    plt.show()

build_forecast(y,85)
