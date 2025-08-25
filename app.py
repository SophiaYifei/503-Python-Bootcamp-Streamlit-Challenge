import os
import re
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import matplotlib.pyplot as plt


# --- Streamlit page config ---
st.set_page_config(page_title="Weather App", page_icon="⛅", layout="centered")
st.title("⛅ Simple Weather App")

# --- Load API key ---
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    st.error("Missing OPENWEATHER_API_KEY. Create a `.env` file with:\n`OPENWEATHER_API_KEY=your_key_here`")
    st.stop()

API_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- tiny helper: description -> emoji ---
def weather_emoji(desc: str) -> str:
    d = desc.lower()
    if "rain" in d or "drizzle" in d:
        return "🌧️"
    if "storm" in d or "thunder" in d:
        return "⛈️"
    if "snow" in d:
        return "❄️"
    if "cloud" in d or "overcast" in d:
        return "☁️"
    if "clear" in d or "sun" in d:
        return "☀️"
    if "fog" in d or "mist" in d or "haze" in d:
        return "🌫️"
    return "🌈"

# --- API call ---
def fetch_weather(city: str) -> dict:
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",   # Celsius
        "lang": "en",
    }
    resp = requests.get(API_URL, params=params, timeout=10)
    data = resp.json()

    if resp.status_code != 200 or str(data.get("cod")) != "200": # check API error
        msg = data.get("message", "Unknown API error")
        raise RuntimeError(msg)
    return data

# --- UI: input ---
city_raw = st.text_input(
    "Enter a U.S. city (e.g., `Raleigh` or `Raleigh,US-NC`):",
    placeholder="Raleigh",
)
city = re.sub(r"\s+", " ", city_raw.strip()) if city_raw else ""

# only create button once
btn = st.button("Get weather", key="btn_get_weather")

if btn:
    if not city:
        st.warning("Please enter a city.")
    else:
        with st.spinner("Fetching weather..."):
            try:
                data = fetch_weather(city)
                city_name = data["name"]
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                description = data["weather"][0]["description"]
                emoji = weather_emoji(description)

                st.subheader(f"{emoji}  {city_name}")
                st.write(f"**Temperature:** {temp} °C")
                st.write(f"**Humidity:** {humidity} %")
                st.write(f"**Description:** {description.capitalize()}")

                chart_df = pd.DataFrame(
                    {"metric": ["Temperature (°C)", "Humidity (%)"], "value": [temp, humidity]}
                ).set_index("metric")
                st.bar_chart(chart_df)
            
                
                # --- simple two-color bar chart with Matplotlib ---
                labels = ["Temperature (°C)", "Humidity (%)"]
                values = [temp, humidity]
                
                fig, ax = plt.subplots(figsize=(4, 3))
                ax.bar(labels, values, color=["tab:blue", "tab:orange"])  # two colors
                ax.set_title("Current Weather Metrics")
                ax.set_ylabel("") 
                ax.set_xlabel("")
                # show value on top of each bar
                for i, v in enumerate(values):
                  ax.text(i, v, f"{v}", ha="center", va="bottom")

                st.pyplot(fig)


                with st.expander("Show raw JSON"):
                 st.json(data)

            except Exception as e:
                st.error(f"Failed to fetch weather for `{city}`: {e}")
