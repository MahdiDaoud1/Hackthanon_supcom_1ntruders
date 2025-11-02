/*
 * ===================================================================
 * Project:   Smart Farm - Automated Valve Controller (v2.1)
 *
 * Role:      - Checks for manual commands when IDLE.
 * - ALWAYS reports its current status every 5 seconds.
 * - Checks for automated watering every 15 minutes.
 * - Runs all watering cycles for 30 seconds.
 *
 * BUG FIX:   (v2.1) Moved reporting outside of the IDLE check
 * to ensure the server always receives the current state.
 * ===================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>

// === Wi-Fi & Server Config ===
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl_GetStatus = "https://hackthanonsupcom1ntruders.vercel.app/get_status";
const char* serverUrl_ValveStatus = "https://hackthanonsupcom1ntruders.vercel.app/valve_status";
const char* serverUrl_ManualCommand = "https://hackthanonsupcom1ntruders.vercel.app/manual_command";

// === Pin Definitions (Relays) ===
const int PUMP_PIN = 25;
const int VALVE_TOMATO_PIN = 26;
const int VALVE_ONION_PIN = 27;
const int VALVE_MINT_PIN = 14;

// === Timers ===
const long AUTO_CHECK_INTERVAL = 15 * 60 * 1000; // 15 minutes
const long MANUAL_CHECK_INTERVAL = 5000; // 5 seconds
const long WATERING_DURATION = 30000; // 30 seconds (for all cycles)

unsigned long lastAutoCheckMillis = 0;
unsigned long lastManualCheckMillis = 0;
unsigned long stateEntryMillis = 0; 

// === State Machine ===
enum State {
  IDLE,
  FETCHING_AUTO_DATA,
  WATERING_TOMATO,
  WATERING_ONION,
  WATERING_MINT,
  MANUAL_TOMATO, 
  MANUAL_ONION,  
  MANUAL_MINT    
};
State currentState = IDLE;

// === Global Status Variables ===
int tomatoStatus = 0;
int onionStatus = 0;
int mintStatus = 0;

// Function Prototypes
void connectToWiFi();
void allValvesOff();
void getAutomatedStatus();
void checkCommandsAndReport();
String stateToString(State state);

/*
 * ===================================================================
 * SETUP
 * ===================================================================
 */
void setup() {
  Serial.begin(115200);
  Serial.println("Valve Controller (v2.1): Booting...");

  pinMode(PUMP_PIN, OUTPUT);
  pinMode(VALVE_TOMATO_PIN, OUTPUT);
  pinMode(VALVE_ONION_PIN, OUTPUT);
  pinMode(VALVE_MINT_PIN, OUTPUT);

  allValvesOff();
  connectToWiFi();

  // Stagger timers
  lastAutoCheckMillis = millis() - AUTO_CHECK_INTERVAL + 10000; // First check in 10s
  lastManualCheckMillis = millis();
}

/*
 * ===================================================================
 * LOOP - The State Machine
 * ===================================================================
 */
void loop() {
  unsigned long currentMillis = millis();

  // --- WiFi Connection Check ---
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("WiFi Disconnected. Reconnecting...");
    connectToWiFi();
    delay(1000);
    return;
  }

  // --- SHORT TIMER (5 seconds) ---
  if (currentMillis - lastManualCheckMillis >= MANUAL_CHECK_INTERVAL) {
    lastManualCheckMillis = currentMillis;
    // This function now runs EVERY 5 seconds to report status
    // and check for commands.
    checkCommandsAndReport();
  }

  // --- LONG TIMER (15 minutes) ---
  if (currentMillis - lastAutoCheckMillis >= AUTO_CHECK_INTERVAL) {
    lastAutoCheckMillis = currentMillis;
    if (currentState == IDLE) { // Only run if not already in a cycle
      currentState = FETCHING_AUTO_DATA;
      Serial.println("Auto-Timer up. Checking server for status...");
    }
  }

  // --- State Machine Logic ---
  switch (currentState) {

    case IDLE:
      // Do nothing, wait for timers
      break;

    case FETCHING_AUTO_DATA:
      getAutomatedStatus(); 
      if (tomatoStatus == 1) {
        currentState = WATERING_TOMATO;
        stateEntryMillis = currentMillis;
        Serial.println("Tomato is DRY. Starting auto cycle.");
      } else if (onionStatus == 1) {
        currentState = WATERING_ONION;
        stateEntryMillis = currentMillis;
        Serial.println("Onion is DRY. Starting auto cycle.");
      } else if (mintStatus == 1) {
        currentState = WATERING_MINT;
        stateEntryMillis = currentMillis;
        Serial.println("Mint is DRY. Starting auto cycle.");
      } else {
        currentState = IDLE;
        Serial.println("All plants OK. Returning to IDLE.");
      }
      break;

    // --- AUTOMATED CYCLES (30 seconds) ---
    case WATERING_TOMATO:
      digitalWrite(PUMP_PIN, HIGH);
      digitalWrite(VALVE_TOMATO_PIN, HIGH);
      if (currentMillis - stateEntryMillis >= WATERING_DURATION) {
        allValvesOff();
        tomatoStatus = 0; // Mark as watered
        Serial.println("Auto Tomato watering complete.");
        // Check next plant
        if (onionStatus == 1) {
          currentState = WATERING_ONION;
          stateEntryMillis = currentMillis;
        } else if (mintStatus == 1) {
          currentState = WATERING_MINT;
          stateEntryMillis = currentMillis;
        } else {
          currentState = IDLE;
        }
      }
      break;

    case WATERING_ONION:
      digitalWrite(PUMP_PIN, HIGH);
      digitalWrite(VALVE_ONION_PIN, HIGH);
      if (currentMillis - stateEntryMillis >= WATERING_DURATION) {
        allValvesOff();
        onionStatus = 0; // Mark as watered
        Serial.println("Auto Onion watering complete.");
        if (mintStatus == 1) {
          currentState = WATERING_MINT;
          stateEntryMillis = currentMillis;
        } else {
          currentState = IDLE;
        }
      }
      break;

    case WATERING_MINT:
      digitalWrite(PUMP_PIN, HIGH);
      digitalWrite(VALVE_MINT_PIN, HIGH);
      if (currentMillis - stateEntryMillis >= WATERING_DURATION) {
        allValvesOff();
        mintStatus = 0; // Mark as watered
        Serial.println("Auto Mint watering complete.");
        currentState = IDLE;
      }
      break;

    // --- MANUAL CYCLES (30 seconds) ---
    case MANUAL_TOMATO:
      Serial.println("MANUAL cycle: TOMATO");
      digitalWrite(PUMP_PIN, HIGH);
      digitalWrite(VALVE_TOMATO_PIN, HIGH);
      if (currentMillis - stateEntryMillis >= WATERING_DURATION) {
        allValvesOff();
        Serial.println("Manual Tomato cycle complete.");
        currentState = IDLE;
      }
      break;

    case MANUAL_ONION:
      Serial.println("MANUAL cycle: ONION");
      digitalWrite(PUMP_PIN, HIGH);
      digitalWrite(VALVE_ONION_PIN, HIGH);
      if (currentMillis - stateEntryMillis >= WATERING_DURATION) {
        allValvesOff();
        Serial.println("Manual Onion cycle complete.");
        currentState = IDLE;
      }
      break;
      
    case MANUAL_MINT:
      Serial.println("MANUAL cycle: MINT");
      digitalWrite(PUMP_PIN, HIGH);
      digitalWrite(VALVE_MINT_PIN, HIGH);
      if (currentMillis - stateEntryMillis >= WATERING_DURATION) {
        allValvesOff();
        Serial.println("Manual Mint cycle complete.");
        currentState = IDLE;
      }
      break;
  }
}

/*
 * ===================================================================
 * HELPER: allValvesOff()
 * ===================================================================
 */
void allValvesOff() {
  digitalWrite(PUMP_PIN, LOW);
  digitalWrite(VALVE_TOMATO_PIN, LOW);
  digitalWrite(VALVE_ONION_PIN, LOW);
  digitalWrite(VALVE_MINT_PIN, LOW);
  Serial.println("All valves and pump are OFF.");
}

/*
 * ===================================================================
 * HELPER: stateToString()
 * ===================================================================
 */
String stateToString(State state) {
  switch (state) {
    case IDLE: return "IDLE";
    case FETCHING_AUTO_DATA: return "FETCHING_DATA";
    case WATERING_TOMATO: return "WATERING_TOMATO";
    case WATERING_ONION: return "WATERING_ONION";
    case WATERING_MINT: return "WATERING_MINT";
    case MANUAL_TOMATO: return "MANUAL_TOMATO";
    case MANUAL_ONION: return "MANUAL_ONION";
    case MANUAL_MINT: return "MANUAL_MINT";
    default: return "UNKNOWN";
  }
}

/*
 * ===================================================================
 * connectToWiFi()
 * ===================================================================
 */
void connectToWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi Connected!");
  } else {
    Serial.println("\nFailed to connect to WiFi.");
  }
}

/*
 * ===================================================================
 * getAutomatedStatus()
 * (This is for the 15-minute automated check)
 * ===================================================================
 */
void getAutomatedStatus() {
  if (WiFi.status() != WL_CONNECTED) return;
  
  HTTPClient http;
  http.begin(serverUrl_GetStatus);
  int httpResponseCode = http.GET();

  if (httpResponseCode == HTTP_CODE_OK) {
    String payload = http.getString();
    payload.trim();
    Serial.print("Auto-Check: Server response: '");
    Serial.print(payload);
    Serial.println("'");

    if (payload.length() >= 5) {
      tomatoStatus = payload.charAt(0) - '0';
      onionStatus = payload.charAt(2) - '0';
      mintStatus = payload.charAt(4) - '0';
      Serial.println("Auto-Status variables updated.");
    }
  } else {
    Serial.print("Error on HTTP GET (Auto-Status): ");
    Serial.println(httpResponseCode);
  }
  http.end();
}

/*
 * ===================================================================
 * checkCommandsAndReport()
 * (This runs every 5 seconds)
 * ===================================================================
 */
void checkCommandsAndReport() {
  if (WiFi.status() != WL_CONNECTED) return;
  
  HTTPClient http;
  
  // --- 1. Report our current status to the server ---
  http.begin(serverUrl_ValveStatus);
  http.addHeader("Content-Type", "text/plain");
  String statusPayload = stateToString(currentState);
  int httpResponseCode = http.POST(statusPayload);
  
  if (httpResponseCode > 0) {
    Serial.print("Reported status '");
    Serial.print(statusPayload);
    Serial.println("' to server.");
  } else {
    Serial.print("Error reporting status: ");
    Serial.println(httpResponseCode);
  }
  http.end(); // End this HTTP request

  // --- 2. Check for commands ONLY if we are IDLE ---
  if (currentState == IDLE) {
    http.begin(serverUrl_ManualCommand);
    httpResponseCode = http.GET();

    if (httpResponseCode == HTTP_CODE_OK) {
      String command = http.getString();
      command.trim();
      
      if (command != "NONE") {
        Serial.print("!!! MANUAL COMMAND RECEIVED: ");
        Serial.println(command);
        
        // --- Act on the command ---
        if (command == "TOMATO_ON") {
          currentState = MANUAL_TOMATO;
          stateEntryMillis = millis(); // Start 30-sec timer
        } else if (command == "ONION_ON") {
          currentState = MANUAL_ONION;
          stateEntryMillis = millis();
        } else if (command == "MINT_ON") {
          currentState = MANUAL_MINT;
          stateEntryMillis = millis();
        } else if (command == "ALL_OFF") {
          allValvesOff();
          currentState = IDLE; // We are already IDLE, but good to confirm
        }
      } else {
        Serial.println("No manual commands.");
      }
    } else {
      Serial.print("Error checking for commands: ");
      Serial.println(httpResponseCode);
    }
    http.end(); // End this HTTP request
  }
}