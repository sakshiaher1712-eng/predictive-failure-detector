import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
import joblib
import os

def generate_historical_dataset(num_samples=5000):
    """Generates synthetic historical industrial telemetry data with explicit failure states."""
    print("📦 Generating historical machine telemetry datasets...")
    np.random.seed(42)
    
    # Generate healthy baseline behaviors
    vibration = np.random.uniform(20.0, 45.0, num_samples)
    temperature = np.random.uniform(65.0, 95.0, num_samples)
    voltage = np.random.uniform(210.0, 240.0, num_samples)
    
    # 0 = Healthy, 1 = Mechanical Failure
    labels = np.zeros(num_samples)
    
    # Inject failure anomalies (representing severe imbalances/fault conditions)
    # 8% of the historical data will represent hardware degradation
    anomaly_indices = np.random.choice(num_samples, int(num_samples * 0.08), replace=False)
    
    for idx in anomaly_indices:
        failure_type = np.random.choice(['bearing_wear', 'overheating', 'voltage_drop'])
        if failure_type == 'bearing_wear':
            vibration[idx] = np.random.uniform(65.0, 95.0)
            temperature[idx] = np.random.uniform(85.0, 105.0)
        elif failure_type == 'overheating':
            temperature[idx] = np.random.uniform(112.0, 135.0)
            vibration[idx] = np.random.uniform(40.0, 60.0)
        elif failure_type == 'voltage_drop':
            voltage[idx] = np.random.uniform(150.0, 178.0)
            vibration[idx] = np.random.uniform(45.0, 70.0)
            
        labels[idx] = 1 # Mark as failed/anomalous record
        
    df = pd.DataFrame({
        'vibration_vrms': vibration,
        'temperature_celsius': temperature,
        'voltage_v': voltage,
        'failure_target': labels
    })
    
    # Save the raw training baseline data to our data folder
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/historical_telemetry.csv', index=False)
    print("💾 Historical metrics successfully exported to 'data/historical_telemetry.csv'")
    return df

def train_infrastructure_model():
    # 1. Fetch and parse our generated dataset
    df = generate_historical_dataset()
    
    X = df[['vibration_vrms', 'temperature_celsius', 'voltage_v']]
    y = df['failure_target']
    
    # 2. Divide data into Training (80%) and Test (20%) tracking subsets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    # 3. Standardize sensor scales for optimal matrix modeling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # 4. Train the advanced XGBoost Classifier architecture
    print("🧠 Initializing and training the XGBoost Classifier...")
    model = XGBClassifier(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        random_state=42,
        use_label_encoder=False,
        eval_metric='logloss'
    )
    model.fit(X_train_scaled, y_train)
    
    # Evaluate baseline accuracy metrics
    accuracy = model.score(X_test_scaled, y_test)
    print(f"🎯 Model training complete! Validation Testing Accuracy Score: {accuracy * 100:.2f}%")
    
    # 5. Serialize and export files so our FastAPI backend server can load them live
    os.makedirs('src/models', exist_ok=True)
    joblib.dump(model, 'src/models/failure_detector_model.pkl')
    joblib.dump(scaler, 'src/models/feature_scaler.pkl')
    print("💾 AI Model components successfully serialized and saved to 'src/models/'")

if __name__ == "__main__":
    train_infrastructure_model()
