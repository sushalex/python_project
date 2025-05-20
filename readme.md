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

Step 1. Create the .venv (Virtual Environment)

Make sure python is recognized in your terminal and use 'python -m venv .venv'. 
if not, use command 'py -m venv .venv'
Tip (Windows) This creates a folder called .venv in your project directory containing a fresh Python environment

Step 2. Activate the .venv

Windows 
run in terminal command '.venv\Scripts\activate'

MacOs/Linux
run in terminal command 'source .venv/bin/activate'

Success activated, your prompt will show something like:
(.venv) C:\Your Project\Path>

Step 3. Install additional libs
pip install -r requirements.txt

---

## Project Structure

weather_app/
	app.py         # Main script
	config.json    # Configuration file with API key and URL template

	src            # Folder for main files of project. Handling, fetcing data, app settings
	 - config.py   # Load settings data from config.json file
	 - weather.py  # It is contains functions for handling  cache, logic, data of the weather app.

	tests		    # Folder for Unit tests
	 - test_weather.py  # Load settings data from config.json file

---

## Configuration

Rename file `config.json.template` to `config.json`:

 .json
{
  "apiKey": "your_openweathermap_api_key",
  "cacheTimeHour": 1,
  "url": "http://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}"
}


* `apiKey`: Your OpenWeatherMap API key.
* `cacheTimeHour`: Number of hours to cache results.
* `url`: The API request format. Use `{}`, `{}`, and `{}` placeholders for city, unit system, and API key.

---

## Usage

Run the script:

python app.py


You will be prompted to enter a comma-separated list of cities:

```
Please insert city for weather forecast (comma-separated): Tallinn, Tartu, London, Paris
```

You'll get output like:

```
City name: London, Temperature: 15 C / 59 F, Description: light rain, Humidity: 80%, Wind Speed: 3 m/s / 6 mph
...

To continue querying, press `y`. To exit, press `n`.

---