from flask import Flask, request
import redis
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # <-- This gives your website permission

# === Database Connection ===
redis_url = os.environ.get('REDIS_URL') # <-- Correct for Vercel
try:
    r = redis.from_url(redis_url)
    r.ping()
    print(f"Connected to Redis at {redis_url}")
except Exception as e:
    print(f"CRITICAL: Could not connect to Redis. {e}")
    r = None 

# === REDIS KEYS ===
PLANT_STATUS_KEY = "plant_status"
VALVE_STATUS_KEY = "valve_status"
MANUAL_COMMAND_KEY = "manual_command"

# ===================================================================
# !!! THIS IS THE LOGIC THAT WAS MISSING BEFORE !!!
# ===================================================================
# These are the thresholds for your sensors
# (HIGH value = DRY, LOW value = WET)
TOMATO_THRESHOLD_DRY = 3000
TOMATO_THRESHOLD_WARN = 2700
ONION_THRESHOLD_DRY = 2500
ONION_THRESHOLD_WARN = 2200
MINT_THRESHOLD_DRY = 2000
MINT_THRESHOLD_WARN = 1800
# ===================================================================


@app.route('/')
def home():
    return "Smart Farm Server is Running (v5.1 - Corrected)"

@app.route('/update_raw', methods=['POST'])
def update_raw_data():
    if not r: return "Server Error: DB not connected", 500
    try:
        rawData = request.data.decode('utf-8')
        print(f"[LOG] Received raw sensor data: {rawData}")
        parts = rawData.split(',')
        if len(parts) != 3: return "Bad data format", 400
        
        tomatoVal, onionVal, mintVal = int(parts[0]), int(parts[1]), int(parts[2])

        # --- Calculate 3-state logic ---
        if tomatoVal > TOMATO_THRESHOLD_DRY: tomatoStatus = 1
        elif tomatoVal > TOMATO_THRESHOLD_WARN: tomatoStatus = 2
        else: tomatoStatus = 0
        
        if onionVal > ONION_THRESHOLD_DRY: onionStatus = 1
        elif onionVal > ONION_THRESHOLD_WARN: onionStatus = 2
        else: onionStatus = 0

        if mintVal > MINT_THRESHOLD_DRY: mintStatus = 1
        elif mintVal > MINT_THRESHOLD_WARN: mintStatus = 2
        else: mintStatus = 0

        finalStatus = f"{tomatoStatus},{onionStatus},{mintStatus}"
        print(f"[LOG] Processed status to: {finalStatus}")
        
        # --- Save the new status to Redis ---
        r.set(PLANT_STATUS_KEY, finalStatus)
        
        return "Data received and processed", 200
    except Exception as e:
        print(f"[ERROR] update_raw: {e}")
        return "Internal server error", 500

@app.route('/get_status', methods=['GET'])
def get_status():
    if not r: return "Server Error: DB not connected", 500
    try:
        status_bytes = r.get(PLANT_STATUS_KEY)
        if status_bytes is None: return "0,0,0", 200
        return status_bytes.decode('utf-8'), 200
    except Exception as e:
        print(f"[ERROR] get_status: {e}")
        return "0,0,0", 500

@app.route('/valve_status', methods=['GET', 'POST'])
def valve_status():
    if not r: return "Server Error: DB not connected", 500
    if request.method == 'POST':
        try:
            status = request.data.decode('utf-8')
            r.set(VALVE_STATUS_KEY, status)
            return "Status received", 200
        except Exception as e:
            return "Internal server error", 500
    elif request.method == 'GET':
        try:
            status_bytes = r.get(VALVE_STATUS_KEY)
            if status_bytes is None: return "UNKNOWN", 200
            return status_bytes.decode('utf-8'), 200
        except Exception as e:
            return "UNKNOWN", 500

@app.route('/manual_command', methods=['GET', 'POST'])
def manual_command():
    if not r: return "Server Error: DB not connected", 500
    if request.method == 'POST':
        try:
            command = request.data.decode('utf-8')
            r.set(MANUAL_COMMAND_KEY, command, ex=30) 
            return "Command received", 200
        except Exception as e:
            return "Internal server error", 500
    elif request.method == 'GET':
        try:
            command_bytes = r.get(MANUAL_COMMAND_KEY)
            if command_bytes is None: return "NONE", 200
            r.delete(MANUAL_COMMAND_KEY)
            return command_bytes.decode('utf-8'), 200
        except Exception as e:
            return "NONE", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)