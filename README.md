# Diabetes Predictor API

A REST API built with Flask that predicts the likelihood of diabetes based on clinical input features. It exposes two models: a **basic** model and an **ensemble** model.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Server](#running-the-server)
- [API Endpoints](#api-endpoints)
  - [GET /](#get-)
  - [POST /predict](#post-predict)
- [Models](#models)
- [Error Handling](#error-handling)

---

## Prerequisites

- Python 3.8+
- pip

---

## Installation

```bash
# Clone the repository
git clone https://github.com/chinni-d/diabetes_predictor_api.git
cd diabetes_predictor_api

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Server

**Development mode:**

```bash
python app.py
```

The server starts at `http://127.0.0.1:5000` by default.

**Production mode (using Gunicorn):**

```bash
gunicorn app:app
```

---

## API Endpoints

### GET /

Returns a welcome message and basic usage information.

**Request**

```
GET /
```

**Response**

```json
{
  "message": "Diabetes Prediction API is running",
  "usage": "Send a POST request to /predict with the required data",
  "modelsAvailable": ["basic", "ensemble"]
}
```

---

### POST /predict

Predicts diabetes risk for a given set of clinical features.

**Request**

- **Content-Type:** `application/json`

| Field                    | Type   | Required | Description                                      |
|--------------------------|--------|----------|--------------------------------------------------|
| `pregnancies`            | number | Yes      | Number of times pregnant                         |
| `glucose`                | number | Yes      | Plasma glucose concentration (mg/dL)             |
| `bloodPressure`          | number | Yes      | Diastolic blood pressure (mm Hg)                 |
| `skinThickness`          | number | Yes      | Triceps skin fold thickness (mm)                 |
| `insulin`                | number | Yes      | 2-hour serum insulin (mu U/ml)                   |
| `bmi`                    | number | Yes      | Body mass index (weight in kg / height in m²)    |
| `diabetesPedigreeFunction` | number | Yes    | Diabetes pedigree function score                 |
| `age`                    | number | Yes      | Age in years                                     |
| `modelType`              | string | No       | Model to use: `"basic"` (default) or `"ensemble"` |

**Example Request**

```json
{
  "pregnancies": 6,
  "glucose": 148,
  "bloodPressure": 72,
  "skinThickness": 35,
  "insulin": 0,
  "bmi": 33.6,
  "diabetesPedigreeFunction": 0.627,
  "age": 50,
  "modelType": "ensemble"
}
```

**Response**

| Field       | Type   | Description                                           |
|-------------|--------|-------------------------------------------------------|
| `prediction`  | integer | `1` = diabetic, `0` = non-diabetic                  |
| `confidence`  | number  | Model confidence as a percentage (0 - 100)          |
| `riskLevel`   | string  | `"High"` if prediction is `1`, otherwise `"Low"`    |
| `modelUsed`   | string  | The model that was used (`"basic"` or `"ensemble"`)  |

**Example Response**

```json
{
  "prediction": 1,
  "confidence": 78.43,
  "riskLevel": "High",
  "modelUsed": "ensemble"
}
```

---

## Models

| Model      | File                          | Description                            |
|------------|-------------------------------|----------------------------------------|
| `basic`    | `model.pkl`                   | Standard single-estimator model        |
| `ensemble` | `diabetes_ensemble_model.pkl` | Ensemble model with improved accuracy  |

If `modelType` is omitted from the request body, the **basic** model is used by default.

---

## Error Handling

If an error occurs (e.g., a missing or invalid field), the API returns HTTP `500` with a JSON body describing the error:

```json
{
  "error": "<error message>"
}
```

**Example – missing field:**

```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"glucose": 148}'
```

```json
{
  "error": "'pregnancies'"
}
```
