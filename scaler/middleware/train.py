import pandas
from pandas import read_csv
from pandas import concat
from numpy import concatenate
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras import Sequential
from keras.layers import LSTM
from keras.layers import Dense
from math import sqrt


class Train:
    def __init__(self, f, maps):
        self.data = pandas.DataFrame(read_csv(f, header=0))
        self.scaler = None
        self.map_condition = maps

    def series2supervise(self, data, n_in=24, n_out=6, is_drop=True):
        data = pandas.DataFrame(data)
        cols, names = list(), list()
        # add input patterns
        for i in range(n_in, 0, -1):
            cols.append(data.shift(i))
        # add output patterns
        for i in range(0, n_out):
            cols.append(data.shift(-i))
        # concat cols to array
        res = concat(cols, axis=1)
        if is_drop:
            res.dropna(inplace=True)
        return res

    def data_prepro(self):
        dt = self.data.sort_values([self.data.columns[1], self.data.columns[2]], ascending=True)
        v = dt.values
        v[:, 0] = [self.map_condition[x.lower()] for x in v[:, 0]]
        v = v.astype('float32')
        reframed = self.series2supervise(v)
        reframed.columns = range(6*30)
        drop = []
        for i in range(30):
            if i < 24:
                drop += [i*6+1, i*6+2]
            else:
                drop += [i*6+1, i*6+2, i*6+3, i*6+4, i*6+5]
        print(reframed.values[10, :])
        reframed.drop(reframed.columns[drop], axis=1, inplace=True)
        print(reframed.shape)
        print(reframed.values[10, :])
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        reframed = pandas.DataFrame(self.scaler.fit_transform(reframed))
        return reframed

    def model(self):
        reframed = self.data_prepro()
        values = reframed.values
        n_train = 365*24
        n_test = 30*24
        train = values[:-n_test, :]
        test = values[-n_test:, :]
        train_X, train_y = train[:, :-6], train[:, -6:]
        test_X, test_y = test[:, :-6], test[:, -6:]

        print(train.shape)
        # reshape
        train_X = train_X.reshape(train_X.shape[0], 1, train_X.shape[1])
        test_X = test_X.reshape(test_X.shape[0], 1, test_X.shape[1])

        # build network
        model = Sequential()
        model.add(LSTM(50, input_shape=(train_X.shape[1], train_X.shape[2])))
        model.add(Dense(6))
        model.compile(loss='mae', optimizer='adam')

        # fit
        fit = model.fit(train_X, train_y, epochs=1, batch_size=72, validation_data=(test_X, test_y), verbose=2, shuffle=False)
        print(" -------train loss-------")

        # predict
        res_y = model.predict(test_X)

        # get true value
        test_X = test_X.reshape(test_X.shape[0], test_X.shape[2])
        y = concatenate((test_X[:, :], res_y), axis=1)
        y = self.scaler.inverse_transform(y)
        y = y[:, -6:]

        # evaluate RMSE
        ground_y = test_y.reshape((len(test_y), 6))
        ground_y = concatenate((test_X[:, :], ground_y), axis=1)
        ground_y = self.scaler.inverse_transform(ground_y)
        ground_y = ground_y[:, -6:]

        print(" -------PREDICTED Condition-------")
        # print(y)
        #print(ground_y)
        print(" -------ERROR DELTA------")
        #print(y-ground_y)
        rmse = sqrt(mean_squared_error(y, ground_y))
        print(" -------RMSE------")
        print(rmse)
        return model, self.scaler

# maps = {'Unknown': 0, 'Clear': 1, 'Scattered Clouds': 2, 'Mist': 3, 'Haze': 4, 'Shallow Fog': 5,
#         'Patches of Fog': 6, 'Fog': 7, 'Partly Cloudy': 8, 'Mostly Cloudy': 9, 'Overcast': 10,
#         'Funnel Cloud': 11, 'Light Drizzle': 12, 'Drizzle': 13, 'Light Rain': 14, 'Rain': 15,
#         'Heavy Rain': 16, 'Light Thunderstorms and Rain': 17, 'Thunderstorms and Rain': 18,
#         'Thunderstorm': 19, 'Smoke': 20}
# engine = Train('data.csv', maps)
# engine.model()
