from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
import pandas as pd
import joblib
import os

# Initialize the FastAPI core application
app = FastAPI(title="ML-Powered Predictive Infrastructure Failure Detector API")

# Define file paths to our exported model artifacts
MODEL_PATH = "src/models/failure_detector_model.pkl"
SCALER_PATH = "src/models/feature_scaler.pkl"

# Check if model files exist before starting the server application
if not os.path.exists(MODEL_PATH) or not os.path.exists(SCALER_PATH):
    raise FileNotFoundError("❌ AI model components not found! Please run 'python src/train.py' first.")

# Load the trained XGBoost model and Feature Scaler binary assets into runtime memory
print("🧠 Loading trained XGBoost and Scaler binary components into server memory...")
ml_model = joblib.load(MODEL_PATH)
feature_scaler = joblib.load(SCALER_PATH)
print("✅ Core model architecture successfully operational.")

# Define the incoming data schema
class SensorTelemetry(BaseModel):
    machine_id: str
    timestamp: str
    vibration_vrms: float
    temperature_celsius: float
    voltage_v: float

@app.get("/")
def home():
    return {"status": "online", "message": "Production ML Inference Engine Online"}

@app.post("/predict")
def predict_failure(data: SensorTelemetry):
    """
    Receives real-time streaming hardware signals, standardizes features,
    and uses the XGBoost model to predict failures dynamically.
    """
    try:
        # 1. Structure the raw data into a DataFrame format matching training features
        input_data = pd.DataFrame([{
            'vibration_vrms': data.vibration_vrms,
            'temperature_celsius': data.temperature_celsius,
            'voltage_v': data.voltage_v
        }])
        
        # 2. Apply standard scaling normalization exactly like training phase
        scaled_features = feature_scaler.transform(input_data)
        
        # 3. Predict probability scores ([Healthy Probability, Failure Probability])
        prediction_probabilities = ml_model.predict_proba(scaled_features)[0]
        failure_prob = float(prediction_probabilities[1]) # Extract the exact breakdown risk percentage
        
        # 4. Generate classifications based on standard 50% operational thresholds
        is_anomaly = True if failure_prob >= 0.50 else False
        
        # Assign contextual warning descriptions for operational workers
        if failure_prob < 0.30:
            status = "Normal Operations - System stable."
        elif failure_prob < 0.70:
            status = "WARNING: Minor anomaly patterns forming. Monitor telemetry closely."
        else:
            status = "CRITICAL FAILURE RISK: High breakdown signature detected! Maintenance required immediately."

        return {
            "machine_id": data.machine_id,
            "processed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "is_anomaly": is_anomaly,
            "failure_probability": round(failure_prob, 4),
            "operational_status": status
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference Pipeline Exception Error: {str(e)}")
