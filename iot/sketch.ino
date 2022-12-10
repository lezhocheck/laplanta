#include <time.h>
#include "Utils.h"
#include "Sensor.h"
#include "Client.h"


Laplanta::Client client;
Laplanta::TemperatureSensor temperatureSensor;
Laplanta::HumiditySensor humiditySensor;

void setup() {
  // test only. remove in real scenario
  srand(time(nullptr));

  Serial.begin(115200);
  try {
    client.connectToNetwork();
    client.authenticate();
    std::string token = client.getToken();
    temperatureSensor.initialize(token);
    humiditySensor.initialize(token);
  } catch(const std::exception& e) {
    Serial.println(e.what());
  }
}

void loop() {
  try {
    std::string token = client.getToken();
    temperatureSensor.record(token);
    humiditySensor.record(token);
  } catch(const std::exception& e) {
    Serial.println(e.what());
  }
  delay(3000);
}