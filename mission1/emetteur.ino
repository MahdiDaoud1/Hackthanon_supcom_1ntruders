/*
 * ===================================================================
 * Project:   Smart Farm - Field Sensor Node (v3 - Deep Sleep)
 *
 * Role:      Wakes up, reads sensors, POSTs data, and goes
 * back to deep sleep for 5 minutes.
 * ===================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>

// === Wi-Fi & Server Config ===
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";
// Use your deployed Vercel URL
const char* serverUrl = "https://hackthanonsupcom1ntruders.vercel.app/update_raw";

// === Pin Definitions ===
const int TOMATO_SENSOR_PIN = 34;
const int ONION_SENSOR_PIN = 35;
const int MINT_SENSOR_PIN = 32;

// === Deep Sleep ===
// 5 minutes in microseconds
// 5 min * 60 sec/min * 1,000,000 µs/sec
#define TIME_TO_SLEEP 300000000  

// Function prototypes
void connectToWiFi();
void sendSensorData();

/*
 * ===================================================================
 * SETUP
 * ===================================================================
 */
void setup() {
  Serial.begin(115200);
  Serial.println("\n-----------------------");
  Serial.println("Field Node: Woke up from deep sleep!");

  // 1. Connect to Wi-Fi
  connectToWiFi();

  // 2. Send data (only if connected)
  if (WiFi.status() == WL_CONNECTED) {
    sendSensorData();
  } else {
    Serial.println("Failed to connect to WiFi. Going back to sleep.");
  }

  // 3. Go to sleep
  Serial.println("Data sent. Going to sleep for 5 minutes...");
  Serial.flush(); // Wait for Serial to finish printing
  
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP);
  esp_deep_sleep_start();
}

/*
 * ===================================================================
 * LOOP (This function is never reached)
 * ===================================================================
 */
void loop() {
  // Nothing here
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
  // Try to connect for 10 seconds (20 attempts * 500ms)
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
 * sendSensorData()
 * ===================================================================
 */
void sendSensorData() {
  // 1. Read Raw Sensor Values
  int tomatoVal = analogRead(TOMATO_SENSOR_PIN);
  int onionVal = analogRead(ONION_SENSOR_PIN);
  int mintVal = analogRead(MINT_SENSOR_PIN);

  // 2. Build Raw Data String
  String rawData = String(tomatoVal) + "," +
                   String(onionVal) + "," +
                   String(mintVal);

  Serial.print("Sending raw data: ");
  Serial.println(rawData);

  // 3. Send HTTP POST Request
  HTTPClient http;
  http.begin(serverUrl);
  http.addHeader("Content-Type", "text/plain");

  int httpResponseCode = http.POST(rawData);

  if (httpResponseCode > 0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
  } else {
    Serial.print("Error on sending POST: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}