from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def user_request():
    if request.method == 'POST':
        command = request.form.get('command')

        if command == 'learn':
            # Obsługa komendy "learn"
            # lstm.create_model(X_train, y_train, X_val, y_val, window_size=WINDOW_SIZE)

            return "Komenda 'learn' została wykonana."
        elif command == 'predict':
            # Obsługa komendy "predict"
            #show_predicted_temperature(df, model, WINDOW_SIZE, HOURS)

            return "Komenda 'predict' została wykonana."
        elif command == 'pred_stats':
            # Obsługa komendy "pred_stats"
            #show_model_statistics(y_test, y_pred)
            return "Komenda 'pred_stats' została wykonana."
        else:
            return("ERRORL: Unknown command.")

    return render_template('templates/form.html')

if __name__ == '__main__':
    app.run(debug=True)
