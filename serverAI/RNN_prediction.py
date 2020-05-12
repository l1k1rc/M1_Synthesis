import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
#pip install -U protobuf==3.8.0 ================= pour tensorflow

df = pd.read_csv('../data/transaction_data.csv', sep=',', parse_dates=True)
data = df.values
days = np.unique(data[:,2])
ts = []
for d in days:
    ts.append(np.sum(np.multiply(data[np.where(data[:,2]==d)[0],4],data[np.where(data[:,2]==d)[0],5])))
del ts[-1]
del ts[-1]

print(ts)



fig = plt.figure(figsize=(19, 7))
plt.plot(ts, linewidth=3)
plt.title('Observations', fontsize=22, fontweight="bold")
plt.xlabel('jours', fontsize=18)
plt.ylabel('CA', fontsize=18)
plt.savefig('../data/observation.png')
mdl = sm.tsa.statespace.SARIMAX(ts,order=(0, 0, 0),seasonal_order=(2, 2, 1, 7),enforce_stationarity=True,enforce_invertibility=True)
res = mdl.fit()
print(res.summary())

res.plot_diagnostics(figsize=(16, 10))
plt.tight_layout()
plt.show()

y = pd.DataFrame(ts)

# fit model to data
res = sm.tsa.statespace.SARIMAX(y,
                                order=(0, 0, 0),
                                seasonal_order=(2, 2, 1, 7),
                                enforce_stationarity=True,
                                enforce_invertibility=True).fit()

# in-sample-prediction and confidence bounds
pred = res.get_prediction(start=200,
                          end=327,
                          dynamic=False,
                          full_results=True)
# plot in-sample-prediction
fig = plt.figure(figsize=(19, 7))
ax = fig.add_subplot(111)
ax.plot(y[0:], color='#006699', linewidth=3, label='Observation');
pred.predicted_mean.plot(ax=ax, linewidth=3, linestyle='-', label='Prediction', alpha=.7, color='#ff5318', fontsize=18);
ax.fill_betweenx(ax.get_ylim(), 200, y.index[-1], alpha=.3, zorder=-1, color='pink');
ax.set_xlabel('jours', fontsize=18)
ax.set_ylabel('CA', fontsize=18)
plt.legend(loc='upper left', prop={'size': 20})
plt.title('Prediction ARIMA', fontsize=22, fontweight="bold")
plt.savefig('../data/PredictionARIMA.png')
plt.show()

rmse = math.sqrt(((pred.predicted_mean.values.reshape(-1, 1) - y[200:].values) ** 2).mean())
print('rmse = ' + str(rmse))