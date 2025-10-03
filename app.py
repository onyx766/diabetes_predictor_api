from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib
import numpy as np

app = Flask(__name__)
CORS(app)

# Load both models
model_basic = joblib.load("model.pkl")
model_ensemble = joblib.load("diabetes_ensemble_model.pkl")

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Diabetes Prediction API is running",
        "usage": "Send a POST request to /predict with the required data",
        "modelsAvailable": ["basic", "ensemble"]
    })

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        print("Received data:", data)

        model_type = data.get('modelType', 'basic')  # default to 'basic'

        features = [
            float(data['pregnancies']),
            float(data['glucose']),
            float(data['bloodPressure']),
            float(data['skinThickness']),
            float(data['insulin']),
            float(data['bmi']),
            float(data['diabetesPedigreeFunction']),
            float(data['age'])
        ]

        # Choose the model
        if model_type == 'ensemble':
            model = model_ensemble
        else:
            model = model_basic

        prediction = model.predict([features])[0]
        probability = model.predict_proba([features])[0][int(prediction)]

        risk_level = "High" if prediction == 1 else "Low"

        return jsonify({
            "prediction": int(prediction),
            "confidence": round(probability * 100, 2),
            "riskLevel": risk_level,
            "modelUsed": model_type
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

