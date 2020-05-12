import math

import matplotlib.pyplot as plt
import \
    mysql.connector  # pip search mysql-connector | grep --color mysql-connector-pytho | pip install mysql-connector-python (get the last one)
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from numpy import log
import numpy as np, pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import csv
from statsmodels.tsa.stattools import adfuller # to study a time serie


'''mydb = mysql.connector.connect(
    host="localhost",
    user="l1k1",
    passwd="raccoon",
    database="projetM1"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT time, count(*) as NUM FROM csv_data GROUP BY time LIMIT 200")
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
df = pd.read_csv('../data/new_.csv', parse_dates=['0'], index_col=['0'])'''
'''for val in daf['1']:
    list_daf.append(val)

ts = list_daf
print(ts)'''


plt.rcParams.update({'figure.figsize': (9, 7), 'figure.dpi': 250})

def saveAndConvert(data,name='new_3'):
    list = pd.DataFrame(data)
    list.to_csv('../data/new_3.csv', index=False, header=True)
    df = pd.read_csv('../data/new_3.csv', names=['value'], header=0)
    print("Stationary data are : ",df)
    return df

def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return diff

def inverse_difference(last_ob, value):
    return value + last_ob

def obtainExploitableData(data):
    #print(df['1'].tolist())
    # define a dataset with a linear trend
    print(data)
    # difference the dataset
    diff = difference(data)
    print(diff)
    # invert the difference
    inverted = [inverse_difference(data[i], diff[i]) for i in range(len(diff))]
    print(inverted)
    return inverted
# Import data
#df = pd.read_csv('../data/new_2.csv', names=['value'], header=0)
df = pd.read_csv('../data/new_.csv', parse_dates=['0'], index_col=['0'])
new_df = obtainExploitableData(df['1'].tolist())
df = saveAndConvert(new_df)

##########################################################################################

result = adfuller(df.value.dropna())
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])
# Original Series
fig, axes = plt.subplots(3, 2)
axes[0, 0].plot(df.value)
axes[0, 0].set_title('Original Series')
plot_acf(df.value, ax=axes[0, 1])

# 1st Differencing
axes[1, 0].plot(df.value.diff());
axes[1, 0].set_title('1st Order Differencing')
plot_acf(df.value.diff().dropna(), ax=axes[1, 1])

# 2nd Differencing
axes[2, 0].plot(df.value.diff().diff());
axes[2, 0].set_title('2nd Order Differencing')
plot_acf(df.value.diff().diff().dropna(), ax=axes[2, 1])

plt.show()
plt.rcParams.update({'figure.figsize': (9, 3), 'figure.dpi': 120})

fig, axes = plt.subplots(1, 2)
axes[0].plot(df.value.diff());
axes[0].set_title('1st Differencing')
axes[1].set(ylim=(0, 5))
plot_pacf(df.value.diff().dropna(), ax=axes[1])

plt.show()

fig, axes = plt.subplots(1, 2)
axes[0].plot(df.value.diff());
axes[0].set_title('1st Differencing')
axes[1].set(ylim=(0, 1.2))
plot_acf(df.value.diff().dropna(), ax=axes[1])

plt.show()
# => d =1 et p=1

# 1,1,1 ARIMA Model
model = ARIMA(df.value, order=(3, 0, 2))
model_fit = model.fit(disp=0)
print(model_fit.summary())

# Actual vs Fitted
model_fit.plot_predict(dynamic=False)
plt.show()

from statsmodels.tsa.stattools import acf

# Create Training and Test
train = df.value[:160]
test = df.value[160:]

# Build Model
# model = ARIMA(train, order=(3,2,1))
model = ARIMA(train, order=(3, 0, 2))
fitted = model.fit(disp=0)

# Forecast
fc, se, conf = fitted.forecast(39, alpha=0.05)  # 95% conf => niveau de prédiction reste 36 cas par rapport au [:XX]

# Make as pandas series
fc_series = pd.Series(fc, index=test.index)
lower_series = pd.Series(conf[:, 0], index=test.index)
upper_series = pd.Series(conf[:, 1], index=test.index)

# Plot
plt.figure(figsize=(12, 5), dpi=100)
plt.plot(train, label='training')
plt.plot(test, label='actual')
plt.plot(fc_series, label='forecast')
plt.fill_between(lower_series.index, lower_series, upper_series,
                 color='k', alpha=.15)
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=8)
plt.show()

# Build Model
model = ARIMA(train, order=(1, 0, 1))
fitted = model.fit(disp=-1)
print(fitted.summary())

# Forecast
fc, se, conf = fitted.forecast(39, alpha=0.05)  # 95% conf

# Make as pandas series
fc_series = pd.Series(fc, index=test.index)
lower_series = pd.Series(conf[:, 0], index=test.index)
upper_series = pd.Series(conf[:, 1], index=test.index)

# Plot
plt.figure(figsize=(12, 5), dpi=100)
plt.plot(train, label='training')
plt.plot(test, label='actual')
plt.plot(fc_series, label='forecast')
plt.fill_between(lower_series.index, lower_series, upper_series,
                 color='k', alpha=.15)
plt.title('Forecast vs Actuals')
plt.legend(loc='upper left', fontsize=8)
plt.show()
