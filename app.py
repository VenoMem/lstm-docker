import lstm_model as lstm
from data_scrapping import create_working_dataframe
import math
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_percentage_error
import numpy as np
import time
from flask import Flask, request



def show_predicted_temperature(df, model, window_size, hours):
    predicted_temp = []
    latest_window = df.iloc[-window_size:, [0]].to_numpy()
    for i in range(hours):
        predicted_val = model.predict(latest_window.reshape(1, window_size, 1), verbose=0).flatten()
        predicted_temp.append(predicted_val[0])
        latest_window = np.append(latest_window, predicted_val)[1:]
        
    string = f'\nOstatnia data: {df.index[-1]}\n'
    for i, val in enumerate(predicted_temp):
        string += f'Temperatura dla godziny T0+{i+1}H: {val:.1f}\n'

    return string


def show_model_statistics(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    rmse = math.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred)

    return f"Statystyki modelu\nR^2:\t{round(r2, 3)}\nRMSE:\t{round(rmse, 3)}\nMAPE:\t{round(mape, 3)}"




global_window_size = 20
global_hours = 24
global_df = create_working_dataframe()
global_X_train, global_y_train, global_X_val, global_y_val, global_X_test, global_y_test = lstm.create_sets(global_df, global_window_size)
lstm.create_model(global_X_train, global_y_train, global_X_val, global_y_val, window_size=global_window_size)
model = lstm.load_best_model()
y_pred = model.predict(global_X_test, verbose=0).flatten()
stats = show_model_statistics(global_y_test, y_pred)
print(stats)
pred = show_predicted_temperature(global_df, model, global_window_size, global_hours)
print(pred)




def set_global_window(window_size):
    global global_window_size
    global_window_size = window_size

def set_global_hours(hours):
    global global_hours
    global_hours = hours

def set_global_df(df):
    global global_df
    global_df = df

def set_global_sets(X_train, y_train, X_val, y_val, X_test, y_test):
    global global_X_train, global_y_train, global_X_val, global_y_val, global_X_test, global_y_test
    global_X_train = X_train
    global_y_train = y_train
    global_X_val = X_val
    global_y_val = y_val
    global_X_test = X_test
    global_y_test = y_test


app = Flask(__name__)

@app.route('/', methods=['POST'])
def user_request():
    data = request.form.to_dict()

    if 'command' in data and len(data['command']) > 0:
        command = data['command']
        if command == 'learn':
            if 'window' in data and 'hours' in data:
                set_global_window(int(data['window']))
                set_global_hours(int(data['hours']))
                set_global_df(create_working_dataframe())
                X_train, y_train, X_val, y_val, X_test, y_test = lstm.create_sets(global_df, global_window_size)
                set_global_sets(X_train, y_train, X_val, y_val, X_test, y_test)
                #lstm.create_model(X_train, y_train, X_val, y_val, window_size=global_window_size)
                lstm.create_model(global_X_train, global_y_train, global_X_val, global_y_val, window_size=global_window_size)
                model = lstm.load_best_model()
                y_pred = model.predict(global_X_test, verbose=0).flatten()
                stats = show_model_statistics(global_y_test, y_pred)
                pred = show_predicted_temperature(global_df, model, global_window_size, global_hours)
                return stats + pred
                
        
        elif command == 'predict':
            if 'hours' in data:
                set_global_hours(int(data['hours']))
                model = lstm.load_best_model()
                y_pred = model.predict(global_X_test, verbose=0).flatten()
                pred = show_predicted_temperature(global_df, model, global_window_size, global_hours)
                return pred
                

        elif command == 'statistics':
            if 'hours' in data:
                #set_global_hours(int(data['hours']))
                model = lstm.load_best_model()
                y_pred = model.predict(global_X_test, verbose=0).flatten()
                stats = show_model_statistics(global_y_test, y_pred)
                return stats
                
        else:
            print("Unknown command")

    return "Processed successfully"


if __name__ == "__main__":

    app.run(host='0.0.0.0', port=8080, debug=True)

    while True:
        time.sleep(3600)  # Sleep for an hour

        set_global_df(create_working_dataframe())
        X_train, y_train, X_val, y_val, X_test, y_test = lstm.create_sets(global_df, global_window_size)
        set_global_sets(X_train, y_train, X_val, y_val, X_test, y_test)
        lstm.create_model(global_X_train, global_y_train, global_X_val, global_y_val, window_size=global_window_size)
        