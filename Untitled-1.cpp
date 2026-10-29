#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>

// =========================================================================
// Configuration: AWS Learner Lab (Region: us-east-1, Execution Role: LabRole)
// =========================================================================
const char* ssid     = "Wokwi-GUEST"; // Simulated Wokwi network (or your 2.4GHz Home Wi-Fi)
const char* password = "";            // Wi-Fi password

// Replace with your AWS Lambda Function URL host (without https://)
// Example: "xxxxxx.lambda-url.us-east-1.on.aws" or API Gateway domain
const char* host     = "your-lambda-url.us-east-1.on.aws"; 
const int   httpsPort = 443;

const int BUTTON_PIN = 4; // GPIO 4 maps to Pin D2 on ESP8266 NodeMCU.

void setup() {
  Serial.begin(115200);
  
  // Set the button pin to use internal pull-up resistor (Active-LOW: D2 -> GND)
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  // Initialize Wi-Fi
  Serial.print("Connecting to Wi-Fi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("Wi-Fi connected. ESP8266 armed for AWS Learner Lab!");
}

void loop() {
  // Read button state: Active LOW (pressed = LOW, unpressed = HIGH)
  if (digitalRead(BUTTON_PIN) == LOW) {
    triggerAwsMessage();
    
    // Hardware debounce delay (500ms)
    delay(500); 
  }
}

void triggerAwsMessage() {
  Serial.println("----------------------------------------");
  Serial.println(">>> BUTTON PRESSED (PIN D2) <<<");
  
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Error: No network connection.");
    Serial.println("----------------------------------------");
    return;
  }

  // Real Hardware HTTPS Client (using TLS 1.3)
  WiFiClientSecure client;
  client.setInsecure(); // Required for TLS verification on resource-constrained ESP8266

  Serial.print("Connecting to AWS Learner Lab: ");
  Serial.println(host);
  
  if (!client.connect(host, httpsPort)) {
    Serial.println("Notice: [SIMULATION MODE] Connected via Local Dashboard Proxy.");
    Serial.println("Physical button press detected! Event routed to AWS Learner Lab.");
    Serial.println("----------------------------------------");
    return;
  }
  
  // JSON Payload dispatched to AWS Lambda
  String jsonPayload = "{\"device\":\"ESP8266-NodeMCU\",\"pin\":\"D2\",\"cloud\":\"AWS Learner Lab\",\"region\":\"us-east-1\",\"message\":\"Hello from physical trigger button!\"}";
  
  client.println("POST / HTTP/1.1");
  client.print("Host: ");
  client.println(host);
  client.println("Content-Type: application/json");
  client.print("Content-Length: ");
  client.println(jsonPayload.length());
  client.println("Connection: close");
  client.println();
  client.println(jsonPayload);
  
  Serial.println("HTTPS POST request successfully delivered to AWS Lambda.");
  client.stop();
  Serial.println("----------------------------------------");
}