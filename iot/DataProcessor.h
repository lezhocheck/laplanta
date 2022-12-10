#pragma once

#include <type_traits>
#include <stdexcept>
#include <ArduinoJson.h>
#include <vector>


namespace Laplanta {
  template<typename T,
  typename = typename std::enable_if<std::is_arithmetic<T>::value, T>::type>
  class DataProcessor {
  public:
    DataProcessor(const std::vector<T>& values) : values(values) { 
      if (values.size() < 2) {
        throw std::runtime_error("Wrong values");
      }
    }

    DynamicJsonDocument getAll() const {
      DynamicJsonDocument result(2048);
      result["values"] = toJsonArray<T>(values);
      result["mean"] = calculateMean();
      result["variance"] = calculateVariance();
      result["std_dev"] = calculateStdDev();
      result["prediction"] = predict();
      return result;
    }

    inline T calculateMean() const {
      return calculateMeanVec(values);
    }

    inline T calculateVariance() const {
      T result = 0;
      T mean = calculateMean();
      for (T value : values) {
        result += (value - mean) * (value - mean);
      }
      return result / values.size();
    }

    inline T calculateStdDev() const {
      return sqrt(calculateVariance());
    }

    inline T predict() const {
      std::pair<std::vector<T>, std::vector<T>> data = getTrainTestData();
      std::vector<T> train = data.first, test = data.second;
      T trainMean = calculateMeanVec(train);
      T testMean = calculateMeanVec(test);
      T value = 0, scale = 0;
      for (size_t i = 0; i < train.size(); i++) {
        T diff = train[i] - trainMean;
        value += diff * (test[i] - testMean);
        scale += diff * diff;
      }
      T k = value / scale;
      T b = testMean - k * trainMean;
      return k * values.back() + b;
    }

  private:
    std::vector<T> values;

    std::pair<std::vector<T>, std::vector<T>> getTrainTestData() const {
      std::vector<T> train, test;
      for (size_t i = 0; i + 1 < values.size(); i++) {
        train.push_back(values[i]);
        test.push_back(values[i + 1]);
      }
      return std::make_pair(train, test);
    }

    inline T calculateMeanVec(const std::vector<T>& vec) const {
      T result = 0;
      for (T value : vec) {
        result += value;
      }
      return result / vec.size();
    }
  };
}