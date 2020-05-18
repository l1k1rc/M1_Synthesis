import itertools
import warnings

import matplotlib.pyplot as plt
import \
    mysql.connector  # pip search mysql-connector | grep --color mysql-connector-pytho | pip install mysql-connector-python (get the last one)
import pandas as pd
import statsmodels.api as sm
import numpy as np

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
daf = pd.read_csv('../data/final.csv', parse_dates=['0'], index_col=['0'])
for val in daf['1']:
    list_daf.append(val)

ts = list_daf

print(ts)
y = pd.DataFrame(ts)


def hyperparameters_optimization(data):
    warnings.filterwarnings("ignore")
    p = d = q = range(0, 2)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
    lf_min = []

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(data, order=param, seasonal_order=param_seasonal,
                                                enforce_stationarity=False, enforce_invertibility=False)
                results = mod.fit(disp=0)
                print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                lf_min.append(results.aic)
            except:
                continue
    print("La veleurs minimal par le critère d'information d'Akaike est :", min(lf_min))


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def build_forecast(data, train_duration):
    # fit model to data
    forecastResult = {}
    res = sm.tsa.statespace.SARIMAX(data,
                                    order=(0, 0, 1),
                                    seasonal_order=(1, 1, 1, 12),
                                    enforce_stationarity=True,
                                    enforce_invertibility=True)
    results = res.fit(disp=0)
    print(results.summary().tables[1])
    # in-sample-prediction and confidence bounds
    pred = results.get_prediction(start=0,
                                  end=train_duration,
                                  dynamic=False,
                                  full_results=True)
    # plot in-sample-prediction
    fig = plt.figure(figsize=(19, 7))
    ax = fig.add_subplot(111)
    ax.plot(data[0:], color='#006699', linewidth=3, label='Observation')
    pred.predicted_mean.plot(ax=ax, linewidth=3, linestyle='-', label='Prediction', alpha=.7, color='#ff5318',
                             fontsize=18)
    ax.fill_betweenx(ax.get_ylim(), train_duration, data.index[-1], alpha=.3, zorder=-1, color='pink')
    ax.set_xlabel('Per minutes', fontsize=18)
    ax.set_ylabel('Users', fontsize=18)
    plt.legend(loc='upper left', prop={'size': 20})
    plt.title('Prediction SARIMA', fontsize=22, fontweight="bold")
    plt.savefig('../data/PredictionARIMA3.png')
    plt.show()
    line = ax.lines[0]


    return line.get_ydata()


data = build_forecast(y, 100)
print(data)
print(np.array_split(data,4))
# hyperparameters_optimization(y)

