# Smart Farm IoT Project

This project is a complete IoT system for monitoring and automating a small farm (Tomato, Onion, Mint). It uses ESP32 microcontrollers for field sensors and valve control, and a central server built with Flask and Redis (deployed on Vercel) to act as the "brain." A web-based dashboard allows for remote monitoring and manual control.

## 🏛️ Project Architecture

The system is split into five main components:

1. **Field Node (Emetteur):** An ESP32 with sensors that wakes up periodically to send moisture data.
2. **The Server (Flask/Redis):** A web server on Vercel that receives data, processes it, and stores the current status.
3. **Mission 1 (LED Display):** An ESP32 in the home that displays the plant status on LEDs.
4. **Mission 2 (Pump Controller):** An ESP32 connected to relays that controls the water pump and valves.
5. **Mission 3 (Web Dashboard):** An HTML/CSS/JS website to monitor the farm and manually turn on the water.

### Data Flow Diagram

[Field Node] --(POST raw data)--> [Server] --> [Redis DB]
^
|
[LED Display (Mission 1)] <--(GET status)--- [Server]
^
|
[Pump Controller (Mission 2)] <-(GET/POST)--> [Server]
^
|
[Web Dashboard (Mission 3)] <-(GET/POST)--> [Server]

text

---

## 📁 Project Structure

.
├── hackathon/ # Folder for the Server
│ ├── app.py # The main Flask server
│ ├── requirements.txt # Vercel dependencies
│ └── vercel.json # Vercel deployment config
│
├── mission1/ # Folder for the Home LED Display
│ └── mission1.ino # Code for the LED Display ESP32
│
├── mission2/ # Folder for the Pump Controller
│ └── mission2.ino # Code for the Pump/Valve ESP32
│
├── mission3/ # Folder for the Web Dashboard
│ ├── index.html # The website structure
│ ├── style.css # The website style
│ └── app.js # The website logic
│
├── Emetteur.ino # Code for the Field Sensor ESP32
└── test_client.py # Python script for simulating hardware

text

---

## ⚙️ Component Details

### 1. The Server (`app.py`)

This is the central "brain" of the operation, built with Python and Flask.

- **Technology:** Flask, Redis (Vercel KV), Vercel
- **Purpose:** To be a stateless "message board" or database. It does **not** contain any timers or loops
- **Endpoints:**
  - `/update_raw` (POST): Called by the **Field Node**. Receives raw sensor values and converts them to status codes
  - `/get_status` (GET): Called by **Mission 1** and **Mission 2**. Returns current plant status
  - `/valve_status` (POST/GET): Used by **Mission 2** and **Mission 3** for pump status communication
  - `/manual_command` (POST/GET): The "mailbox" for manual control commands

### 2. The Field Node (`Emetteur.ino`)

- **Hardware:** ESP32, 3x Capacitive Moisture Sensors
- **Logic:**
  1. Wakes up from 5-minute deep sleep
  2. Connects to Wi-Fi
  3. Reads raw analog values from 3 sensors
  4. POSTs data to server's `/update_raw` endpoint
  5. Goes back to deep sleep to save battery

### 3. Mission 1: Home LED Display

- **Hardware:** ESP32, 3x LEDs (one for each plant)
- **Wokwi Simulation:** [https://wokwi.com/projects/446471362041217025](https://wokwi.com/projects/446471362041217025)
- **Logic:**
  1. Connects to Wi-Fi
  2. In a 10-second loop, GETs status from `/get_status`
  3. Updates LEDs based on status:
     - `0` (Wet): LED **OFF**
     - `1` (Dry): LED **SOLID ON**
     - `2` (Warn): LED **BLINKING**

### 4. Mission 2: Pump & Valve Controller

The "smartest" hardware component, responsible for all timers and physical action.

- **Hardware:** ESP32, 4-Channel Relay Module (1 pump + 3 valves)
- **Logic:** Runs a state machine with two independent timers
  - **Automated Timer (15 minutes):**
    1. GETs status from `/get_status`
    2. If all dry, begins sequential watering cycle
    3. Cycles through each plant with 30-second watering
  - **Reporting Timer (5 seconds):**
    1. POSTs current state to `/valve_status`
    2. Checks `/manual_command` for manual control commands

### 5. Mission 3: Web Control Board

- **Technology:** HTML, CSS, JavaScript
- **Logic:**
  1. Communicates **only** with the Vercel server
  2. GETs from `/get_status` every 5 seconds for plant status
  3. GETs from `/valve_status` every 5 seconds for pump status
  4. Disables buttons when pump is active to prevent conflicts
  5. POSTs commands to `/manual_command` when user clicks buttons

---

## 🎮 Wokwi Simulation

A working simulation of **Mission 1 (LED Display)** is available on Wokwi:

🔗 **Simulation Link:** [https://wokwi.com/projects/446471362041217025](https://wokwi.com/projects/446471362041217025)

**Simulation Components:**

- ESP32 microcontroller
- 3x Potentiometers (simulating moisture sensors)
- 3x LEDs (Red, Green, Blue for Tomato, Onion, Mint)
- Resistors and wiring

**How it works in simulation:**

- Potentiometers simulate soil moisture readings
- ESP32 reads potentiometer values and sends them to the server
- Server processes the data and returns status codes
- LEDs display the plant status based on server response
- Provides an oversimplified but functional demonstration of Mission 1

---

## 🚀 How to Run & Test

### 1. Deploy the Server

1. Ensure your `hackathon` folder has the final files
2. From the `hackathon` folder, run `vercel --prod`
3. Vercel will give you a **new production URL**

### 2. Update the Clients

1. **Web (`app.js`):** Paste the new Vercel URL into the `VERCEL_BASE_URL` variable
2. **ESP32s:** Paste the new Vercel URL into all three ESP32 `.ino` files and re-upload
3. **Wokwi Simulation:** Update the server URL in the Wokwi code

### 3. Run the Website

1. Navigate to the `mission3` folder: `cd mission3`
2. Run a local server: `python -m http.server 8000`
3. Open browser to `http://localhost:8000`

### 4. Test with Wokwi Simulation

1. Open the Wokwi simulation: [https://wokwi.com/projects/446471362041217025](https://wokwi.com/projects/446471362041217025)
2. Adjust potentiometers to simulate different moisture levels
3. Observe LED behavior changes based on server responses
4. Watch real-time updates on the web dashboard

### 5. Simulate the Hardware

1. Run `test_client.py` script with the new Vercel URL
2. Use **Option 1** to send sensor data
3. Use **Option 7** or **8** to simulate watering cycles
4. Watch both the website and Wokwi simulation update in real-time

---

## 🔧 Technical Specifications

- **Microcontroller:** ESP32 (x3)
- **Sensors:** Capacitive Soil Moisture Sensors (x3) - Simulated with potentiometers in Wokwi
- **Actuators:** 4-Channel Relay Module, Solenoid Valves (x3), Water Pump
- **Server:** Flask + Redis on Vercel
- **Communication:** HTTP REST API
- **Power Management:** Deep Sleep for field nodes
- **Update Intervals:**
  - Field Sensors: 5 minutes
  - LED Display: 10 seconds
  - Pump Controller: 15 minutes (auto), 5 seconds (manual check)
  - Web Dashboard: 5 seconds
- **Simulation Platform:** Wokwi for Mission 1 demonstration
