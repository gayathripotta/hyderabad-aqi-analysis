"""
setup_db.py
-----------
Run this file ONCE, first, before anything else.
It creates a small database file on your computer with two empty tables:
  1. aqi_readings    -> will store pollution numbers
  2. weather_readings -> will store weather numbers

You don't need to understand SQL to run this. Just run:
    python setup_db.py
"""

import sqlite3
from config import DB_NAME

def setup_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Table 1: pollution readings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aqi_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_name TEXT,
            reading_time TEXT,
            aqi INTEGER,
            pm25 REAL,
            pm10 REAL,
            no2 REAL,
            so2 REAL,
            co REAL,
            o3 REAL,
            dominant_pollutant TEXT
        )
    """)

    # Table 2: weather readings
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            reading_time TEXT,
            temperature REAL,
            humidity REAL,
            wind_speed REAL
        )
    """)

    conn.commit()
    conn.close()
    print(f"Success! Database '{DB_NAME}' is ready with empty tables.")
    print("Next step: run 'python collect_data.py' to start pulling live numbers.")

if __name__ == "__main__":
    setup_database()
