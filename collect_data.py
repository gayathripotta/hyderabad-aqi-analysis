"""
collect_data.py
----------------
This script does two things every time you run it:
  1. Asks the WAQI website: "what is the pollution level right now
     at each station in Hyderabad?" and saves the answer.
  2. Asks the Open-Meteo website: "what is the weather right now
     in Hyderabad?" and saves that too.

HOW TO USE:
  Run this command:      python collect_data.py
  Run it again every 2 hours (or as often as you can) for 3 days.
  Each time you run it, it ADDS new rows — it does not delete old ones.

You do not need to edit this file. Only edit config.py (for your token).
"""

import sqlite3
import requests
import datetime
from config import WAQI_TOKEN, CITY_KEYWORD, LATITUDE, LONGITUDE, DB_NAME


def get_hyderabad_stations():
    """
    Asks WAQI: 'which pollution-monitoring stations exist in Hyderabad?'
    Returns a list of station names + their unique IDs (uid).
    """
    url = f"https://api.waqi.info/search/?token={WAQI_TOKEN}&keyword={CITY_KEYWORD}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        print("Something went wrong talking to WAQI. Response was:")
        print(data)
        return []

    stations = []
    for item in data["data"]:
        stations.append({
            "uid": item["uid"],
            "name": item["station"]["name"]
        })
    return stations


def fetch_station_reading(uid):
    """
    Asks WAQI: 'what is the pollution reading right now at this exact station?'
    Returns a dictionary of pollution numbers.
    """
    url = f"https://api.waqi.info/feed/@{uid}/?token={WAQI_TOKEN}"
    response = requests.get(url)
    data = response.json()

    if data.get("status") != "ok":
        return None

    iaqi = data["data"].get("iaqi", {})

    def safe_get(key):
        # Some stations don't measure every pollutant - this avoids errors
        return iaqi.get(key, {}).get("v", None)

    return {
        "aqi": data["data"].get("aqi", None),
        "pm25": safe_get("pm25"),
        "pm10": safe_get("pm10"),
        "no2": safe_get("no2"),
        "so2": safe_get("so2"),
        "co": safe_get("co"),
        "o3": safe_get("o3"),
        "dominant_pollutant": data["data"].get("dominentpol", None),
    }


def fetch_weather():
    """
    Asks Open-Meteo: 'what is the weather right now in Hyderabad?'
    No signup or token needed for this one.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={LATITUDE}&longitude={LONGITUDE}"
        f"&current=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    response = requests.get(url)
    data = response.json()
    current = data.get("current", {})
    return {
        "temperature": current.get("temperature_2m"),
        "humidity": current.get("relative_humidity_2m"),
        "wind_speed": current.get("wind_speed_10m"),
    }


def save_to_database(station_name, reading_time, aqi_data, weather_data):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO aqi_readings
        (station_name, reading_time, aqi, pm25, pm10, no2, so2, co, o3, dominant_pollutant)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        station_name, reading_time,
        aqi_data["aqi"], aqi_data["pm25"], aqi_data["pm10"],
        aqi_data["no2"], aqi_data["so2"], aqi_data["co"], aqi_data["o3"],
        aqi_data["dominant_pollutant"]
    ))

    # Only save one weather row per run (weather is city-wide, not per-station)
    cursor.execute("""
        INSERT INTO weather_readings (reading_time, temperature, humidity, wind_speed)
        VALUES (?, ?, ?, ?)
    """, (
        reading_time, weather_data["temperature"],
        weather_data["humidity"], weather_data["wind_speed"]
    ))

    conn.commit()
    conn.close()


def main():
    print("Starting data collection...")
    reading_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    stations = get_hyderabad_stations()
    if not stations:
        print("No stations found. Check your token in config.py and try again.")
        return

    weather_data = fetch_weather()

    saved_count = 0
    for station in stations:
        aqi_data = fetch_station_reading(station["uid"])
        if aqi_data and aqi_data["aqi"] is not None:
            save_to_database(station["name"], reading_time, aqi_data, weather_data)
            saved_count += 1
            print(f"  Saved: {station['name']} -> AQI {aqi_data['aqi']}")

    print(f"Done! Saved readings for {saved_count} station(s) at {reading_time}.")
    print("Run this script again in 2 hours to add more data.")


if __name__ == "__main__":
    main()
