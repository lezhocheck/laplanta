#pragma once

#include <DHTesp.h>
#include <ArduinoJson.h>
#include <stdexcept>
#include <type_traits>
#include <vector>
#include "Data.h"
#include "DataProcessor.h"
#include "Utils.h"


namespace Laplanta {
  template<typename T,
  typename = typename std::enable_if<std::is_arithmetic<T>::value, T>::type>
  class Sensor {
  public:
    void initialize(const std::string& token) {
      std::vector<std::string> plants = getPlants();
      DynamicJsonDocument document(2048);
      document["name"] = getDefaultName();
      document["type"] = getType();
      document["plants"] = toJsonArray<std::string>(plants);
      Laplanta::TokenDataSender sender(CONNECTION + "sensor", token);
      sender.set(document);
      Laplanta::Response response = sender.send();
      if (!response.isSuccess()) {
        printString(response.toString());
        return;
      }
      document = response.getDocument();
      id = document["message"]["sensor_id"].as<std::string>();
      printString("Successfully connected. Id of this device: " + id);
    }

    void record(const std::string& token) {
      if (id.empty()) {
        throw std::runtime_error("Configure your device first");
      }
      Laplanta::TokenDataSender sender(CONNECTION + "sensor/" + id + "/record", token);
      DynamicJsonDocument document(2048);
      std::string name = getDefaultName();

      std::vector<T> values;
      for (int i = 0; i < 5; i++) {
        values.push_back(measureOnce());
        delay(1000);
      }
      DataProcessor<T> processor(values);
      document = processor.getAll();
      sender.set(document);
      Laplanta::Response response = sender.send();
      if (!response.isSuccess()) {
        printString(response.toString());
      }
      printString("Sensor #" + id + " successfully sent a portion of data");
    }

  protected:
    virtual std::string getType() const = 0;
    virtual T measureOnce() = 0;  

  private:
    std::string id = "";

    std::string getDefaultName() const {
       std::string type = getType();
       return type + " sensor";
    }

    std::vector<std::string> getPlants() {
      printString("Enter plants for " + getDefaultName() + " in format: plant_id_1 plant_id2 ...");
      std::vector<std::string> plants;
      while (plants.empty()) {
        std::string plantsString = readString("Plants:");
        plants = parsePlants(plantsString);
        if (plants.empty()) {
           printString("Wrong format. Use: plant_id_1 plant_id2 ...");
        }
      }
      return plants;
    }

    std::vector<std::string> parsePlants(std::string input) {
      trim(input);
      size_t pos = 0;
      std::string token;
      std::vector<std::string> result;
      while ((pos = input.find(' ')) != std::string::npos) {
        token = input.substr(0, pos);
        trim(token);
        if (!token.empty())
          result.push_back(token);
        input.erase(0, pos + 1);
      }
      result.push_back(input);
      return result;
    }
  };


  class DhtSensor : public Sensor<float> {
  public:
    DhtSensor() { 
      dhtSensor.setup(15, DHTesp::DHT22);
    }

  protected:
    DHTesp dhtSensor;
  };


  class TemperatureSensor : public DhtSensor {
  public:
    TemperatureSensor() : DhtSensor() { }

  protected:
    std::string getType() const override {
      return "temperature";
    }

    float measureOnce() override {
      // for better visualization values are simmulated
      // return dhtSensor.getTemperature();
      return rand() % 5 + 20;
    }
  };


  class HumiditySensor : public DhtSensor {
  public:  
    HumiditySensor() : DhtSensor() { }

  protected:
    std::string getType() const override {
      return "humidity";
    }

    float measureOnce() override {
      // for better visualization values are simmulated
      // return dhtSensor.getHumidity();
      return rand() % 10 + 80;
    }
  };
}