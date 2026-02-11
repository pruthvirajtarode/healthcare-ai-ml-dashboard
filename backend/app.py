"""
Healthcare ML Backend API using Flask
Provides endpoints for data analysis and risk prediction
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import json
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.preprocessing import StandardScaler
import pickle
import os

app = Flask(__name__)
CORS(app)

# Configuration
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Load reports
try:
    with open(DATA_DIR / "eda_report.json", 'r') as f:
        eda_report = json.load(f)
except:
    eda_report = {}

try:
    with open(DATA_DIR / "kpi_report.json", 'r') as f:
        kpi_report = json.load(f)
except:
    kpi_report = {}

try:
    with open(DATA_DIR / "ml_preparation_report.json", 'r') as f:
        ml_report = json.load(f)
except:
    ml_report = {}

# Load engineered data
try:
    engineered_data = pd.read_csv(DATA_DIR / "healthcare_data_engineered.csv")
except:
    engineered_data = None


@app.route('/')
def index():
    """Serve the dashboard"""
    return send_from_directory(BASE_DIR / 'frontend', 'index.html')


@app.route('/<path:filename>')
def serve_frontend(filename):
    """Serve frontend files"""
    return send_from_directory(BASE_DIR / 'frontend', filename)


@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Healthcare API is running"})


@app.route('/api/eda-report')
def get_eda_report():
    """Get EDA analysis report"""
    return jsonify(eda_report if eda_report else {"error": "EDA report not found"})


@app.route('/api/kpi-report')
def get_kpi_report():
    """Get KPI report"""
    return jsonify(kpi_report if kpi_report else {"error": "KPI report not found"})


@app.route('/api/ml-report')
def get_ml_report():
    """Get ML preparation report"""
    return jsonify(ml_report if ml_report else {"error": "ML report not found"})


@app.route('/api/dataset-stats')
def get_dataset_stats():
    """Get basic dataset statistics"""
    if engineered_data is None:
        return jsonify({"error": "Dataset not found"}), 404

    stats = {
        "total_records": len(engineered_data),
        "total_features": len(engineered_data.columns),
        "missing_values": engineered_data.isnull().sum().to_dict(),
        "data_types": engineered_data.dtypes.astype(str).to_dict(),
        "numeric_summary": engineered_data.describe().to_dict()
    }
    return jsonify(stats)


@app.route('/api/high-risk-patients')
def get_high_risk_patients():
    """Get high-risk patients list"""
    if engineered_data is None:
        return jsonify({"error": "Dataset not found"}), 404

    # Filter high-risk patients
    high_risk = engineered_data[
        (engineered_data['Risk_Score'] >= 60) |
        (engineered_data['Disease_Risk'] == 'Heart Risk')
    ]

    high_risk_list = high_risk[[
        'Patient_ID', 'Name', 'Age', 'BMI', 'Blood_Pressure',
        'Glucose', 'Disease_Risk', 'Health_Score', 'Risk_Score'
    ]].to_dict('records')

    return jsonify({
        "total_high_risk": len(high_risk_list),
        "percentage": round((len(high_risk_list) / len(engineered_data)) * 100, 2),
        "patients": high_risk_list
    })


@app.route('/api/distribution/<metric>')
def get_distribution(metric):
    """Get distribution for a specific metric"""
    if engineered_data is None:
        return jsonify({"error": "Dataset not found"}), 404

    distributions = {
        "age_groups": {
            "0-18": len(engineered_data[(engineered_data['Age'] >= 0) & (engineered_data['Age'] < 18)]),
            "18-30": len(engineered_data[(engineered_data['Age'] >= 18) & (engineered_data['Age'] < 30)]),
            "30-45": len(engineered_data[(engineered_data['Age'] >= 30) & (engineered_data['Age'] < 45)]),
            "45-60": len(engineered_data[(engineered_data['Age'] >= 45) & (engineered_data['Age'] < 60)]),
            "60+": len(engineered_data[engineered_data['Age'] >= 60])
        },
        "disease": engineered_data['Disease_Risk'].value_counts().to_dict(),
        "city": engineered_data['City'].value_counts().to_dict() if 'City' in engineered_data.columns else {},
        "bmi_category": engineered_data['BMI_Category'].value_counts().to_dict() if 'BMI_Category' in engineered_data.columns else {}
    }

    if metric in distributions:
        return jsonify(distributions[metric])
    else:
        return jsonify({"error": f"Distribution for {metric} not found"}), 404


@app.route('/api/predict-risk', methods=['POST'])
def predict_risk():
    """
    Predict risk score for a patient
    
    Expected JSON:
    {
        "age": int,
        "bmi": float,
        "blood_pressure": int,
        "glucose": int,
        "disease_risk": string,
        "city": string
    }
    """
    try:
        data = request.get_json()

        # Extract features
        age = float(data.get('age', 0))
        bmi = float(data.get('bmi', 0))
        bp = float(data.get('blood_pressure', 0))
        glucose = float(data.get('glucose', 0))
        disease = data.get('disease_risk', 'Normal')

        # Calculate risk score (simplified version of ML model)
        risk_score = 0

        # Age risk
        risk_score += (age - 50) * 0.5 if age > 50 else 0

        # BMI risk
        if bmi < 18.5 or bmi >= 30:
            risk_score += 20
        elif bmi >= 25:
            risk_score += 10

        # BP risk
        if bp >= 140:
            risk_score += 20
        elif bp >= 120:
            risk_score += 10

        # Glucose risk
        if glucose >= 126:
            risk_score += 25
        elif glucose >= 100:
            risk_score += 15

        # Disease risk
        disease_risk_map = {
            'Normal': 0,
            'Asthma': 15,
            'Hypertension': 20,
            'Diabetes': 25,
            'Heart Risk': 30
        }
        risk_score += disease_risk_map.get(disease, 0)

        # Normalize
        risk_score = min(100, max(0, risk_score))
        risk_probability = risk_score / 100

        return jsonify({
            "risk_score": round(risk_score, 2),
            "risk_probability": round(risk_probability, 4),
            "is_high_risk": risk_probability >= 0.5,
            "risk_level": "HIGH" if risk_probability >= 0.5 else "LOW"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/api/patient-profile/<int:patient_id>')
def get_patient_profile(patient_id):
    """Get detailed profile for a specific patient"""
    if engineered_data is None:
        return jsonify({"error": "Dataset not found"}), 404

    patient = engineered_data[engineered_data['Patient_ID'] == patient_id]

    if len(patient) == 0:
        return jsonify({"error": f"Patient {patient_id} not found"}), 404

    patient_dict = patient.iloc[0].to_dict()

    return jsonify({
        "patient": {k: (float(v) if isinstance(v, (np.floating, np.integer)) else v)
                    for k, v in patient_dict.items()}
    })


@app.route('/api/summary')
def get_summary():
    """Get overall summary statistics"""
    if engineered_data is None:
        return jsonify({"error": "Dataset not found"}), 404

    summary = {
        "total_patients": len(engineered_data),
        "high_risk_patients": len(engineered_data[engineered_data['Risk_Score'] >= 60]),
        "average_age": float(engineered_data['Age'].mean()),
        "average_bmi": float(engineered_data['BMI'].mean()),
        "average_bp": float(engineered_data['Blood_Pressure'].mean()),
        "average_glucose": float(engineered_data['Glucose'].mean()),
        "average_health_score": float(engineered_data['Health_Score'].mean() if 'Health_Score' in engineered_data.columns else 0),
        "average_risk_score": float(engineered_data['Risk_Score'].mean() if 'Risk_Score' in engineered_data.columns else 0),
        "diseases": engineered_data['Disease_Risk'].value_counts().to_dict()
    }

    return jsonify(summary)


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({"error": "Internal server error"}), 500


if __name__ == '__main__':
    # Enable debug mode for development
    app.run(debug=True, host='0.0.0.0', port=5000)
