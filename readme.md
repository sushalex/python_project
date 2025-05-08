# Developed by Aleksandr Borissov

# Weather Forecast CLI App

This is a command line Python application that allows users to retrieve and display current weather data for multiple cities using OpenWeatherMap API.
It supports both metric and imperial units and includes in-memory caching to avoid repeated API calls.

---

## Features

* Fetches weather data (temperature, description, humidity, wind speed) for multiple cities
* Uses both **metric** (Celsius, m/s) and **imperial** (Fahrenheit, mph) units
* Removes duplicate and empty city entries
* Caches results for a configurable number of hours
* Simple command-line interface (CLI) loop

---

## Requirements

* OpenWeatherMap API key
* Python 3.7+
* Internet connection

Install required package:

pip install requests


---

## 📁 Project Structure


weather_app/
	weather_app.py         # Main script
	config.json            # Configuration file with API key and URL template
	test_weather_module.py # Unit tests

---

## ⚙️ Configuration

Rename file `config.json.template` to `config.json`:

```json
{
  "apiKey": "your_openweathermap_api_key",
  "cacheTimeHour": 1,
  "url": "http://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}"
}
```

* `apiKey`: Your OpenWeatherMap API key.
* `cacheTimeHour`: Number of hours to cache results.
* `url`: The API request format. Use `{}`, `{}`, and `{}` placeholders for city, unit system, and API key.

---

## 🚀 Usage

Run the script:

python weather_app.py


You will be prompted to enter a comma-separated list of cities:

```
Please insert city for weather forecast (comma-separated): London, Paris, New York
```

You'll get output like:

```
City name: London, Temperature: 15 C / 59 F, Description: light rain, Humidity: 80%, Wind Speed: 3 m/s / 6 mph
...
```

To continue querying, press `y`. To exit, press `n`.

---

## Testing

Unit tests are provided using `unittest` and `unittest.mock`.

Run tests with:


python -m unittest test_weather_module.py


---

##  Future for next api version. Improvements

* Replace `exit()` calls with proper exceptions
* Use logging instead of `print()`
* Support for asynchronous requests/response

---