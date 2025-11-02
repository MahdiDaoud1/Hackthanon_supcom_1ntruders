# ===================================================================
# Project:   Smart Farm - Flask Server (v2 - with Warning State)
#
# Role:      Receives raw data, applies 3-state logic, and serves
#            the processed status (0=OK, 1=DRY, 2=WARN).
# ===================================================================

from flask import Flask, request, jsonify

app = Flask(__name__)

# === Logic and Storage ===
# We now have TWO thresholds per plant
TOMATO_THRESHOLD_DRY = 3000
TOMATO_THRESHOLD_WARN = 2700  # Warning level (must be < DRY)

ONION_THRESHOLD_DRY = 2500
ONION_THRESHOLD_WARN = 2200

MINT_THRESHOLD_DRY = 2000
MINT_THRESHOLD_WARN = 1800

# This file will store the final status (e.g., "1,0,2")
STATUS_FILE = "plant_status.txt"

@app.route('/')
def home():
    return "Smart Farm Server is Running (v2)"

#
# ENDPOINT 1: For the Field Node to POST raw data
#
@app.route('/update_raw', methods=['POST'])
def update_raw_data():
    try:
        rawData = request.data.decode('utf-8')
        print(f"[LOG] Received raw data: {rawData}")

        parts = rawData.split(',')
        if len(parts) != 3:
            return "Bad data format", 400

        tomatoVal = int(parts[0])
        onionVal = int(parts[1])
        mintVal = int(parts[2])

        # --- New 3-State Server-Side Logic ---
        
        # Tomato
        if tomatoVal > TOMATO_THRESHOLD_DRY:
            tomatoStatus = 1  # Dry
        elif tomatoVal > TOMATO_THRESHOLD_WARN:
            tomatoStatus = 2  # Warning
        else:
            tomatoStatus = 0  # OK

        # Onion
        if onionVal > ONION_THRESHOLD_DRY:
            onionStatus = 1
        elif onionVal > ONION_THRESHOLD_WARN:
            onionStatus = 2
        else:
            onionStatus = 0

        # Mint
        if mintVal > MINT_THRESHOLD_DRY:
            mintStatus = 1
        elif mintVal > MINT_THRESHOLD_WARN:
            mintStatus = 2
        else:
            mintStatus = 0

        # Create the final, processed status string
        finalStatus = f"{tomatoStatus},{onionStatus},{mintStatus}"
        print(f"[LOG] Processed status: {finalStatus}")

        # Save the final status to the file
        with open(STATUS_FILE, 'w') as f:
            f.write(finalStatus)

        return "Data received and processed", 200

    except Exception as e:
        print(f"[ERROR] {e}")
        return "Internal server error", 500

#
# ENDPOINT 2: For the Home Node to GET the processed status
#
@app.route('/get_status', methods=['GET'])
def get_status():
    try:
        with open(STATUS_FILE, 'r') as f:
            status = f.read().strip()
        return status, 200, {'Content-Type': 'text/plain'}
    except FileNotFoundError:
        return "0,0,0", 200, {'Content-Type': 'text/plain'}
    except Exception as e:
        print(f"[ERROR] {e}")
        return "Internal server error", 500

#
# Run the server
#
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)