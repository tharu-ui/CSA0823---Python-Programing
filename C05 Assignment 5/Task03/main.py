import csv
import sqlite3
import time
import cProfile
import pstats
import tracemalloc
from pathlib import Path
from datetime import date, timedelta

import pandas as pd

BASE = Path(__file__).parent
DATA = BASE / "data"
OUTPUT = BASE / "outputs"

DATA.mkdir(exist_ok=True)
OUTPUT.mkdir(exist_ok=True)

READINGS_PER_STATION = 8760
SIZES = [1, 12, 120]


def generate_dataset(station_count):
    filename = DATA / f"air_quality_{station_count}_stations.csv"

    start_date = date(2026, 1, 1)

    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["station", "date", "hour", "pm25"])

        for station_number in range(station_count):
            station = f"Station_{station_number + 1}"

            for reading in range(READINGS_PER_STATION):
                current_date = start_date + timedelta(
                    days=reading // 24
                )
                hour = reading % 24

                pm25 = round(
                    30 + station_number * 2
                    + (reading % 24) * 0.5
                    + (reading % 7), 2
                )

                writer.writerow([
                    station,
                    current_date.isoformat(),
                    hour,
                    pm25
                ])

    return filename


def python_loop(filename):
    totals = {}
    counts = {}

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            key = (row["station"], row["date"])
            value = float(row["pm25"])

            totals[key] = totals.get(key, 0) + value
            counts[key] = counts.get(key, 0) + 1

    return {
        key: totals[key] / counts[key]
        for key in totals
    }


def pandas_groupby(filename):
    df = pd.read_csv(filename)

    result = df.groupby(
        ["station", "date"]
    )["pm25"].mean()

    return result.to_dict()


def sql_groupby(filename, database):
    if database.exists():
        database.unlink()

    con = sqlite3.connect(database)
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE readings (
            station TEXT,
            day TEXT,
            hour INTEGER,
            pm25 REAL
        )
    """)

    batch = []

    with open(filename, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:
            batch.append((
                row["station"],
                row["date"],
                int(row["hour"]),
                float(row["pm25"])
            ))

            if len(batch) == 10000:
                cur.executemany(
                    "INSERT INTO readings VALUES (?, ?, ?, ?)",
                    batch
                )
                batch.clear()

        if batch:
            cur.executemany(
                "INSERT INTO readings VALUES (?, ?, ?, ?)",
                batch
            )

    con.commit()

    start = time.perf_counter()

    cur.execute("""
        SELECT station, day, AVG(pm25)
        FROM readings
        GROUP BY station, day
    """)

    result = {
        (row[0], row[1]): row[2]
        for row in cur.fetchall()
    }

    query_time = time.perf_counter() - start

    con.close()

    return result, query_time


def verify_results(first, second, third):
    if set(first) != set(second) or set(first) != set(third):
        return False

    for key in first:
        if abs(first[key] - second[key]) > 1e-8:
            return False

        if abs(first[key] - third[key]) > 1e-8:
            return False

    return True


def measure_python(filename):
    tracemalloc.start()

    start = time.perf_counter()
    result = python_loop(filename)
    elapsed = time.perf_counter() - start

    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    return result, elapsed, peak / (1024 * 1024)


def profile_python(filename):
    profiler = cProfile.Profile()

    profiler.enable()
    python_loop(filename)
    profiler.disable()

    output_file = OUTPUT / "profile_report.txt"

    with open(output_file, "w") as file:
        stats = pstats.Stats(profiler, stream=file)
        stats.sort_stats("cumulative")
        stats.print_stats(20)

    print("\nProfiling report saved:", output_file)


def main():
    print("LOOPS VS PANDAS VS SQL")
    print("=" * 55)

    results = []

    for station_count in SIZES:
        print(f"\n--- {station_count} STATION(S) ---")

        filename = generate_dataset(station_count)

        print("Dataset generated:", filename)
        print("Total readings:", station_count * READINGS_PER_STATION)

        python_result, python_time, memory = measure_python(filename)

        start = time.perf_counter()
        pandas_result = pandas_groupby(filename)
        pandas_time = time.perf_counter() - start

        database = DATA / f"air_quality_{station_count}.db"

        sql_result, sql_time = sql_groupby(filename, database)

        correct = verify_results(
            python_result, pandas_result, sql_result
        )

        print("\nExecution times:")
        print(f"Python loops: {python_time:.6f} seconds")
        print(f"Pandas:       {pandas_time:.6f} seconds")
        print(f"SQL query:    {sql_time:.6f} seconds")

        print(f"Python peak memory: {memory:.2f} MB")
        print("All three methods agree:", correct)
        print("Daily summary records:", len(python_result))

        results.append([
            station_count,
            station_count * READINGS_PER_STATION,
            python_time,
            pandas_time,
            sql_time,
            memory,
            correct
        ])

        if station_count == 120:
            profile_python(filename)

    with open(
        OUTPUT / "benchmark_results.csv",
        "w",
        newline=""
    ) as file:
        writer = csv.writer(file)

        writer.writerow([
            "Stations", "Readings", "Python Time",
            "Pandas Time", "SQL Query Time",
            "Python Peak Memory MB", "Correctness"
        ])

        writer.writerows(results)

    print("\n--- FINAL BENCHMARK TABLE ---")

    for row in results:
        print(row)

    print("\nResults saved in outputs/benchmark_results.csv")
    print("TASK 03 COMPLETED SUCCESSFULLY.")


if __name__ == "__main__":
    main()
