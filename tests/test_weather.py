from datetime import datetime, timedelta, timezone
from src import weather

# Mock the config used in weather.py
class MockConfig:
    api_key_id = "*************"
    url_template = "https://api.openweathermap.org/data/2.5/weather?q={}&units={}&appid={}"
    cache_lifetime = timedelta(hours=1)

# Patch config and cache manually
weather.weater_config = MockConfig()
weather.requests_cache = {}  # Format: { "city_name_lower": weather_data_dict }

def test_get_unique_nonempty_cities():
    cities = ["Tallinn", "  Tartu", "London", " ", "Tallinn", "TARTU"]
    result = weather.get_unique_nonempty_cities(cities)
    assert result == ["Tallinn", "Tartu", "London"]

def test_is_cached_recent_hit():
    city = "Tallinn"
    now = datetime.now(timezone.utc)
    entry = {
        "city": city,
        "timestamp": now
    }
    weather.requests_cache = {"tallinn": entry}
    result = weather.is_cached_recent("tallinn")
    assert result == entry

def test_is_cached_recent_miss():
    city = "Tartu"
    old_time = datetime.now(timezone.utc) - timedelta(hours=2)
    weather.requests_cache = {"tartu": {
        "city": city,
        "timestamp": old_time
    }}
    result = weather.is_cached_recent("tartu")
    assert result is None

def test_extract_weather_fields_valid():
    city = "London"
    metric_json = {
        "main": {"temp": 15, "humidity": 70},
        "weather": [{"description": "clear sky"}],
        "wind": {"speed": 5}
    }
    imperial_json = {
        "main": {"temp": 59},
        "wind": {"speed": 10}
    }

    result = weather.extract_weather_fields(city, metric_json, imperial_json)
    assert result["city"] == city
    assert "temperature" in result
    assert "description" in result
    assert "humidity" in result
    assert "windSpeed" in result
    assert isinstance(result["timestamp"], datetime)

def test_extract_weather_fields_missing_fields():
    city = "Tallinn"
    metric_json = {
        "main": {},
        "weather": [{}],
        "wind": {}
    }
    imperial_json = {
        "main": {},
        "wind": {}
    }

    result = weather.extract_weather_fields(city, metric_json, imperial_json)
    assert result is None
