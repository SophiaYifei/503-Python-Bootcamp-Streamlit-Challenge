# ⛅ Simple Weather App (Streamlit + OpenWeather)

A minimal Streamlit app that fetches and displays the current weather for a user-entered city using the OpenWeather API.

## Features
- Input a city name in the Streamlit UI
- Calls OpenWeather Current Weather API
- Displays **Temperature (°C)**, **Humidity (%)**, and **Description**
- Tiny bar chart for temperature & humidity
- Emoji indicator based on description (e.g., ☀️, ☁️, 🌧️)
- Light input cleaning using **regex** (`\s+` → single space)

## Tech Stack
- Python, Streamlit, requests, python-dotenv, pandas

## Prerequisites
1. Python 3.9+ recommended
2. An OpenWeather API key (free tier is fine): https://openweathermap.org/api

## Setup

```bash
# (Optional) create and activate a virtual environment
python -m venv .venv
# Windows:
python -m venv .venv
.venv\Scripts\Activate.ps1
# macOS/Linux:
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create a .env file in the project root and add your key:
# (Do NOT commit this file)
# .env
OPENWEATHER_API_KEY=your_openweather_key_here

# Run
streamlit run app.py