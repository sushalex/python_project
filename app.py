from src.weather import get_weather_for_cities
IS_EXIST = True

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
