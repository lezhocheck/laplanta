#pragma once

#include <vector>
#include <algorithm>
#include <ArduinoJson.h>

namespace Laplanta {
  const std::string CONNECTION = "http://109.87.83.121:9999/";
  
  void printString(const std::string& value) {
    String result = String(value.c_str());
    Serial.println(result);
  }

  std::string readString(const std::string& label) {
    printString(label);
    while (Serial.available() == 0) { 
      delay(100);
    }
    String value = Serial.readStringUntil('\n');
    std::string result(value.c_str());
    printString(result);
    return result;
  }

  String toArduinoString(const std::string& value) {
    return String(value.c_str());
  }

  template<typename T>
  JsonArray toJsonArray(const std::vector<T>& arr) {
    DynamicJsonDocument doc(2048);
    JsonArray result = doc.to<JsonArray>();
    for (const T& str : arr) {
      result.add(str);
    }
    return result;
  }

  inline void ltrim(std::string &s) {
    s.erase(s.begin(), std::find_if(s.begin(), s.end(),
      std::not1(std::ptr_fun<int, int>(std::isspace))));
  }

  inline void rtrim(std::string &s) {
    s.erase(std::find_if(s.rbegin(), s.rend(),
      std::not1(std::ptr_fun<int, int>(std::isspace))).base(), s.end());
  }

  inline void trim(std::string &s) {
    rtrim(s);
    ltrim(s);
  }

}