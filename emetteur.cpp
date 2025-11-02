/*
 * ===================================================================
 * Project:   Smart Farm - Field Sensor Node (Transmitter)
 *
 * Role:      Reads raw sensor data and POSTs it to a web server.
 * This node does NO local calculation.
 *
 * Hardware:  ESP32, 3x Moisture Sensors, Wi-Fi
 * ===================================================================
 */

#include <WiFi.h>
#include <HTTPClient.h>

// === Wi-Fi & Server Config ===
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

// This is the URL to your Flask server's POST endpoint
const char* serverUrl = "http://YOUR_SERVER_IP_OR_DOMAIN:5000/update_raw";

// === Pin Definitions ===
const int TOMATO_SENSOR_PIN = 34; // ADC1
const int ONION_SENSOR_PIN = 35;  // ADC1
const int MINT_SENSOR_PIN = 32;   // ADC1

// === Timing ===
// Send data every 5 minutes (300,000 milliseconds)
const long INTERVAL = 300000;
unsigned long previousMillis = 0;

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
  while (!Serial);
  Serial.println("Field Sensor Node: Booting...");
  connectToWiFi();
}

/*
 * ===================================================================
 * LOOP
 * ===================================================================
 */
void loop() {
  unsigned long currentMillis = millis();

  // Non-blocking timer to send data
  if (currentMillis - previousMillis >= INTERVAL) {
    previousMillis = currentMillis;
    if (WiFi.status() != WL_CONNECTED) {
      Serial.println("WiFi disconnected. Reconnecting...");
      connectToWiFi();
    }
    if (WiFi.status() == WL_CONNECTED) {
      sendSensorData();
    }
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
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nFailed to connect to WiFi. Will retry later.");
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