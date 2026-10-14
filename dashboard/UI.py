import streamlit as st
import requests
import time
import pandas as pd
from datetime import datetime

# Set up the browser tab config
st.set_page_config(page_title="Infrastructure Health Dashboard", layout="wide")

# Configure backend targets
API_URL = "http://127.0.0"

# Set up the title element
st.title("🛡️ Predictive Infrastructure Failure Detector")
st.markdown("---")

# Initialize session storage to remember data frames across UI page refreshes
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar configurations
st.sidebar.header("🛠️ Simulation Controls")
poll_rate = st.sidebar.slider("Sensor Refresh Interval (seconds)", 1, 5, 2)
clear_button = st.sidebar.button("Clear Log History")

if clear_button:
    st.session_state.history = []
    st.success("History cache cleared!")

# Set up visual containers for streaming metrics
live_status_box = st.empty()
metric_columns = st.columns(3)
chart_container = st.empty()

# Helper function to generate mock telemetry that matches what the simulator would push
def fetch_mock_sensor_telemetry():
    import random
    vibration = round(random.uniform(20.0, 75.0), 2)  # Expanded range to deliberately trigger anomalies occasionally
    temperature = round(random.uniform(65.0, 115.0), 2)
    voltage = round(random.uniform(175.0, 240.0), 2)
    
    return {
        "machine_id": "MACH_101",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "vibration_vrms": vibration,
        "temperature_celsius": temperature,
        "voltage_v": voltage
    }

# Infinite UI loop that continuously fetches data frames and redraws components
while True:
    # 1. Fetch live telemetry metrics from sensor layer
    raw_payload = fetch_mock_sensor_telemetry()
    
    # 2. Request prediction analysis from our running FastAPI application
    try:
        response = requests.post(API_URL, json=raw_payload, timeout=2)
        result = response.json()
        
        # Merge telemetry values with prediction scores for our data history
        combined_record = {**raw_payload, **result}
        st.session_state.history.append(combined_record)
        
        # Limit cache size to the latest 20 readings to keep the app highly responsive
        if len(st.session_state.history) > 20:
            st.session_state.history.pop(0)
            
        df = pd.DataFrame(st.session_state.history)
        
        # 3. Update Operational Health Alert Banner
        is_anomaly = result["is_anomaly"]
        if is_anomaly:
            live_status_box.error(f"🚨 **{result['operational_status']}** (Risk Probability: {result['failure_probability']*100:.1f}%)")
        else:
            live_status_box.success(f"✅ **System Status:** Operational. {result['operational_status']} (Risk Probability: {result['failure_probability']*100:.1f}%)")
            
        # 4. Render Live Snapshot Numeric Gauges
        with metric_columns[0]:
            st.metric("Vibration (VRMS)", f"{raw_payload['vibration_vrms']} mm/s", delta="Critical Value >60" if raw_payload['vibration_vrms'] > 60 else None, delta_color="inverse")
        with metric_columns[1]:
            st.metric("Temperature", f"{raw_payload['temperature_celsius']} °C", delta="Critical Value >110" if raw_payload['temperature_celsius'] > 110 else None, delta_color="inverse")
        with metric_columns[2]:
            st.metric("Supply Voltage", f"{raw_payload['voltage_v']} V", delta="Low Voltage <180" if raw_payload['voltage_v'] < 180 else None, delta_color="inverse")
            
        # 5. Render Historical Trend Graph for Monitoring Analytics
        with chart_container.container():
            st.subheader("📈 Live Telemetry Sensor History")
            st.line_chart(df.set_index("timestamp")[["vibration_vrms", "temperature_celsius"]])
            
    except requests.exceptions.ConnectionError:
        live_status_box.warning("⚠️ Waiting to connect with the backend FastAPI engine... Make sure app.py is running on port 8000.")
        
    time.sleep(poll_rate)
