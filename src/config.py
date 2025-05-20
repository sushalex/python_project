# Load settings data from config.json file
from datetime import timedelta
import json
import os

class Config:
    def __init__(self, data: dict):
        self.api_key_id = data["api_key_id"]
        self.duration_hours = data["duration_hours"]
        self.cache_lifetime = timedelta(hours=self.duration_hours)
        self.url_template = str(data["url_template"])


config_path = os.path.join(os.getcwd(), "config.json")

# Read config file and return a json
def read_config_file():
    try:
        with open(config_path, "r") as f:
            config_json = json.load(f)
            return config_json
    except Exception as e:
        print(f"[ERROR] Read config file. {e}")
        exit()

# Return Config object from config file
def get_config():
    try:
        config_json = read_config_file()

        settings_data = {  
            'api_key_id': config_json["apiKey"],
            'duration_hours': config_json["cacheTimeHour"],
            'url_template': str(config_json["url"])
        }

        return Config(settings_data)
          
    except Exception as e:
        print(f"[ERROR] Read config file. {e}")
        exit()


