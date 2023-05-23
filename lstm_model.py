from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import *
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import RootMeanSquaredError
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.models import load_model
import numpy as np


def df_to_X_y(df, window_size=20):
    df_as_np = df.to_numpy().ravel()
    X = []
    y = []
    for i in range(len(df_as_np)-window_size):
        row = [[a] for a in df_as_np[i:i+window_size]]
        X.append(row)
        label = df_as_np[i  + window_size]
        y.append(label)
    return np.array(X), np.array(y)



def create_sets(df, window_size=20):
    X, y = df_to_X_y(df, window_size)

    train_amount = int(len(df)*0.8)
    val_amount = int(len(df)*0.9)

    X_train, y_train = X[:train_amount], y[:train_amount]
    X_val, y_val = X[train_amount:val_amount], y[train_amount:val_amount]
    X_test, y_test = X[val_amount:], y[val_amount:]

    return [X_train, y_train, X_val, y_val, X_test, y_test]



def create_model(x_train, y_train, x_val, y_val, window_size=20, epochs=10, alpha=0.0001):
    model = Sequential()
    model.add(InputLayer((window_size, 1)))
    model.add(LSTM(64))
    model.add(Dense(8, 'relu'))
    model.add(Dense(1, 'linear'))

    cp1 = ModelCheckpoint('model/', save_best_only=True, verbose=0)
    model.compile(loss=MeanSquaredError(), optimizer=Adam(learning_rate=alpha), metrics=[RootMeanSquaredError()])

    model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=epochs, callbacks=[cp1], verbose=False)



def load_best_model():
    return load_model('model/')
