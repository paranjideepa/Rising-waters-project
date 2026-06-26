from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load trained model
model = joblib.load("model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Read input values
        data = [
            float(request.form["Temp"]),
            float(request.form["Humidity"]),
            float(request.form["CloudCover"]),
            float(request.form["ANNUAL"]),
            float(request.form["JanFeb"]),
            float(request.form["MarMay"]),
            float(request.form["JunSep"]),
            float(request.form["OctDec"]),
            float(request.form["avgjune"]),
            float(request.form["sub"])
        ]

        # Make prediction
        prediction = model.predict([data])[0]

        if prediction == 1:

            result = {
                "risk": "🔴 HIGH RISK",
                "status": "⚠️ Flood Likely",
                "color": "red",

                "recommendations": [
                    "Move to higher ground immediately.",
                    "Avoid flooded roads and bridges.",
                    "Keep an emergency kit ready.",
                    "Switch off electricity if flooding starts.",
                    "Follow official government weather alerts."
                ],

                "preparedness": [
                    "🆘 Move to higher ground immediately.",
                    "🚫 Never walk or drive through flood water.",
                    "⚡ Turn off electricity and gas supply if water enters your house.",
                    "🎒 Carry emergency supplies including food, water and medicines.",
                    "📱 Keep your mobile phone fully charged.",
                    "📞 Contact emergency services if immediate assistance is required."
                ],

                "contacts": [
                    "🚑 Ambulance : 108",
                    "👮 Police : 100",
                    "🚒 Fire : 101",
                    "🌊 Disaster Management : 1077"
                ]
            }

        else:

            result = {
                "risk": "🟢 LOW RISK",
                "status": "✅ No Flood Predicted",
                "color": "green",

                "recommendations": [
                    "Current weather conditions indicate a low flood risk.",
                    "Continue monitoring local weather forecasts.",
                    "Keep drainage systems clean around your home.",
                    "Stay prepared during the rainy season.",
                    "Follow official weather advisories for sudden weather changes."
                ],

                "preparedness": [
                    "💧 Store clean drinking water.",
                    "🔋 Keep your mobile phone charged.",
                    "🩹 Keep a first-aid kit ready.",
                    "📻 Stay updated with official weather forecasts.",
                    "📄 Keep important documents in a waterproof folder.",
                    "👨‍👩‍👧 Discuss an emergency plan with your family."
                ],

                "contacts": []
            }

        return render_template(
            "index.html",
            prediction=result,
            form=request.form
        )

    except Exception as e:

        return render_template(
            "index.html",
            prediction={
                "risk": "❌ ERROR",
                "status": str(e),
                "color": "red",
                "recommendations": [],
                "preparedness": [],
                "contacts": []
            },
            form=request.form
        )


if __name__ == "__main__":
    app.run(debug=True)