
import csv
import sqlite3
import statistics
import math
from pathlib import Path
from datetime import date, timedelta
import matplotlib.pyplot as plt

BASE = Path(__file__).parent
OUTPUT = BASE / "outputs"
GRAPHS = BASE / "graphs"

OUTPUT.mkdir(exist_ok=True)
GRAPHS.mkdir(exist_ok=True)

RAW_FILE = OUTPUT / "raw_air_quality.csv"
CLEAN_FILE = OUTPUT / "clean_air_quality.csv"
DB_FILE = OUTPUT / "air_quality.db"

STATIONS = [
    "Adyar", "Guindy", "Velachery", "T Nagar",
    "Anna Nagar", "Tambaram", "Porur", "Chromepet",
    "Ambattur", "Perungudi", "Mylapore", "Thiruvanmiyur"
]


def generate_data():
    fields = [
        "station", "date", "hour", "pm25",
        "pm10", "no", "temperature", "unit"
    ]

    rows = []
    start = date(2026, 10, 1)

    for s_index, station in enumerate(STATIONS):
        for day in range(30):
            current_date = start + timedelta(days=day)

            for hour in [0, 6, 12, 18]:
                pm25 = round(
                    35 + s_index * 3 + 12 * math.sin(day / 4)
                    + hour / 3, 2
                )
                pm10 = round(pm25 * 1.8, 2)
                no = round(10 + s_index + day / 5, 2)
                temp = round(25 + 5 * math.sin(day / 5)
                             + hour / 8, 2)

                unit = "F" if station in ["Adyar", "Guindy"] else "C"

                if unit == "F":
                    temp = round(temp * 9 / 5 + 32, 2)

                rows.append({
                    "station": station,
                    "date": current_date.isoformat(),
                    "hour": hour,
                    "pm25": pm25,
                    "pm10": pm10,
                    "no": no,
                    "temperature": temp,
                    "unit": unit
                })

    # Introduce missing values
    rows[2]["pm25"] = "NA"
    rows[10]["pm10"] = ""
    rows[25]["no"] = "NA"

    # Introduce impossible negative readings
    rows[30]["pm25"] = -10
    rows[40]["pm10"] = -20
    rows[50]["no"] = -5

    # Introduce impossibly large readings
    rows[60]["pm25"] = 1500
    rows[70]["pm10"] = 2000
    rows[80]["no"] = 1000

    # Introduce an invalid temperature
    rows[90]["temperature"] = 200

    # Introduce a duplicate record
    rows.append(rows[0].copy())

    with open(RAW_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print("Raw air-quality dataset generated.")
    print("Total raw records:", len(rows))


def read_raw_data():
    with open(RAW_FILE, "r", newline="") as file:
        return list(csv.DictReader(file))


def clean_data(raw_rows):
    seen = set()
    cleaned = []
    rejected = 0
    duplicates = 0

    for row in raw_rows:
        key = (row["station"], row["date"], row["hour"])

        if key in seen:
            duplicates += 1
            continue

        seen.add(key)

        try:
            temperature = float(row["temperature"])
            if row["unit"] == "F":
                temperature = (temperature - 32) * 5 / 9

            if not -50 <= temperature <= 60:
                temperature = None
        except (ValueError, TypeError):
            temperature = None

        values = {}

        for column, maximum in [
            ("pm25", 999), ("pm10", 999), ("no", 500)
        ]:
            try:
                value = float(row[column])
                if not 0 <= value <= maximum:
                    value = None
            except (ValueError, TypeError):
                value = None

            values[column] = value

        cleaned.append({
            "station": row["station"].strip().title(),
            "date": row["date"],
            "hour": int(row["hour"]),
            "pm25": values["pm25"],
            "pm10": values["pm10"],
            "no": values["no"],
            "temperature": temperature
        })

    # Replace missing or invalid values using column medians
    columns = ["pm25", "pm10", "no", "temperature"]

    for column in columns:
        valid = [
            row[column] for row in cleaned
            if row[column] is not None
        ]
        median_value = statistics.median(valid)

        for row in cleaned:
            if row[column] is None:
                row[column] = median_value
                rejected += 1

    # Min-max normalisation of PM2.5
    pm_values = [row["pm25"] for row in cleaned]
    minimum = min(pm_values)
    maximum = max(pm_values)

    for row in cleaned:
        if maximum != minimum:
            row["pm25_normalized"] = round(
                (row["pm25"] - minimum) / (maximum - minimum), 3
            )
        else:
            row["pm25_normalized"] = 0.0

    print("\nCleaning completed.")
    print("Duplicate records removed:", duplicates)
    print("Missing/invalid values replaced:", rejected)
    print("Valid records:", len(cleaned))

    return cleaned


def save_clean_data(rows):
    fields = [
        "station", "date", "hour", "pm25",
        "pm10", "no", "temperature", "pm25_normalized"
    ]

    with open(CLEAN_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def store_database(rows):
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS stations")
    cur.execute("DROP TABLE IF EXISTS readings")

    cur.execute("""
        CREATE TABLE stations (
            station_id INTEGER PRIMARY KEY,
            station_name TEXT UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE readings (
            station TEXT,
            day TEXT,
            hour INTEGER,
            pm25 REAL,
            pm10 REAL,
            no REAL,
            temperature REAL,
            pm25_normalized REAL,
            PRIMARY KEY (station, day, hour)
        )
    """)

    stations = [(name,) for name in STATIONS]
    cur.executemany(
        "INSERT INTO stations (station_name) VALUES (?)",
        stations
    )

    data = [
        (
            r["station"], r["date"], r["hour"],
            r["pm25"], r["pm10"], r["no"],
            r["temperature"], r["pm25_normalized"]
        )
        for r in rows
    ]

    cur.executemany("""
        INSERT INTO readings VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, data)

    con.commit()

    print("\nSQLite database created successfully.")
    print("Records stored:", len(data))

    return con


def run_queries(con):
    cur = con.cursor()

    print("\n--- SQL QUERY RESULTS ---")

    print("\n1. Average PM2.5 of each station in October:")
    cur.execute("""
        SELECT station, ROUND(AVG(pm25), 2)
        FROM readings
        GROUP BY station
        ORDER BY station
    """)

    for row in cur.fetchall():
        print(row)

    print("\n2. Comparison of station pollution levels:")
    cur.execute("""
        SELECT station, ROUND(AVG(pm25), 2)
        FROM readings
        GROUP BY station
        ORDER BY AVG(pm25) DESC
        LIMIT 5
    """)

    for row in cur.fetchall():
        print(row)

    print("\n3. Hours with the worst average air quality:")
    cur.execute("""
        SELECT hour, ROUND(AVG(pm25), 2)
        FROM readings
        GROUP BY hour
        ORDER BY AVG(pm25) DESC
    """)

    for row in cur.fetchall():
        print(row)


def create_summary(con):
    cur = con.cursor()

    cur.execute("""
        SELECT station, day,
               MIN(pm25), MAX(pm25), AVG(pm25), COUNT(pm25)
        FROM readings
        GROUP BY station, day
        ORDER BY station, day
    """)

    rows = cur.fetchall()

    with open(OUTPUT / "daily_summary.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Station", "Date", "Minimum", "Maximum",
            "Mean", "Valid Readings"
        ])
        writer.writerows(rows)

    print("\nDaily summary generated.")
    print("Daily summary records:", len(rows))


def create_charts(con):
    cur = con.cursor()

    # Chart 1: Monthly PM2.5 trend
    cur.execute("""
        SELECT day, AVG(pm25)
        FROM readings
        GROUP BY day
        ORDER BY day
    """)
    data = cur.fetchall()

    plt.figure(figsize=(10, 5))
    plt.plot(
        [r[0] for r in data],
        [r[1] for r in data],
        marker="o"
    )
    plt.title("Monthly PM2.5 Trend")
    plt.xlabel("Date")
    plt.ylabel("Average PM2.5")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(GRAPHS / "monthly_trend.png")
    plt.close()

    # Chart 2: Station comparison
    cur.execute("""
        SELECT station, AVG(pm25)
        FROM readings
        GROUP BY station
        ORDER BY station
    """)
    data = cur.fetchall()

    plt.figure(figsize=(11, 5))
    plt.bar([r[0] for r in data], [r[1] for r in data])
    plt.title("PM2.5 Comparison Across Stations")
    plt.xlabel("Station")
    plt.ylabel("Average PM2.5")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(GRAPHS / "station_comparison.png")
    plt.close()

    # Chart 3: Temperature and PM2.5 relationship
    cur.execute("SELECT temperature, pm25 FROM readings")
    data = cur.fetchall()

    plt.figure(figsize=(8, 5))
    plt.scatter(
        [r[0] for r in data],
        [r[1] for r in data],
        alpha=0.5
    )
    plt.title("Temperature vs PM2.5")
    plt.xlabel("Temperature (Celsius)")
    plt.ylabel("PM2.5")
    plt.tight_layout()
    plt.savefig(GRAPHS / "temperature_pm25.png")
    plt.close()

    # Chart 4: Worst pollution hours
    cur.execute("""
        SELECT hour, AVG(pm25)
        FROM readings
        GROUP BY hour
        ORDER BY hour
    """)
    data = cur.fetchall()

    plt.figure(figsize=(8, 5))
    plt.bar(
        [str(r[0]) + ":00" for r in data],
        [r[1] for r in data]
    )
    plt.title("Average PM2.5 by Hour")
    plt.xlabel("Hour")
    plt.ylabel("Average PM2.5")
    plt.tight_layout()
    plt.savefig(GRAPHS / "worst_hours.png")
    plt.close()

    print("\nFour charts generated successfully.")


def complete_code_test():
    print("\n--- COMPLETE THE CODE TEST ---")

    raw = """station,date,pm25
Adyar,2026-10-01,48
Adyar,2026-10-02,NA
Adyar,2026-10-03,
Guindy,2026-10-01,95
Guindy,2026-10-02,-5
Guindy,2026-10-03,121
Guindy,2026-10-04,1200
"""

    rows = []
    reader = csv.DictReader(raw.splitlines())

    for row in reader:
        value = row["pm25"].strip()

        if not value or value == "NA":
            continue

        pm = float(value)

        if pm < 0 or pm > 999:
            continue

        rows.append((row["station"], row["date"], pm))

    values = [pm for _, _, pm in rows]
    minimum = min(values)
    maximum = max(values)

    if maximum == minimum:
        scaled = [0.0 for v in values]
    else:
        scaled = [
            round((v - minimum) / (maximum - minimum), 3)
            for v in values
        ]

    print(rows)
    print(scaled)


def main():
    print("CITY AIR-QUALITY MONITORING SYSTEM")
    print("=" * 45)

    generate_data()

    raw = read_raw_data()

    print("\n--- BEFORE CLEANING ---")
    print("Total records:", len(raw))
    for row in raw[:5]:
        print(row)

    cleaned = clean_data(raw)

    print("\n--- AFTER CLEANING ---")
    for row in cleaned[:5]:
        print(row)

    save_clean_data(cleaned)

    con = store_database(cleaned)
    run_queries(con)
    create_summary(con)
    create_charts(con)
    con.close()

    complete_code_test()

    print("\n--- FINAL STATUS ---")
    print("Raw CSV:", RAW_FILE)
    print("Clean CSV:", CLEAN_FILE)
    print("SQLite database:", DB_FILE)
    print("Daily summary:", OUTPUT / "daily_summary.csv")
    print("Charts folder:", GRAPHS)
    print("\nTASK 01 COMPLETED SUCCESSFULLY.")


if __name__ == "__main__":
    main()
