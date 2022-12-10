#pragma once

#include <HTTPClient.h>
#include <ArduinoJson.h>
#include <stdexcept>


namespace Laplanta {
  class Response {
  public:
    Response(int code, const std::string& document) : code(code), document(2048) {
      deserializeJson(this->document, document);
    }

    explicit Response() : Response(-1, "") { }

    std::string toString() const {
      std::string result;
      serializeJson(document["message"], result);
      return "Response: " + std::to_string(code) + " " + result;
    }

    bool isSuccess() const {
        return code == OK;
    }

    void guaranteeSuccess() const {
        if (!isSuccess()) {
        std::string representation = toString();
        throw std::runtime_error(representation.c_str());
        }
    }

    const DynamicJsonDocument& getDocument() const {
        return document;
    }

  private:
    const static int OK = 200;
    int code;
    DynamicJsonDocument document;
  };


  class DataOperator {
  public:
    explicit DataOperator(const std::string& connection) {
      client.begin(toArduinoString(connection));
      client.addHeader("Content-Type", "application/json");
    }

    virtual Response send() = 0;

    ~DataOperator() {
      client.end();
    }

  protected:
    HTTPClient client;
  };


  class DataSender : public DataOperator {
  public:
    explicit DataSender(const std::string& connection) : DataOperator(connection), 
      document(2048) { }

    template <typename T>
    void add(const std::string& key, const T& value) {
        document[key] = value;
    }

    void set(const DynamicJsonDocument& document) {
        this->document = document;
    }

    Response send() override {
        std::string json;
        serializeJson(document, json);
        int statusCode = client.POST(toArduinoString(json));
        std::string message = client.getString().c_str();
        return Response(statusCode, message);
    }

  protected:
    DynamicJsonDocument document;
  };


  class TokenDataSender : public DataSender {
  public:
    TokenDataSender(const std::string& connection, const std::string& token) : 
      DataSender(connection), token(token) {   
      client.addHeader("x-access-token", toArduinoString(token));      
    }

  private:
    std::string token;  
  };


  class TokenDataReceiver : public DataOperator {
  public:
    explicit TokenDataReceiver(const std::string& connection, const std::string& token) : 
        DataOperator(connection), token(token) {
      client.addHeader("x-access-token", toArduinoString(token));   
    }

    Response send() override {
        int statusCode = client.GET();
        std::string message = client.getString().c_str();
        return Response(statusCode, message);
    }

  private:
    std::string token;
  };
}