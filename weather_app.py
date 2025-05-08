import requests
import json
import os
from datetime import datetime, timedelta

# Load API key from config
config_path = os.path.join(os.getcwd(), "config.json")
print(" --------- " + config_path)

requests_cache = []  # Each item includes "timestamp"
IS_EXIST = True

try:
    with open(config_path, "r") as f:
        config_json = json.load(f)
        API_KEY_ID = config_json["apiKey"]
        DURATION_HOURS = config_json["cacheTimeHour"]
        CACHE_LIFETIME = timedelta(hours=DURATION_HOURS)
        URL_TEMPLATE = str(config_json["url"])
except Exception as e:
    print(f"[ERROR] Read config file. {e}")
    exit()


def is_cached_recent(city):
    now = datetime.utcnow()
    for entry in requests_cache:
        if entry["city"].lower() == city.lower():
            if now - entry["timestamp"] <= CACHE_LIFETIME:
                return entry
    return None


def extract_weather_fields(city, metric_json, imperial_json):
    try:
        # Validate required fields in both metric and imperial responses
        if not all(key in metric_json for key in ["main", "weather", "wind"]):
            print(f"[ERROR] Metric data missing required fields for city '{city}'")
            return None
        if not all(key in imperial_json for key in ["main", "wind"]):
            print(f"[ERROR] Imperial data missing required fields for city '{city}'")
            return None
        if not isinstance(metric_json["weather"], list) or not metric_json["weather"]:
            print(f"[ERROR] 'weather' field is empty or invalid in metric data for city '{city}'")
            return None

        # Extract values with fallback checking
        temp_metric = metric_json["main"].get("temp")
        temp_imperial = imperial_json["main"].get("temp")
        description = metric_json["weather"][0].get("description")
        humidity = metric_json["main"].get("humidity")
        wind_speed_metric = metric_json["wind"].get("speed")
        wind_speed_imperial = imperial_json["wind"].get("speed")

        # Ensure no values are missing
        if None in [temp_metric, temp_imperial, description, humidity, wind_speed_metric, wind_speed_imperial]:
            print(f"[ERROR] Missing weather values in response for city '{city}'")
            exit()

        return {
            "city": city,
            "temperature": f"{temp_metric} C / {temp_imperial} F",
            "description": description,
            "humidity": f"{humidity}%",
            "windSpeed": f"{wind_speed_metric} m/s / {wind_speed_imperial} mph",
            "timestamp": datetime.utcnow()
        }
    except (TypeError, ValueError) as e:
        print(f"[ERROR] Failed to extract weather fields for city '{city}': {e}")
        exit()


def fetch_weather_data(city):
    try:
        metric_url = URL_TEMPLATE.format(city, "metric", API_KEY_ID)
        imperial_url = URL_TEMPLATE.format(city, "imperial", API_KEY_ID)

        #get data from openweathermap 
        metric_resp = requests.get(metric_url)
        imperial_resp = requests.get(imperial_url)

        if metric_resp.status_code == 200 and imperial_resp.status_code == 200:
            try:
                metric_json = metric_resp.json()
                imperial_json = imperial_resp.json()
                return extract_weather_fields(city, metric_json, imperial_json)
            except json.JSONDecodeError as e:
                print(f"[ERROR] Failed to parse JSON for city '{city}': {e}")
        else:
            print(f"[ERROR] API request failed for city '{city}': "
                  f"Metric status {metric_resp.status_code}, Imperial status {imperial_resp.status_code}")
    except requests.RequestException as e:
        print(f"[ERROR] Network error while requesting city '{city}': {e}")
        exit()
    return None


def get_unique_nonempty_cities(city_list: list):
    seen = set()
    unique = []

    if city_list is None or len(city_list)==0:
        print(f"[ERROR] city_list is none or empty.")
        exit()

    #remove whitespaces, set city to lowercase, distinct
    for city in city_list:
        city = city.strip()
        if city and city.lower() not in seen:
            seen.add(city.lower())
            unique.append(city)
    return unique


def get_weather_for_cities(city_list):
    unique_cities = get_unique_nonempty_cities(city_list)
    response_data = []

    for city in unique_cities:
        cached_entry = is_cached_recent(city)
        if cached_entry:
            response_data.append(cached_entry)
            continue

        data = fetch_weather_data(city)
        if data:
            requests_cache.append(data)
            response_data.append(data)

    return response_data

# Main loop
while IS_EXIST:
    try:
        input_cities = input("Please insert city for weather forecast (comma-separated): ")
        city_list = input_cities.split(",")
        weather_data = get_weather_for_cities(city_list)
        
        result = ""
        for data in weather_data:
            result += f"\nCity name: {data['city']}, Temperature: {data['temperature']}, Description: {data['description']}, Humidity: {data['humidity']}, Wind Speed: {data['windSpeed']}"
        
        print(result)
        exit_str = input("\nTo continue - press 'y', exit - press 'n': ").strip().lower()
        if exit_str == "n":
            IS_EXIST = False
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        IS_EXIST = False

print("Exit...")
