import matplotlib.pyplot as plt
import \
    mysql.connector  # pip search mysql-connector | grep --color mysql-connector-pytho | pip install mysql-connector-python (get the last one)
import pandas as pd
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller  # to study a time serie

# Connect to database and send a request to find number of client per minutes
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
# convert the result into csv


plt.rcParams.update({'figure.figsize': (9, 7), 'figure.dpi': 250})
############ Make the serie stationnary ############
def saveAndConvert(data,name='new_3'):
    list = pd.DataFrame(data)
    list.to_csv('../data/new_3.csv', index=False, header=True)
    df = pd.read_csv('../data/new_3.csv', names=['value'], header=0)
    #print("Stationary data are : ",df)
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
#Convert the data into an exploitable stationary serie
new_df = obtainExploitableData(df['1'].tolist())
df = saveAndConvert(new_df)
################################################################
import warnings
from pandas import read_csv
from statsmodels.tsa.arima_model import ARIMA
from sklearn.metrics import mean_squared_error

# evaluate an ARIMA model for a given order (p,d,q)
def evaluate_arima_model(X, arima_order):
# prepare training dataset
	train_size = int(len(X) * 0.66)
	train, test = X[0:train_size], X[train_size:]
	history = [x for x in train]
	# make predictions
	predictions = list()
	for t in range(len(test)):
		model = ARIMA(history, order=arima_order)
		model_fit = model.fit(disp=0)
		yhat = model_fit.forecast()[0]
		predictions.append(yhat)
		history.append(test[t])
	# calculate out of sample error
	error = mean_squared_error(test, predictions)
	return error

# evaluate combinations of p, d and q values for an ARIMA model
def evaluate_models(dataset, p_values, d_values, q_values):
	dataset = dataset.astype('float32')
	best_score, best_cfg = float("inf"), None
	for p in p_values:
		for d in d_values:
			for q in q_values:
				order = (p,d,q)
				try:
					mse = evaluate_arima_model(dataset, order)
					if mse < best_score:
						best_score, best_cfg = mse, order
					print('ARIMA%s MSE=%.3f' % (order,mse))
				except:
					continue
	print('Best ARIMA%s MSE=%.3f' % (best_cfg, best_score))

# load dataset
df = read_csv('../data/test_dt_4.csv', header=0, index_col=0, names=['value'])
# evaluate parameters
print(df.value)
p_values = [0, 1, 2, 4, 6, 8, 10]
d_values = range(0, 3)
q_values = range(0, 3)
#warnings.filterwarnings("ignore")
#evaluate_models(df.values, p_values, d_values, q_values)
######################################################################"


############ Serie stationary ############
#If p-value is low, the serie is stationary
result = adfuller(df.value.dropna())
print('ADF Statistic: %f' % result[0])
print('p-value: %f' % result[1])

def findMATermsQ(dataframe):
    fig, axes = plt.subplots(1, 2)
    axes[0].plot(dataframe.value.diff())
    axes[0].set_title('Graphics for Q terms')
    axes[1].set(ylim=(0, 1.2))
    plot_acf(dataframe.value.diff().dropna(), ax=axes[1])

    plt.show()

def findARTermsP(dataframe):
    fig, axes = plt.subplots(1, 2)
    axes[0].plot(dataframe.value.diff())
    axes[0].set_title('Graphics for P terms')
    axes[1].set(ylim=(0, 5))
    plot_pacf(dataframe.value.diff().dropna(), ax=axes[1])

    plt.show()

def findDifferencingTermsD(dataframe):
    # Original Series
    fig, axes = plt.subplots(3, 2)
    axes[0, 0].plot(dataframe.value)
    axes[0, 0].set_title('Graphics for differencing terms')
    plot_acf(dataframe.value, ax=axes[0, 1])

    # 1st Differencing
    axes[1, 0].plot(dataframe.value.diff())
    axes[1, 0].set_title('1st differencing')
    plot_acf(dataframe.value.diff().dropna(), ax=axes[1, 1])

    # 2nd Differencing
    axes[2, 0].plot(dataframe.value.diff().diff())
    axes[2, 0].set_title('2nd differencing')
    plot_acf(dataframe.value.diff().diff().dropna(), ax=axes[2, 1])

    plt.show()

findARTermsP(df)
findMATermsQ(df)
# 1,1,1 ARIMA Model as p,d,q
# d = 0 s la série est déjà stationnaire besoin de# différenciation uniquement si la série
# n'est pas stationnaire. Sinon, aucune différenciation n'est nécessaire
# si p < 0.05 alors on peut dire que la série est staionnaire
# si p > 0.05 alors il faut trouver un ordre de différenciation d


# Enfin il faut trouver le nombre de terme AR = p en inspectant le tracé d'autocorrélation partielle (PACF).
# PACF transmet en quelque sorte la corrélation pure entre un décalage et la série
# Toute autocorrélation dans une série stationnaire peut être corrigée en ajoutant suffisamment de termes
# AR. Donc, il faut prendre initialement l'ordre du terme AR comme étant égal à autant de retards qui
# franchissent la limite de signification dans le tracé PACF

# Un terme MA est techniquement, l'erreur de la prévision décalée.
# L'ACF indique combien de termes MA sont nécessaires pour supprimer
# toute autocorrélation dans la série stationnaire.
# order = (AR,d,MA)
model = ARIMA(df.value, order=(6, 1, 0))
model_fit = model.fit(disp=0)
print(model_fit.summary())


residuals = pd.DataFrame(model_fit.resid)
fig, ax = plt.subplots(1,2)
residuals.plot(title="Residuals", ax=ax[0])
residuals.plot(kind='kde', title='Density', ax=ax[1])
plt.show()

model_fit.plot_predict(dynamic=False)
plt.show()
'''
@:train : 60% of total values
@:test : rest of train => 40% of total values
'''



# Create Training and Test
train = df.value[:300]
test = df.value[300:]

###########################################################################################

def build(p,d,q,val_forecast,train, test):
    # Build Model
    model = ARIMA(train, order=(p, d, q))
    fitted = model.fit(disp=0)
    print(fitted.summary())

    # Forecast
    fc, se, conf = fitted.forecast(val_forecast, alpha=0.10)  # 95% conf

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


build(6, 1, 0, 65, train, test)

