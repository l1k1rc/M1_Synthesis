import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from pandas.plotting import register_matplotlib_converters
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller

register_matplotlib_converters()
df = pd.read_csv('../data/dataset.csv', parse_dates=['Time'], index_col=['Time'])

print(df.head())
plt.xlabel('Time')
plt.ylabel('User')
plt.plot(df)
plt.show()

# graphics method moyenne mobile et ecart-type mobile
rolling_mean = df.rolling(window=12).mean()
rolling_std = df.rolling(window=12).std()
plt.plot(df, color='blue', label='Origine')
plt.plot(rolling_mean, color='red', label='Moyenne mobile')
plt.plot(rolling_std, color='black', label='Ecart-type mobile')
plt.legend(loc='best')
plt.title('Moyenne et Ecart-type mobiles')
plt.show()

# ADF method
result = adfuller(df['User'])

print('Statistiques ADF : {}'.format(result[0]))
print('p-value : {}'.format(result[1]))
print('Valeurs Critiques :')
for key, value in result[4].items():
    print('\t{}: {}'.format(key, value))

'''# Convert réduction
df_log = np.log(df)
plt.plot(df_log)
plt.show()'''

# Convert réduction
df_log = np.log(df)
plt.plot(df_log)
plt.show()

# transformations que nous pouvons appliquer à une série temporelle pour la rendre stationnaire.
def get_stationarity(timeseries):
    # Statistiques mobiles
    rolling_mean = timeseries.rolling(window=12).mean()
    rolling_std = timeseries.rolling(window=12).std()

    # tracé statistiques mobiles
    original = plt.plot(timeseries, color='blue', label='Origine')
    mean = plt.plot(rolling_mean, color='red', label='Moyenne Mobile')
    std = plt.plot(rolling_std, color='black', label='Ecart-type Mobile')
    plt.legend(loc='best')
    plt.title('Moyenne et écart-type Mobiles')
    plt.show(block=False)

    # Test Dickey–Fuller :
    result = adfuller(timeseries['User'])
    print('Statistiques ADF : {}'.format(result[0]))
    print('p-value : {}'.format(result[1]))
    print('Valeurs Critiques :')
    for key, value in result[4].items():
        print('\t{}: {}'.format(key, value))


# Solution 1
rolling_mean = df_log.rolling(window=12).mean()
df_log_minus_mean = df_log - rolling_mean
df_log_minus_mean.dropna(inplace=True)
get_stationarity(df_log_minus_mean)
# Solution 2
df_log_shift = df_log - df_log.shift()
df_log_shift.dropna(inplace=True)
get_stationarity(df_log_shift)

# utilisation d'ARIMA
#decomposition = seasonal_decompose(df_log,freq=None)
model = ARIMA(df_log, order=(2, 1, 2))
results = model.fit(disp=-1)
plt.plot(df_log_shift)
plt.plot(results.fittedvalues, color='red')
plt.show()

fig = results.plot_predict(1, 60)
plt.show()
