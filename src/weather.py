# This file is part of the Weather App project.
# It is contains functions for handling  cache, logic, data of the weather app.
import requests
import json
from datetime import datetime, timezone
from src.config import get_config

requests_cache = {}  # Format: { "city_name_lower": weather_data_dict }

weater_config = get_config()

def is_cached_recent(city):
    now = datetime.now(timezone.utc)
    key = city.lower()
    entry = requests_cache.get(key)

    if entry and now - entry["timestamp"] <= weater_config.cache_lifetime:
        return entry
    return None

# Return dict weather data for a city
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
            return None

        return {
            "city": city,
            "temperature": f"{temp_metric} C / {temp_imperial} F",
            "description": description,
            "humidity": f"{humidity}%",
            "windSpeed": f"{wind_speed_metric} m/s / {wind_speed_imperial} mph",
            "timestamp": datetime.now(timezone.utc)
        }
    except (TypeError, ValueError) as e:
        print(f"[ERROR] Failed to extract weather fields for city '{city}': {e}")
        return None


# Get data from openweathermap and return dict weather data for a city
def fetch_weather_data(city):
    try:
        metric_url = weater_config.url_template.format(city, "metric", weater_config.api_key_id)
        imperial_url = weater_config.url_template.format(city, "imperial", weater_config.api_key_id)

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

# Return normalized list of cities. Removed whitespaces, set city to lowercase, distinct
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

# Return list of weather data for a cities
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
            key = city.lower()
            requests_cache[key] = data
            response_data.append(data)

    return response_data
