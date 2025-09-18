# Utility functions for the ClimaMap project
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
import geocoder

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_KEY")

if not API_KEY:
    # This will raise an error when the app starts if the key is missing.
    # It's better to fail early.
    raise ValueError("OPENWEATHER_KEY environment variable not set.")

def get_location_from_ip():
    """Get user's approximate location (city) based on their IP address."""
    location = geocoder.ip('me')
    if location.ok:
        return location.city
    return None

def get_weather(city, units="metric"):
    """Fetch weather data from the OpenWeatherMap API for a given city."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={units}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"]
        }
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return {"error": "City not found."}
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"An error occurred during the request: {req_err}"}

def get_weather_by_coords(lat, lon, units="metric"):
    """Fetch weather data from the OpenWeatherMap API for given coordinates."""
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units={units}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        return {
            "city": data["name"],
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].capitalize(),
            "lat": data["coord"]["lat"],
            "lon": data["coord"]["lon"]
        }
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            return {"error": "Location not found."}
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as req_err:
        return {"error": f"An error occurred during the request: {req_err}"}

def _process_forecast_data(data):
    """Helper function to process raw forecast data into daily summaries."""
    daily_forecasts = {}
    for item in data['list']:
        date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
        if date not in daily_forecasts:
            daily_forecasts[date] = {
                'temps': [],
                'descriptions': set(),
                'icons': set()
            }
        daily_forecasts[date]['temps'].append(item['main']['temp'])
        daily_forecasts[date]['descriptions'].add(item['weather'][0]['description'].capitalize())
        daily_forecasts[date]['icons'].add(item['weather'][0]['icon'])

    processed_data = []
    for date, values in sorted(daily_forecasts.items())[:5]: # Get up to 5 days
        processed_data.append({
            "date": datetime.strptime(date, '%Y-%m-%d').strftime('%A, %b %d'),
            "temp_min": min(values['temps']),
            "temp_max": max(values['temps']),
            "description": ', '.join(values['descriptions']),
            "icon": list(values['icons'])[0] # Just take one icon for simplicity
        })
    return processed_data

def get_forecast(city, units="metric"):
    """Fetch 5-day weather forecast from the OpenWeatherMap API."""
    url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units={units}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return _process_forecast_data(response.json())
    except (requests.exceptions.RequestException, KeyError) as e:
        return {"error": f"Could not retrieve forecast for {city}. Reason: {e}"}