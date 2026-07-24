Hyderabad Air Quality Analysis

A real-time data pipeline that collects live air quality readings from monitoring stations across Hyderabad, stores them in a database, analyzes them using SQL and Python, and visualizes the results in a Power BI dashboard.

Problem Statement

Air pollution varies significantly across different parts of a city. This project collects live AQI (Air Quality Index) data across multiple Hyderabad monitoring stations to identify which areas have notably higher pollution and explore possible causes.

Data Sources
WAQI API (aqicn.org) — live AQI and pollutant readings (PM2.5, PM10, NO2, SO2, CO, O3) across 9 Hyderabad monitoring stations
Open-Meteo API — live weather data (temperature, humidity, wind speed) for the same period
Method
Built a Python script to pull live readings from both APIs and store them in a SQLite database
Ran the collection script repeatedly over multiple days to build a real-world dataset
Used SQL queries and pandas to calculate average AQI per station and by hour
Applied statistical anomaly detection (rolling mean ± 2 standard deviations) to flag unusual spikes
Built a Power BI dashboard with a comparison chart, an average AQI KPI card, and a written insight
Key Finding

Across all nine monitored stations, Bollaram Industrial Area recorded the highest AQI at 156 — more than 60 points above the next-highest station and over 10 times higher than the cleanest station (Central University, AQI 4). Since Bollaram Industrial Area is an industrial zone, this gap is more likely explained by local industrial emissions than short-term weather changes, especially since AQI values stayed constant across the data collection period rather than fluctuating with wind speed or humidity. Future monitoring could help track whether pollution levels there change with production activity or time of day, once station-level updates refresh more frequently.

Tools Used

Python, SQL (SQLite), pandas, matplotlib, Power BI

Files in this repo
collect_data.py — pulls live AQI + weather data and saves to database
setup_db.py — creates the database tables (run once)
analyze.py — runs SQL-style summaries, anomaly detection, and exports charts/CSVs
findings.txt — written summary of results
aqi_trend_chart.png — chart of AQI trends
aqi_dashboard.png — Power BI dashboard screenshot
requirements.txt — Python packages needed to run this project
How to Run

See USER_MANUAL.md for full setup instructions.
