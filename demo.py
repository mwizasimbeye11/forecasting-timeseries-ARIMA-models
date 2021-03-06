# plot the timeseries data, Visualizing data is good.
from pandas import Series
import numpy as np
from statsmodels.tsa.arima_model import ARIMA
# load dataset
series = Series.from_csv('data/daily-minimum-temperatures.csv', header=0)

# split the dataset
split_point = len(series) - 7
dataset, validation = series[0:split_point], series[split_point:]
print ('Dataset %d, Validation %d' % (len(dataset), len(validation)))
dataset.to_csv('dataset.csv')
validation.to_csv('validation.csv')

# create differenced series
def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return np.array(diff)

# invert differenced value
def inverse_difference(history, yhat, interval=1):
	return yhat + history[-interval]

# load dataset for ARIMA model
series = Series.from_csv('dataset.csv', header=None)
# seasonal difference
X = series.values
days_in_year = 365
differenced = difference(X, days_in_year)
# fit model
model = ARIMA(differenced, order=(7,0,1))
model_fit = model.fit(disp=0)
# print summary of fit model
print (model_fit.summary())
forcast = model_fit.forecast(steps=7)[0]
# invert the differenced value to something usable
history = [x for x in X]
day = 1
for yhat in forcast:
    inverted = inverse_difference(history, yhat, days_in_year)
    print('Day %d: %f' % (day, inverted))
    day += 1





