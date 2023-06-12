import lstm_model as lstm
from data_scrapping import create_working_dataframe
import math
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_percentage_error
import numpy as np
import time
from flask import Flask, request, render_template
import json
from flask_cors import CORS
import os
import matplotlib.pyplot as plt

template_dir = os.path.abspath('./public/templates')
static_dir = os.path.abspath('./public/static')


def show_predicted_temperature(df, model, window_size, hours):
    predicted_temp = []
    latest_window = df.iloc[-window_size:, [0]].to_numpy()
    for i in range(hours):
        predicted_val = model.predict(latest_window.reshape(1, window_size, 1), verbose=0).flatten()
        predicted_temp.append(predicted_val[0])
        latest_window = np.append(latest_window, predicted_val)[1:]

    # string = f'\nOstatnia data: {df.index[-1]}\n'
    # for i, val in enumerate(predicted_temp):
    #     string += f'Temperatura dla godziny T0+{i+1}H: {val:.1f}\n'

    # return string

    data = {'last_known_temp': {'string': f'Ostatnia data: {df.index[-1]}', 'value': float(df.iloc[-1, 0])},
            'predictions': []}
    for i, val in enumerate(predicted_temp):
        data['predictions'].append({'string': f'Temperatura dla godziny T0+{i + 1}H', 'value': float(round(val, 1))})

    # return json.dumps(data, indent=4)
    return predicted_temp


def show_model_statistics(y_true, y_pred):
    r2 = r2_score(y_true, y_pred)
    rmse = math.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred)

    return json.dumps({'r2': r2, 'rmse': rmse, 'mape': mape}, indent=4)


# Building model during container initialization
global_window_size = 20
global_hours = 24

global_df = create_working_dataframe()
global_X_train, global_y_train, global_X_val, global_y_val, global_X_test, global_y_test = lstm.create_sets(global_df,
                                                                                                            global_window_size)
lstm.create_model(global_X_train, global_y_train, global_X_val, global_y_val, window_size=global_window_size)

model = lstm.load_best_model()


# y_pred = model.predict(global_X_test, verbose=0).flatten()

# stats = show_model_statistics(global_y_test, y_pred)
# pred = show_predicted_temperature(global_df, model, global_window_size, global_hours)


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


app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET', 'POST'])
def user_request():
    if request.method == 'GET':
        model = lstm.load_best_model()
        y_pred = model.predict(global_X_test, verbose=0).flatten()

        pred = show_predicted_temperature(global_df, model, global_window_size, global_hours)
        stats = show_model_statistics(global_y_test, y_pred)

        plt.title('Wykres predykcji w zależności od czasu')

        fig = plt.figure(figsize=(6, 6))
        plt.plot(list(range(global_hours)), pred)
        # image_path = "./public/static/plot.png"
        plt.savefig(static_dir)
        # plt.close()

        return render_template('form.html', image_filename=stats)




    else:
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

                    lstm.create_model(global_X_train, global_y_train, global_X_val, global_y_val,
                                      window_size=global_window_size)
                    model = lstm.load_best_model()
                    y_pred = model.predict(global_X_test, verbose=0).flatten()

                    stats = show_model_statistics(global_y_test, y_pred)
                    pred = show_predicted_temperature(global_df, model, global_window_size, global_hours)

                    data = {}
                    data.update(json.loads(stats))
                    data.update(json.loads(pred))

                    return render_template('form.html', data=json.dumps(data, indent=4))



            elif command == 'predict':
                if 'hours' in data:
                    set_global_hours(int(data['hours']))

                    model = lstm.load_best_model()
                    y_pred = model.predict(global_X_test, verbose=0).flatten()

                    pred = show_predicted_temperature(global_df, model, global_window_size, global_hours)
                    return render_template('form.html', data=pred)


            elif command == 'statistics':
                model = lstm.load_best_model()
                y_pred = model.predict(global_X_test, verbose=0).flatten()

                stats = show_model_statistics(global_y_test, y_pred)
                return render_template('form.html', data=stats)

            else:
                return ("ERRORL: Unknown command.")

    # return "ERROR: Invalid request."
    return ("ERROR: Unknown request.")


if __name__ == "__main__":
    start = time.time()
    app.run(host='0.0.0.0', port=8080, debug=True)
    print(time.time() - start)

    while True:
        time.sleep(3600)

        set_global_df(create_working_dataframe())
        X_train, y_train, X_val, y_val, X_test, y_test = lstm.create_sets(global_df, global_window_size)
        set_global_sets(X_train, y_train, X_val, y_val, X_test, y_test)
        lstm.create_model(global_X_train, global_y_train, global_X_val, global_y_val, window_size=global_window_size)