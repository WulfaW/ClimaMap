# app.py
import streamlit as st
from utils import get_weather, get_forecast, get_weather_by_coords, get_location_from_ip
import folium
from streamlit_folium import st_folium
import numpy as np

st.set_page_config(page_title="ClimaMap", page_icon="🌤️", layout="wide")
st.markdown(
    """
    <h1 style='text-align: center; color: #1E3A8A;'>ClimaMap 🌤️</h1>
    """,
    unsafe_allow_html=True
)

def get_background_class(description):
    """Returns a CSS class name based on the weather description."""
    description = description.lower()
    if "clear" in description or "güneşli" in description:
        return "clear-sky"
    elif "few clouds" in description or "az bulutlu" in description:
        return "few-clouds"
    elif "scattered clouds" in description or "parçalı bulutlu" in description:
        return "scattered-clouds"
    elif "broken clouds" in description or "çok bulutlu" in description:
        return "broken-clouds"
    elif "clouds" in description or "bulutlu" in description:
        return "cloudy"
    elif "rain" in description or "drizzle" in description or "yağmurlu" in description:
        return "rainy"
    elif "thunderstorm" in description or "fırtına" in description:
        return "stormy"
    elif "snow" in description or "kar" in description:
        return "snowy"
    elif "mist" in description or "fog" in description or "haze" in description or "sisli" in description:
        return "misty"
    elif "smoke" in description or "dumanlı" in description:
        return "smoky"
    elif "dust" in description or "tozlu" in description:
        return "dusty"
    elif "sand" in description or "kumlu" in description:
        return "sandy"
    elif "ash" in description or "kül" in description:
        return "ashy"
    elif "squall" in description or "ani rüzgar" in description:
        return "squall"
    elif "tornado" in description or "hortum" in description:
        return "tornado"
    else:
        return "default-bg"

def get_bg_color_from_class(bg_class):
    """Maps a class name to a hex color code for direct injection."""
    colors = {
        "clear-sky": "#87CEEB",           # Açık mavi
        "few-clouds": "#B2DFDB",          # Turkuaz
        "scattered-clouds": "#AED6F1",    # Açık mavi-gri
        "broken-clouds": "#85929E",       # Gri-mavi
        "cloudy": "#B0C4DE",              # Gri
        "rainy": "#5DADE2",               # Yağmurlu mavi
        "stormy": "#34495E",              # Koyu gri
        "snowy": "#F8F8FF",               # Beyaz
        "misty": "#D3D3D3",               # Açık gri
        "smoky": "#A1887F",               # Kahverengi-gri
        "dusty": "#F4E2D8",               # Tozlu bej
        "sandy": "#F7DC6F",               # Kum sarısı
        "ashy": "#616161",                # Kül grisi
        "squall": "#7FB3D5",              # Rüzgarlı mavi
        "tornado": "#7D3C98",             # Mor
        "default-bg": "#f0f2f6"           # Varsayılan açık gri
    }
    return colors.get(bg_class, "#f0f2f6")

def set_background_css(bg_class):
    """Injects local CSS for styling and dynamic background color."""
    bg_color = get_bg_color_from_class(bg_class)
    st.markdown(f"""
        <style>
        .stApp {{
            background-color: {bg_color};
            transition: background-color 0.5s ease;
        }}

        /* Main content area */
        .main .block-container {{
            padding: 2rem;
            border-radius: 10px;
        }}

        /* Title styling */
        h1 {{
            color: #1E3A8A; /* Dark Blue */
        }}

        /* Subheader styling */
        h3 {{
            color: #3B82F6; /* Lighter Blue */
        }}
        </style>
    """, unsafe_allow_html=True)

# Set a default background on initial load
set_background_css("default-bg")
st.subheader("Enter a city or click on the map!")

# Initialize session state
if "city" not in st.session_state:
    st.session_state.city = None
if "initial_load" not in st.session_state:
    st.session_state.initial_load = True

# --- UI Elements ---
col1, col2 = st.columns([3, 1])
with col1:
    # Single city input
    city_input = st.text_input("Enter a city (e.g., Istanbul)", "")
with col2:
    # Unit selection
    unit_choice = st.radio("Select Temperature Unit", ("Celsius", "Fahrenheit"), key="unit_choice")
    unit_system = "metric" if unit_choice == "Celsius" else "imperial"
    unit_symbol = "°C" if unit_choice == "Celsius" else "°F"

# --- Event Handlers ---
if st.button("Show Weather"):
    city = city_input.strip()
    if city:
        # When a new city is searched, we pass the unit system
        st.session_state.city = city
    else:
        st.warning("Please enter at least one city.")
        st.session_state.city = None

# --- Display Functions ---
def display_forecast(city):
    """Fetches and displays the 5-day forecast for a selected city."""
    st.subheader(f"5-Day Forecast for {city} ({unit_choice})")
    forecast_data = get_forecast(city, units=unit_system)
    if "error" in forecast_data:
        st.error(forecast_data["error"])
        return

    cols = st.columns(len(forecast_data))
    for i, day_forecast in enumerate(forecast_data):
        with cols[i]:
            st.write(f"**{day_forecast['date']}**")
            icon_url = f"http://openweathermap.org/img/wn/{day_forecast['icon']}.png"
            st.image(icon_url, width=50)
            st.write(f"{day_forecast['temp_max']:.1f}{unit_symbol} / {day_forecast['temp_min']:.1f}{unit_symbol}")
            st.caption(day_forecast['description'])

def display_weather_and_map():
    """Fetches and displays weather data and the map."""
    city = st.session_state.city
    weather_data = get_weather(city, units=unit_system)

    if "error" in weather_data:
        st.error(f"{city}: {weather_data['error']}")
        return
        
    # Set the background based on the current weather
    background_class = get_background_class(weather_data['description'])
    set_background_css(background_class)

    # Display current weather in a card-like format
    with st.container():
        st.subheader(f"Current Weather in {weather_data['city']} ({unit_choice})")
        col1, col2 = st.columns(2)
        col1.metric(label="Temperature 🌡️", value=f"{weather_data['temp']} {unit_symbol}")
        col2.metric(label="Humidity 💧", value=f"{weather_data['humidity']}%")
        st.markdown(f"**Durum:** {weather_data['description']}")


    # Set up map
    map_center = [weather_data.get('lat', 41.0), weather_data.get('lon', 29.0)]
    zoom_level = weather_data.get('zoom', 8)

    m = folium.Map(location=map_center, zoom_start=zoom_level)
    m.add_child(folium.LatLngPopup())
    # Add marker to the map
    folium.Marker(
        [weather_data['lat'], weather_data['lon']],
        popup=f"{weather_data['city']} - {weather_data['temp']}{unit_symbol}"
    ).add_to(m)

    # Display map
    map_data = st_folium(m, width=1800, height=600, center=map_center, zoom=zoom_level)

    # Display 5-day forecast
    display_forecast(weather_data['city'])
    
    return map_data

# --- Main App Logic ---
if st.session_state.initial_load:
    # On first load, try to get location from IP
    initial_city = get_location_from_ip()
    if initial_city:
        st.session_state.city = initial_city
    st.session_state.initial_load = False # Ensure this runs only once

if st.session_state.city:
    map_output = display_weather_and_map()
    if map_output and map_output.get("last_clicked"):
        lat = map_output["last_clicked"]["lat"]
        lon = map_output["last_clicked"]["lng"]
        
        # Get weather for the clicked coordinates
        clicked_weather = get_weather_by_coords(lat, lon, units=unit_system)
        if "error" not in clicked_weather:
            # Update session state to show the new location
            st.session_state.city = clicked_weather['city']
            # Rerun the script to display the new city's weather
            st.rerun()
        else:
            st.warning(f"Could not get weather for the clicked location: {clicked_weather['error']}")



# Footer 
st.markdown(
    """
    <hr style="margin-top:2em;">
    <div style="text-align:center; color:gray; font-size:0.9em;">
        © 2025 Wulfa. All rights reserved. <br>
        This software is for educational and personal use only.
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# Copyright (c) 2025 Wulfa. All rights reserved.
# This software is for educational and personal use only.
# ---------------------------------------------------------