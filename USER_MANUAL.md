# USER MANUAL — Hyderabad Air Quality Project
### Written like a step-by-step recipe. Follow in order. Don't skip.

You should have these 5 files (I gave them to you):
- `config.py`
- `setup_db.py`
- `collect_data.py`
- `analyze.py`
- `requirements.txt`

Put all 5 in the SAME folder on your computer. Do not rename them.

---

## PART 0 — One-time setup (do this first, only once)

### Step 1: Check Python is installed
Open a terminal / command prompt and type:
```
python --version
```
If you see a version number (like `Python 3.11.2`), you're good.
If not, install Python from https://www.python.org/downloads/ first.

### Step 2: Go into your project folder
```
cd path/to/your/folder
```
(Replace `path/to/your/folder` with wherever you saved the 5 files.)

### Step 3: Install the helper tools (libraries)
```
pip install -r requirements.txt
```
This installs `requests` (to talk to websites), `pandas` (to organize numbers),
and `matplotlib` (to draw charts). You only do this once.

### Step 4: Get your free API token
1. Go to: https://aqicn.org/data-platform/token/
2. Type your email and submit.
3. You'll get a token (a long code) — either instantly on screen or by email.
4. Open `config.py` in any text editor (Notepad, VS Code, anything).
5. Find this line:
   ```python
   WAQI_TOKEN = "PASTE_YOUR_TOKEN_HERE"
   ```
6. Replace `PASTE_YOUR_TOKEN_HERE` with your real token, keeping the quotes.
   Example: `WAQI_TOKEN = "abc123xyz456"`
7. Save the file.

### Step 5: Create your empty database
Run:
```
python setup_db.py
```
You should see:
```
Success! Database 'aqi_data.db' is ready with empty tables.
```
A new file called `aqi_data.db` will appear in your folder. That's your storage box — don't delete it.

**You only do Part 0 once. Everything below, you repeat.**

---

## PART 1 — Collecting data (Day 1, 2, and 3)

Every 2 hours (or as often as you can — even every 3-4 hours is fine), run:
```
python collect_data.py
```

Each time, you'll see something like:
```
Starting data collection...
  Saved: Bahadurpura -> AQI 87
  Saved: ICRISAT Patancheru -> AQI 91
  Saved: Zoo Park -> AQI 76
Done! Saved readings for 3 station(s) at 2026-07-22 10:00:00.
```

That means it worked. Just run this same command again later — it keeps ADDING
new rows, it never deletes old ones. Do this across all 3 days as many times
as you reasonably can (aim for at least 3-4 times per day).

**If you see an error instead:**
- "Something went wrong talking to WAQI" → double-check your token in `config.py`
  is correct and has no extra spaces or missing quotes.
- Internet connection issue → just try again in a few minutes.

---

## PART 2 — Analyzing your data (after at least 1 full day of collecting)

Once you've run `collect_data.py` several times across at least a day, run:
```
python analyze.py
```

This will:
1. Print simple summaries in your terminal (worst station, worst hour, etc.)
2. Look for anomalies (unusual pollution spikes) and print them
3. Save a chart picture: `aqi_trend_chart.png`
4. Save a text summary: `findings.txt`
5. Save two CSV files: `aqi_readings_export.csv` and `weather_readings_export.csv`

**Open `findings.txt`** — at the bottom, there's a blank space asking you to
write your own one-paragraph guess about WHY the anomaly happened. Look at
the weather numbers around that same time (low wind or high humidity often
makes pollution worse) and write 2-3 honest sentences.

You can run `python analyze.py` again anytime — it will just refresh the
chart and findings using whatever data you've collected so far.

---

## PART 3 — Building your dashboard (Day 3)

1. Open Power BI Desktop (or Tableau, whichever you know).
2. Import the file `aqi_readings_export.csv` (Get Data → Text/CSV).
3. Also import `weather_readings_export.csv` if you want to show weather too.
4. Build:
   - A number card showing the latest/average AQI
   - A line chart: Time (x-axis) vs AQI (y-axis), split by station
   - A bar chart comparing stations by average AQI
5. Add a text box with your one-paragraph finding from `findings.txt`.
6. Save/export your dashboard as a PDF or screenshot for your portfolio.

---

## PART 4 — Putting it on GitHub (so you can show it to recruiters)

1. Create a free GitHub account at https://github.com if you don't have one.
2. Create a "New repository" — name it something like `hyderabad-aqi-analysis`.
3. Upload these files:
   - `collect_data.py`, `analyze.py`, `setup_db.py`, `config.py` (remove your real token before uploading — put back `PASTE_YOUR_TOKEN_HERE`)
   - `findings.txt`
   - `aqi_trend_chart.png`
   - A screenshot of your Power BI/Tableau dashboard
4. Write a short description at the top of the repository (a README) explaining:
   - What the project does
   - What data source you used
   - What you found (your anomaly + explanation)
   - What tools you used (Python, SQL/SQLite, Power BI)

**Important: Before uploading `config.py` to GitHub, delete your real token
and put back `PASTE_YOUR_TOKEN_HERE`.** Never upload your real token publicly.

---

## Quick Checklist
- [ ] Part 0 done once (Python installed, libraries installed, token added, database created)
- [ ] Collected data at least 3-4 times per day for 3 days
- [ ] Ran `analyze.py` and got a chart + findings.txt
- [ ] Wrote my own paragraph explaining the anomaly
- [ ] Built a dashboard in Power BI/Tableau
- [ ] Uploaded everything to GitHub (with token removed from config.py)
- [ ] Wrote 2-3 resume bullet points about this project
