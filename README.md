# 🛡️ Advanced Predictive Infrastructure Failure Detector

An end-to-end MLOps industrial streaming pipeline designed to monitor infrastructure health telemetry and predict structural failures in real time using an **XGBoost Classifier machine learning core**.

## 🏗️ Architecture Blueprint
- **IoT Telemetry Layer:** Simulates real-time hardware telemetry variations (Vibration, Temperature, Voltage).
- **Backend Microservices:** A **FastAPI** application engine hosting pre-trained ML modeling matrices.
- **MLOps/AI Engine:** An **XGBoost Classifier** combined with `StandardScaler` transformations achieving a ~99% testing metric profile.
- **Frontend Command Room:** A live, dynamic **Streamlit** tracking room visualizing historical data streams and anomaly risk tracking arrays.

## 🚀 Deployment Instructions
1. Clone the project matrix framework.
2. Initialize and configure dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run model compilation configurations:
   ```bash
   python src/train.py
   ```
4. Fire up deployment servers:
   ```bash
   uvicorn src.app:app --reload
   streamlit run dashboard/UI.py
   ```
