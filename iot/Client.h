#pragma once

#include <stdexcept>
#include <WiFi.h>
#include "Data.h"
#include "Utils.h"


namespace Laplanta {
  class Client {
  public:
    Client() : email(""), password(""), token("") { }

    void connectToNetwork() {
      printString("Connecting to Wi-Fi...");
      WiFi.begin("Wokwi-GUEST", "", 6);
      while (WiFi.status() != WL_CONNECTED) {
        delay(100);
      }
      printString("Connected!");
    }

    void authenticate() {
      printString("Authenticate in Laplanta first");
      Response response = guaranteeAuthentication(CONNECTION + "user/login");
      DynamicJsonDocument document = response.getDocument();
      token = document["message"]["token"].as<std::string>();
      printString("Successfully logged in!");
    }

    std::string getToken() const {
      if (token == "") {
        throw std::runtime_error("Token is not valid. Authenticate first");
      }
      return token;
    }

  private:
    std::string email, password, token;

    Response guaranteeAuthentication(const std::string& connection) {
      Response response = Response();
      DataSender dataSender(connection);
      while (!response.isSuccess()) {
        email = readString("email:");
        password = readString("password:");
        dataSender.add<std::string>("email", email);
        dataSender.add<std::string>("password", password);
        response = dataSender.send();
        if (!response.isSuccess()) {
          printString("Authentication failed. " + response.toString());
        }
      }
      return response;
    }
  };
}
