from flask import Flask, request, render_template
from flask_cors import cross_origin
import pickle
from datetime import datetime
import random

model = pickle.load(open("Flight-Fare-Prediction.pkl", "rb"))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route("/predict", methods=["GET", "POST"])
@cross_origin()
def predict():
    if request.method == "POST":
        # Setting current date and time
        current_date_time = datetime.now()
        Journey_day = current_date_time.day
        Journey_month = current_date_time.month

        dep_hour = 19
        dep_min = 0

        arrival_hour = 23
        arrival_min = 0

        dur_hour = abs(arrival_hour - dep_hour)
        dur_min = abs(arrival_min - dep_min)

        Source = request.form["Source"]
        if Source == 'Delhi':
            s_Delhi = 1
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0
        elif Source == 'Kolkata':
            s_Delhi = 0
            s_Kolkata = 1
            s_Mumbai = 0
            s_Chennai = 0
        elif Source == 'Mumbai':
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 1
            s_Chennai = 0
        elif Source == 'Chennai':
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 1
        else:
            s_Delhi = 0
            s_Kolkata = 0
            s_Mumbai = 0
            s_Chennai = 0

        Destination = request.form["Destination"]
        if Destination == 'Cochin':
            d_Cochin = 1
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0
        elif Destination == 'Delhi':
            d_Cochin = 0
            d_Delhi = 1
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0
        elif Destination == 'New Delhi':
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 1
            d_Hyderabad = 0
            d_Kolkata = 0
        elif Destination == 'Hyderabad':
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 1
            d_Kolkata = 0
        elif Destination == 'Kolkata':
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 1
        else:
            d_Cochin = 0
            d_Delhi = 0
            d_New_Delhi = 0
            d_Hyderabad = 0
            d_Kolkata = 0

        # Assuming maximum 4 stops
        airlines = [
            "Jet Airways", "IndiGo", "Air India", "Multiple carriers",
            "SpiceJet", "Vistara", "GoAir", "Multiple carriers Premium economy",
            "Jet Airways Business", "Vistara Premium economy", "Trujet"
        ]

        budget = float(request.form.get('Budget'))

        predictions = []
        under_budget = False

        for airline in airlines:
            for stop_count in range(5):
                Total_stops = stop_count
                if airline == 'Jet Airways':
                    Jet_Airways = 1
                    IndiGo = 0
                    Air_India = 0
                    Multiple_carriers = 0
                    SpiceJet = 0
                    Vistara = 0
                    GoAir = 0
                    Multiple_carriers_Premium_economy = 0
                    Jet_Airways_Business = 0
                    Vistara_Premium_economy = 0
                    Trujet = 0
                # Code to set other airline variables based on the current airline...
                else:
                    Jet_Airways = 0
                    IndiGo = 0
                    Air_India = 0
                    Multiple_carriers = 0
                    SpiceJet = 0
                    Vistara = 0
                    GoAir = 0
                    Multiple_carriers_Premium_economy = 0
                    Jet_Airways_Business = 0
                    Vistara_Premium_economy = 0
                    Trujet = 0

                prediction = model.predict([[Total_stops, Journey_day, Journey_month, dep_hour, dep_min, arrival_hour, arrival_min, dur_hour, dur_min, Air_India, GoAir, IndiGo, Jet_Airways, Jet_Airways_Business, Multiple_carriers, Multiple_carriers_Premium_economy, SpiceJet, Trujet, Vistara, Vistara_Premium_economy, s_Chennai, s_Delhi, s_Kolkata, s_Mumbai, d_Cochin, d_Delhi, d_Hyderabad, d_Kolkata, d_New_Delhi]])
                output = round(prediction[0], 2)

                if output <= budget:
                    predictions.append((f"{airline} - with {stop_count} stops: Rs. {output}"))
                    under_budget = True

        if under_budget:
            return render_template('home.html', prediction_text=predictions)
        else:
            cheapest = min([(f"{airline} - with {stop_count} stops: Rs. {output}") for airline in airlines for stop_count in range(5)], key=lambda x: x[1])
            cheapest_flight = f"The cheapest flight is: {cheapest}"
            return render_template('home.html', prediction_text=[cheapest_flight])

if __name__ == "__main__":
    app.run(debug=True)
