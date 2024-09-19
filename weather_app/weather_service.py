
import datetime
import requests
from requests import Response
from typing import Dict
from django.core.cache import cache

class WeatherService:
    BASE_URL: str = "https://api.open-meteo.com/v1/forecast"
    GEOCODE_URL: str = "https://geocoding-api.open-meteo.com/v1/search"

    @staticmethod
    def fetch_cords(city: str) -> Dict[str, any]:
        ## Check if cords exist in cache
        key: str = city.replace(" ", "_")
        if cache.has_key(key):
            return cache.get(key)
        ## If no cache was found, make a request
        req_params: dict = {
            "name": city.title(),
            "count": 1
        }
        response: Response = requests.get(WeatherService.GEOCODE_URL, params=req_params)
        response.raise_for_status()
        data: dict = response.json()
        if data.get("results", None):
            ## Cache result
            cache.set(key, data["results"][0])
            return data["results"][0]
        else:
            raise ValueError(f"City not found: '{city.title()}'")
        
    @staticmethod
    def request_weather(city=None, latitude=None, longitude=None):
        ## If the city was specified, try looking up the city's cords 
        if city:
            cords = WeatherService.fetch_cords(city)
            latitude = cords["latitude"]
            longitude = cords["longitude"]
        
        if (latitude is None) or (longitude is None):
            raise ValueError("Either coordinates or city name must be provided")

        ## Check if weather exists in cache
        key: str = f"{latitude}_{longitude}"
        if cache.has_key(key):
            return cache.get(key)
        
        ## Weather not found in cache, make a request
        reqParams = {
            "latitude": latitude,
            "longitude": longitude,
            "current": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
	        "hourly": ["temperature_2m", "relative_humidity_2m", "wind_speed_10m"],
            "timezone": "auto",
        }

        response = requests.get(WeatherService.BASE_URL, params=reqParams)
        response.raise_for_status()

        res_data = response.json()

        # Extract hourly weather data
        hourly_data = {
            'time': res_data.get('hourly', {}).get('time', []),
            'temperature': res_data.get('hourly', {}).get('temperature_2m', []),
            'humidity': res_data.get('hourly', {}).get('relative_humidity_2m', []),
            'weather_code': res_data.get('hourly', {}).get('weather_code', []),
            'wind_speed': res_data.get('hourly', {}).get('wind_speed_10m', []),
        }

        # Extract current weather data
        current_weather = res_data.get('current', {})
        # Get the current hour
        now = datetime.datetime.fromisoformat(current_weather["time"])

        # Filter hourly data for the current hour and the next 7 days
        filtered_data = []
        for i, time in enumerate(hourly_data['time']):
            hour_datetime = datetime.datetime.fromisoformat(time)
            if hour_datetime.hour == now.hour:
                filtered_data.append({
                    'time': time,
                    'temperature': hourly_data['temperature'][i],
                    'humidity': hourly_data['humidity'][i],
                    'wind_speed': hourly_data['wind_speed'][i],
                })

        ## Store result in cache
        cache.set(key, filtered_data)
        return filtered_data
    
