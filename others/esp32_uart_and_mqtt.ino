#include <WiFi.h>
#include <PubSubClient.h>
#include <PZEM004Tv30.h>

const char* ssid = "YOUR_WIFI";
const char* password = "YOUR_PASSWORD";

const char* mqtt_server = "YOUR_MQTT_BROKER";
const int mqtt_port = 1883;
const char* mqtt_topic = "iot/energy/measurements";

WiFiClient espClient;
PubSubClient client(espClient);
PZEM004Tv30 pzem(Serial1, 16, 17);

void connectWiFi() {
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
}

void reconnectMQTT() {
  while (!client.connected()) {
    client.connect("ESP32_PZEM");
    if (!client.connected()) {
      delay(2000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  Serial1.begin(9600, SERIAL_8N1, 16, 17);
  connectWiFi();
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  if (!client.connected()) {
    reconnectMQTT();
  }
  client.loop();

  float V = pzem.voltage();
  float I = pzem.current();
  float P = pzem.power();
  float E = pzem.energy();

  String json = "{";
  json += "\"voltage\":" + String(V) + ",";
  json += "\"current\":" + String(I) + ",";
  json += "\"power\":" + String(P) + ",";
  json += "\"energy\":" + String(E);
  json += "}";

  client.publish(mqtt_topic, json.c_str());

  delay(2000);
}
