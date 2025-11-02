/*
 * ===================================================================
 * Project:   Smart Farm - Home Display Node (v2 - Blinking LEDs)
 *
 * Role:      Fetches 3-state status (0=OK, 1=DRY, 2=WARN)
 * and controls LEDs (OFF, ON, Blinking).
 * ===================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>

// === Wi-Fi & Server Config ===
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverUrl = "http://YOUR_SERVER_IP_OR_DOMAIN:5000/get_status";

// === Pin Definitions ===
const int TOMATO_LED_PIN = 25;
const int ONION_LED_PIN = 26;
const int MINT_LED_PIN = 27;

// === HTTP Check Timing ===
const long HTTP_INTERVAL = 10000; // Check server every 10 seconds
unsigned long previousHttpMillis = 0;

// === Non-Blocking Blinker Timing ===
const long BLINK_INTERVAL = 500; // Blink speed (every 500ms)
unsigned long previousBlinkMillis = 0;
bool ledBlinkState = false; // Tracks the blinker (ON/OFF)

// === Global State Variables ===
// These store the *desired* state (0=OFF, 1=ON, 2=BLINK)
int tomatoLedState = 0;
int onionLedState = 0;
int mintLedState = 0;

// Function prototypes
void connectToWiFi();
void getIrrigationStatus();
void updateLedDisplay();

/*
 * ===================================================================
 * SETUP
 * ===================================================================
 */
void setup() {
  Serial.begin(115200);
  while (!Serial);
  Serial.println("Home Display Node (v2): Booting...");

  pinMode(TOMATO_LED_PIN, OUTPUT);
  pinMode(ONION_LED_PIN, OUTPUT);
  pinMode(MINT_LED_PIN, OUTPUT);

  digitalWrite(TOMATO_LED_PIN, LOW);
  digitalWrite(ONION_LED_PIN, LOW);
  digitalWrite(MINT_LED_PIN, LOW);
  
  connectToWiFi();
}

/*
 * ===================================================================
 * LOOP
 * ===================================================================
 */
void loop() {
  unsigned long currentMillis = millis();

  // --- Task 1: Check Server (runs every HTTP_INTERVAL) ---
  if (currentMillis - previousHttpMillis >= HTTP_INTERVAL) {
    previousHttpMillis = currentMillis;
    if (WiFi.status() == WL_CONNECTED) {
      getIrrigationStatus(); // This just *updates* the state variables
    } else if (WiFi.status() != WL_CONNECTED) {
      Serial.println("WiFi disconnected. Reconnecting...");
      connectToWiFi();
    }
  }

  // --- Task 2: Update Blinker (runs every BLINK_INTERVAL) ---
  if (currentMillis - previousBlinkMillis >= BLINK_INTERVAL) {
    previousBlinkMillis = currentMillis;
    ledBlinkState = !ledBlinkState; // Toggle blink state (true/false)
  }

  // --- Task 3: Update LEDs (runs *every* loop) ---
  // This function applies the stored states (0, 1, or 2)
  updateLedDisplay();
}

/*
 * ===================================================================
 * updateLedDisplay()
 * This function runs continuously in the loop to set the
 * physical LED pins based on the global state variables.
 * ===================================================================
 */
void updateLedDisplay() {
  // --- Tomato LED ---
  if (tomatoLedState == 1) {
    digitalWrite(TOMATO_LED_PIN, HIGH); // Solid ON
  } else if (tomatoLedState == 2) {
    digitalWrite(TOMATO_LED_PIN, ledBlinkState); // Blink
  } else {
    digitalWrite(TOMATO_LED_PIN, LOW); // Solid OFF
  }
  
  // --- Onion LED ---
  if (onionLedState == 1) {
    digitalWrite(ONION_LED_PIN, HIGH);
  } else if (onionLedState == 2) {
    digitalWrite(ONION_LED_PIN, ledBlinkState);
  } else {
    digitalWrite(ONION_LED_PIN, LOW);
  }
  
  // --- Mint LED ---
  if (mintLedState == 1) {
    digitalWrite(MINT_LED_PIN, HIGH);
  } else if (mintLedState == 2) {
    digitalWrite(MINT_LED_PIN, ledBlinkState);
  } else {
    digitalWrite(MINT_LED_PIN, LOW);
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
 * getIrrigationStatus()
 * This function just fetches the string from the server and
 * updates the global state variables. It does NOT control LEDs.
 * ===================================================================
 */
void getIrrigationStatus() {
  HTTPClient http;
  Serial.println("Fetching server status...");
  http.begin(serverUrl);
  int httpResponseCode = http.GET();

  if (httpResponseCode == HTTP_CODE_OK) {
    String payload = http.getString();
    payload.trim();
    Serial.print("Server response: '");
    Serial.print(payload);
    Serial.println("'");

    // Parse the string "1,0,2"
    if (payload.length() >= 5 && payload.charAt(1) == ',' && payload.charAt(3) == ',') {
      
      // Convert char '0','1','2' to int 0, 1, 2
      tomatoLedState = payload.charAt(0) - '0';
      onionLedState = payload.charAt(2) - '0';
      mintLedState = payload.charAt(4) - '0';
      
      Serial.println("LED states updated.");
      
    } else {
      Serial.print("Error: Received unexpected data format: ");
      Serial.println(payload);
      // Set to safe state (OFF)
      tomatoLedState = 0;
      onionLedState = 0;
      mintLedState = 0;
    }
    
  } else {
    Serial.print("Error on HTTP GET: ");
    Serial.println(httpResponseCode);
  }
  http.end();
}