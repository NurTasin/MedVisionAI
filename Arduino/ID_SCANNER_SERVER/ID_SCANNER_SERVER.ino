#include <SPI.h>
#include <MFRC522.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>

// Define RC522 pins
#define SS_PIN D8
#define RST_PIN D4

// Define WiFi credentials and server address
const char* ssid = "Tasin's M21";
const char* password = "zdhw5861";
const char* server = "192.168.216.81";

// Initialize the RC522 module
MFRC522 mfrc522(SS_PIN, RST_PIN);

void setup() {
  Serial.begin(115200);
  // Initialize the RC522 module
  SPI.begin();
  mfrc522.PCD_Init();
  // Connect to WiFi network
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  // Look for new cards
  if ( ! mfrc522.PICC_IsNewCardPresent() || ! mfrc522.PICC_ReadCardSerial() ) {
    delay(50);
    return;
  }

  // Get card UID
  String cardUID = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    cardUID += String(mfrc522.uid.uidByte[i] < 0x10 ? "0" : "");
    cardUID += String(mfrc522.uid.uidByte[i], HEX);
  }

  Serial.print("Card UID: ");
  Serial.println(cardUID);

  // Make HTTP POST request to server
  WiFiClient client;
  if (client.connect(server, 80)) {
    String postData = "card_uid=" + cardUID;
    client.println("POST /card HTTP/1.1");
    client.println("Host: 192.168.216.81");
    client.println("Content-Type: application/x-www-form-urlencoded");
    client.print("Content-Length: ");
    client.println(postData.length());
    client.println();
    client.println(postData);
  }
  else {
    Serial.println("Unable to connect to server");
  }

  // Wait for response from server
  while (client.connected() && !client.available());
  while (client.available()) {
    char c = client.read();
    Serial.write(c);
  }

  delay(1000);
}
