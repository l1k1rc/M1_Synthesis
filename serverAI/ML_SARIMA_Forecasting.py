import itertools
import warnings

import matplotlib.pyplot as plt
import \
    mysql.connector  # pip search mysql-connector | grep --color mysql-connector-pytho | pip install mysql-connector-python (get the last one)
import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

plt.style.use('fivethirtyeight')

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

'''
Methode which just display data inside graphics.
'''


def simple_graphics(data):
    import matplotlib
    matplotlib.rcParams['axes.labelsize'] = 14
    matplotlib.rcParams['xtick.labelsize'] = 12
    matplotlib.rcParams['ytick.labelsize'] = 12
    fig = plt.figure(figsize=(19, 7))
    ax = fig.add_subplot(111)
    # Add more ticks for X axis
    x = list(range(0, len(data)))
    plt.xticks(np.arange(min(x), max(x) + 1, 2.0))

    ax.plot(data[0:], color='#006699', linewidth=3, label='User\'s Values')
    ax.axvspan(0, 24, alpha=.3, color='green', zorder=-1)
    ax.axvspan(24, 48, alpha=.3, color='orange', zorder=-1)
    ax.axvspan(48, 72, alpha=.3, color='yellow', zorder=-1)
    ax.axvspan(72, 96, alpha=.3, color='red', zorder=-1)
    ax.set_xlabel('Per hour', fontsize=18)
    ax.set_ylabel('Nb.Users', fontsize=18)
    plt.legend(loc='upper left', prop={'size': 20})
    plt.title('Number of user per hour', fontsize=22, fontweight="bold")
    plt.savefig('../data/PredictionARIMA3.png')
    plt.show()


'''
@:parameter= data : send timeserie values
@:param training_length : Intreval of search where AIC criterion try  
This method is a method called "Hyperparameters optimization". This is the 
grid search method based on an evaluation criterion given to each parameter 
sequence sent to the SARIMA model: the Akaike Criterion (AIC).
The method returns the sequence associated with the lowest of the calculated criteria.
'''


def hyperparameters_optimization(data,
                                 training_length):  # ARIMA(0, 2, 1)x(1, 3, 0, 24)24 - AIC:6.0 and ARIMA(0, 1, 0)x(2, 2, 0, 24)24 - AIC:6.0
    warnings.filterwarnings("ignore")
    p = d = q = range(0, training_length)
    pdq = list(itertools.product(p, d, q))
    seasonal_pdq = [(x[0], x[1], x[2], 24) for x in list(itertools.product(p, d, q))]
    lf_min = []

    for param in pdq:
        for param_seasonal in seasonal_pdq:
            try:
                mod = sm.tsa.statespace.SARIMAX(data, order=param, seasonal_order=param_seasonal,
                                                enforce_stationarity=False, enforce_invertibility=False)
                results = mod.fit(disp=0)
                print('ARIMA{}x{}24 - AIC:{}'.format(param, param_seasonal, results.aic))
                lf_min.append(results.aic)
            except:
                continue
    print("La veleurs minimal par le critère d'information d'Akaike est :", min(lf_min))


def chunks(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def test_stationarity(data):
    # Determing rolling statistics
    rolmean = pd.rolling_mean(data, window=12)
    rolstd = pd.rolling_std(data, window=12)  # Plot rolling statistics:
    plt.plot(data, color='blue', label='Original')
    plt.plot(rolmean, color='red', label='Rolling Mean')
    plt.plot(rolstd, color='black', label='Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show()
    # Perform Dickey-Fuller test:
    print('Results of Dickey-Fuller Test:')
    dftest = adfuller(data, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic', 'p-value', '#Lags Used', 'Number of Observations Used'])
    for key, value in dftest[4].items():
        dfoutput['Critical Value (%s)' % key] = value
    print(dfoutput)


'''
@:parameter data= for timeserie
@:parameter train_duration= how far to prédict the data by considering the 
ratio 75:25 for train/test.
This method build a plot to show the prediction values and get them to send to another method.
'''


def build_forecast(data, train_duration, p, d, q, P, D, Q, season_length):
    # Hyperparameters given by their optimization from grid-searching done before
    # for each value : p,d,q and P,D,Q,m
    forecastResult = {}
    res = sm.tsa.statespace.SARIMAX(data,
                                    order=(p, d, q),
                                    seasonal_order=(P, D, Q, season_length),
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
    x = list(range(0, len(data) + 24))
    plt.xticks(np.arange(min(x), max(x) + 1, 5.0))
    ax.plot(data[0:], color='#006699', linewidth=3, label='Actual')
    pred.predicted_mean.plot(ax=ax, linewidth=3, linestyle='-', label='Forecast', alpha=.7, color='#ff5318',
                             fontsize=18)
    ax.fill_betweenx(ax.get_ylim(), train_duration, data.index[-1], alpha=.3, zorder=-1, color='pink')
    ax.set_xlabel('Per hour', fontsize=18)
    ax.set_ylabel('Nb.users', fontsize=18)
    plt.legend(loc='upper left', prop={'size': 20})
    plt.title('Prediction SARIMA', fontsize=22, fontweight="bold")
    plt.savefig('../data/PredictionARIMA3.png')
    plt.show()
    line = ax.lines[1]
    return line.get_ydata()


# simple_graphics(y)
# test_stationarity(y)
# SARIMA = #, #, p, d ,q, P, D, Q, seasonal_length
data = build_forecast(y, 120, 1, 1, 3, 1, 1, 3, 24)
print(data)
data_per_day = np.array_split(data, 5)
print("Données prévisionnelles trouvées :", data_per_day[4])
#hyperparameters_optimization(y,3)
