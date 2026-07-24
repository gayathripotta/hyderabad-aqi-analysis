"""
analyze.py
----------
Run this file AFTER you've collected data for at least 1-2 days.
(You need multiple readings over time for this to find anything useful.)

It does 4 things:
  1. Prints simple SQL-style answers (worst station, worst hour, etc.)
  2. Finds "anomalies" - unusual pollution spikes
  3. Draws a chart and saves it as a picture (aqi_trend_chart.png)
  4. Saves a plain-English findings summary (findings.txt)

HOW TO USE:
  Run this command:      python analyze.py
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from config import DB_NAME


def load_data():
    conn = sqlite3.connect(DB_NAME)
    aqi_df = pd.read_sql_query("SELECT * FROM aqi_readings", conn)
    weather_df = pd.read_sql_query("SELECT * FROM weather_readings", conn)
    conn.close()

    aqi_df["reading_time"] = pd.to_datetime(aqi_df["reading_time"])
    weather_df["reading_time"] = pd.to_datetime(weather_df["reading_time"])
    return aqi_df, weather_df


def run_sql_style_summaries(aqi_df):
    print("\n========== SIMPLE SUMMARIES ==========")

    print("\n-- Average AQI per station --")
    avg_by_station = aqi_df.groupby("station_name")["aqi"].mean().sort_values(ascending=False)
    print(avg_by_station)

    print("\n-- Worst single reading recorded --")
    worst_row = aqi_df.loc[aqi_df["aqi"].idxmax()]
    print(worst_row[["station_name", "reading_time", "aqi"]])

    print("\n-- Average AQI by hour of day --")
    aqi_df["hour"] = aqi_df["reading_time"].dt.hour
    avg_by_hour = aqi_df.groupby("hour")["aqi"].mean().sort_values(ascending=False)
    print(avg_by_hour)

    return avg_by_station, avg_by_hour


def find_anomalies(aqi_df):
    """
    An 'anomaly' here means: a reading that is much higher than the
    normal (average) reading for that same station.
    We flag anything more than 2 standard deviations above the mean.
    """
    print("\n========== ANOMALIES FOUND ==========")

    anomalies = []
    for station, group in aqi_df.groupby("station_name"):
        mean_aqi = group["aqi"].mean()
        std_aqi = group["aqi"].std()
        if pd.isna(std_aqi) or std_aqi == 0:
            continue
        threshold = mean_aqi + 2 * std_aqi
        flagged = group[group["aqi"] > threshold]
        for _, row in flagged.iterrows():
            anomalies.append({
                "station": station,
                "time": row["reading_time"],
                "aqi": row["aqi"],
                "normal_average": round(mean_aqi, 1)
            })

    if not anomalies:
        print("No anomalies found yet — you may need more data (collect for longer).")
    else:
        for a in anomalies:
            print(f"  {a['station']} at {a['time']}: AQI {a['aqi']} "
                  f"(normal average is {a['normal_average']})")

    return anomalies


def make_chart(aqi_df):
    plt.figure(figsize=(10, 5))
    for station, group in aqi_df.groupby("station_name"):
        group = group.sort_values("reading_time")
        plt.plot(group["reading_time"], group["aqi"], marker="o", label=station)

    plt.title("AQI Trend Over Time - Hyderabad Stations")
    plt.xlabel("Time")
    plt.ylabel("AQI")
    plt.legend(fontsize=8)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("aqi_trend_chart.png")
    print("\nChart saved as: aqi_trend_chart.png")


def write_findings(avg_by_station, avg_by_hour, anomalies):
    with open("findings.txt", "w") as f:
        f.write("AIR QUALITY FINDINGS SUMMARY\n")
        f.write("=============================\n\n")

        f.write("Most polluted station (on average):\n")
        f.write(f"  {avg_by_station.index[0]} - average AQI {round(avg_by_station.iloc[0], 1)}\n\n")

        f.write("Worst hour of the day (on average):\n")
        f.write(f"  {avg_by_hour.index[0]}:00 - average AQI {round(avg_by_hour.iloc[0], 1)}\n\n")

        f.write(f"Number of anomalies (unusual spikes) found: {len(anomalies)}\n")
        for a in anomalies:
            f.write(f"  - {a['station']} at {a['time']}: AQI {a['aqi']} "
                    f"(normal average {a['normal_average']})\n")

        f.write("\nWrite your own one-paragraph explanation here about WHY you think\n")
        f.write("these anomalies happened (check the weather_readings table for clues:\n")
        f.write("low wind speed and high humidity often make pollution worse).\n")

    print("Findings summary saved as: findings.txt")
    print("Open it and add your own explanation paragraph at the bottom.")


def main():
    aqi_df, weather_df = load_data()

    if aqi_df.empty:
        print("No data found yet! Run collect_data.py a few times first, over a few hours/days.")
        return

    avg_by_station, avg_by_hour = run_sql_style_summaries(aqi_df)
    anomalies = find_anomalies(aqi_df)
    make_chart(aqi_df)
    write_findings(avg_by_station, avg_by_hour, anomalies)

    # Also export a clean CSV so it's easy to import into Power BI / Tableau
    aqi_df.to_csv("aqi_readings_export.csv", index=False)
    weather_df.to_csv("weather_readings_export.csv", index=False)
    print("\nExported aqi_readings_export.csv and weather_readings_export.csv")
    print("Import these two CSV files into Power BI or Tableau to build your dashboard.")


if __name__ == "__main__":
    main()
