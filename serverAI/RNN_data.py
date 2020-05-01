import \
    mysql.connector  # pip search mysql-connector | grep --color mysql-connector-pytho | pip install mysql-connector-python (get the last one)
import matplotlib.pyplot as plt
import \
    mysql.connector  # pip search mysql-connector | grep --color mysql-connector-pytho | pip install mysql-connector-python (get the last one)
import numpy as np
import pandas as pd
from keras.layers import Dense
from keras.models import Sequential

mydb = mysql.connector.connect(
    host="localhost",
    user="l1k1",
    passwd="raccoon",
    database="projetM1"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT time, count(*) as NUM FROM csv_data GROUP BY time LIMIT 500")
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
list_daf=[]
daf = pd.read_csv('../data/new_.csv', parse_dates=['0'], index_col=['0'])
for val in daf['1']:
    list_daf.append(val)
print(list_daf)

'''df = pd.read_csv('/home/l1k1/Documents/transaction_data.csv', sep=',', parse_dates=True)
data = df.values
days = np.unique(data[:, 2])
ts = []
for d in days:
    ts.append(np.sum(np.multiply(data[np.where(data[:, 2] == d)[0], 4], data[np.where(data[:, 2] == d)[0], 5])))
del ts[-1]
del ts[-1]
print(ts)'''
ts = list_daf

y = pd.DataFrame(ts)
def preparation_data(data, lags=1):
    X, y = [], []
    for row in range(len(data) - lags - 1):
        a = data[row:(row + lags)]
        X.append(a)
        y.append(data[row + lags])
    return np.array(X), np.array(y)


train = ts[0:190]
test = ts[190:]
lags = 10
X_train, y_train = preparation_data(train, lags)
X_test, y_test = preparation_data(test, lags)

mdl = Sequential()
mdl.add(Dense(4, input_dim=lags, activation='relu'))
mdl.add(Dense(8, activation='relu'))
mdl.add(Dense(1))
mdl.compile(loss='mean_squared_error', optimizer='adam')
mdl.fit(X_train, y_train, epochs=400, batch_size=2, verbose=2)

train_score = mdl.evaluate(X_train, y_train, verbose=0)
test_score = mdl.evaluate(X_test, y_test, verbose=0)

train_predict = mdl.predict(X_train)
test_predict = mdl.predict(X_test)

train_predict_plot = np.empty_like(ts)
train_predict_plot[:, ] = np.nan
train_predict_plot[lags: len(train_predict) + lags, ] = train_predict.reshape(179, )

test_predict_plot = np.empty_like(ts)
test_predict_plot[:, ] = np.nan
test_predict_plot[len(train_predict) + (lags * 2) + 1:len(ts) - 1, ] = test_predict.reshape(299,)

fig = plt.figure(figsize=(19, 7))
ax = fig.add_subplot(111)
ax.plot(y[0:], color='#006699', linewidth=3, label='Observation');
df_pred = pd.Series(pd.DataFrame(test_predict_plot).dropna().values.reshape(500,),
                    pd.DataFrame(test_predict_plot).dropna().index)
df_pred.plot(ax=ax, linewidth=3, linestyle='-', label='Prediction', alpha=.7, color='#ff5318', fontsize=18);
ax.fill_betweenx(ax.get_ylim(), 200, y.index[-1], alpha=.3, zorder=-1, color='pink');
ax.set_xlabel('jours', fontsize=18)
ax.set_ylabel('CA', fontsize=18)
plt.legend(loc='upper left', prop={'size': 20})
plt.title('Prediction RNN', fontsize=22, fontweight="bold")
plt.savefig('../data/PredictionRNN.png')
plt.show()
