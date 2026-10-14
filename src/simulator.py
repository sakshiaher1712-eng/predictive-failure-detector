import time
import random
import requests

# The URL where our AI backend server will listen for live data
API_URL = "http://127.0.0"

def generate_sensor_data(machine_id):
    """
    Simulates reading data from physical hardware sensors.
    """
    # Simulate a steady baseline with small random vibrations and temperatures
    vibration = round(random.uniform(20.0, 45.0), 2)
    temperature = round(random.uniform(65.0, 95.0), 2)
    voltage = round(random.uniform(210.0, 240.0), 2)
    
    # 5% chance to simulate a sudden dangerous hardware anomaly
    if random.random() < 0.05:
        vibration += random.uniform(30.0, 50.0)
        temperature += random.uniform(25.0, 40.0)
        voltage -= random.uniform(40.0, 60.0)

    payload = {
        "machine_id": f"MACH_{machine_id:03d}",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "vibration_vrms": vibration,
        "temperature_celsius": temperature,
        "voltage_v": voltage
    }
    return payload

def start_streaming():
    print("🚀 IoT Telemetry Simulator Started. Press Ctrl+C to stop.")
    machine_id = 101
    
    while True:
        # 1. Generate live data frame
        data_packet = generate_sensor_data(machine_id)
        print(f"📡 Sending data packet: {data_packet}")
        
        # 2. Try sending this data to our FastAPI AI server
        try:
            response = requests.post(API_URL, json=data_packet, timeout=2)
            print(f"✅ Response from Server: {response.json()}")
        except requests.exceptions.ConnectionError:
            print("❌ Server is offline. Retrying in next cycle...")
            
        # 3. Wait 2 seconds before reading the sensors again
        time.sleep(2)

if __name__ == "__main__":
    start_streaming()
