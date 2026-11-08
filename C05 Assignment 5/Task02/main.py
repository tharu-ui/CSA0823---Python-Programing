
import csv
import sqlite3
import time
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "outputs"
OUTPUT.mkdir(exist_ok=True)


def create_test_files():
    (OUTPUT / "missing_column.csv").write_text(
        "station,date\nAdyar,2026-10-01\n"
    )

    (OUTPUT / "wrong_delimiter.csv").write_text(
        "station;date;pm25\nAdyar;2026-10-01;48\n"
    )

    (OUTPUT / "empty.csv").write_text("")

    with open(OUTPUT / "different_encoding.csv",
              "w", encoding="latin-1") as file:
        file.write("station,date,pm25\nCafé,2026-10-01,48\n")

    print("Adversarial test files created.")


def test_csv_files():
    print("\n--- CSV ADVERSARIAL TESTS ---")

    for filename in [
        "missing_column.csv",
        "wrong_delimiter.csv",
        "different_encoding.csv",
        "empty.csv"
    ]:
        path = OUTPUT / filename
        print("\nTesting:", filename)

        try:
            if path.stat().st_size == 0:
                raise ValueError("File is empty")

            with open(path, "r", encoding="utf-8-sig",
                      newline="") as file:
                reader = csv.DictReader(file)
                headers = reader.fieldnames

                if not headers:
                    raise ValueError("Missing header")

                required = {"station", "date", "pm25"}

                if not required.issubset(set(headers)):
                    raise ValueError(
                        "Missing required columns or wrong delimiter"
                    )

                rows = list(reader)
                print("Valid CSV structure.")
                print("Records:", rows)

        except UnicodeDecodeError:
            print("Error: Unsupported text encoding.")

        except (ValueError, csv.Error) as error:
            print("Error:", error)


def test_sql_injection():
    print("\n--- SQL INJECTION TEST ---")

    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE readings (
            station TEXT,
            pm25 REAL
        )
    """)

    cur.executemany(
        "INSERT INTO readings VALUES (?, ?)",
        [
            ("Adyar", 48.0),
            ("Guindy", 95.0),
            ("Velachery", 60.0)
        ]
    )

    name = "Adyar' OR '1'='1"

    print("\n1. Unsafe SQL using string concatenation:")

    unsafe_query = (
        "SELECT * FROM readings WHERE station = '" + name + "'"
    )

    try:
        cur.execute(unsafe_query)
        print(cur.fetchall())
    except sqlite3.Error as error:
        print("SQL error:", error)

    print("\n2. Safe parameterised SQL:")

    cur.execute(
        "SELECT * FROM readings WHERE station = ?",
        (name,)
    )

    print("Result:", cur.fetchone())

    con.close()


POSITIVE = {"good", "clean", "fast", "helpful", "improved"}
NEGATIVE = {"bad", "dirty", "slow", "rude", "smoke", "broken"}
NEGATORS = {"not", "never", "no"}


def score(text):
    words = text.lower().replace(".", " ").replace(
        ",", " "
    ).split()

    total = 0

    for i, word in enumerate(words):
        value = 1 if word in POSITIVE else -1 if word in NEGATIVE else 0

        if i > 0 and words[i - 1] in NEGATORS:
            value = -value

        total += value

    return total


def label(text):
    value = score(text)

    if value > 0:
        return "positive"
    elif value < 0:
        return "negative"
    return "neutral"


def test_sentiment():
    print("\n--- SENTIMENT ADVERSARIAL TEST ---")

    complaints = [
        "The road is clean and the bus is fast.",
        "The factory smoke is bad.",
        "The service is not good.",
        "The service is not bad.",
        "The roads are not clean.",
        "The service is never not good.",
        "The bus is good but the road is dirty.",
        "Wonderful! Another day of breathing smoke.",
        "The staff are helpful but the air is dirty."
    ]

    for complaint in complaints:
        print(f"{label(complaint):8} | {complaint}")


def compare_insertion_methods():
    print("\n--- INSERTION PERFORMANCE ---")

    data = [(f"Station{i}", float(i)) for i in range(10000)]

    con = sqlite3.connect(":memory:")
    cur = con.cursor()

    cur.execute("CREATE TABLE test (station TEXT, pm25 REAL)")

    start = time.perf_counter()

    cur.executemany(
        "INSERT INTO test VALUES (?, ?)", data
    )

    executemany_time = time.perf_counter() - start

    cur.execute("DELETE FROM test")
    con.commit()

    start = time.perf_counter()

    for row in data:
        cur.execute(
            "INSERT INTO test VALUES (?, ?)", row
        )

    execute_time = time.perf_counter() - start

    print(f"executemany(): {executemany_time:.6f} seconds")
    print(f"execute() loop: {execute_time:.6f} seconds")

    con.close()


def main():
    print("ADVERSARIAL DATA TESTING SYSTEM")
    print("=" * 45)

    create_test_files()
    test_csv_files()
    test_sql_injection()
    test_sentiment()
    compare_insertion_methods()

    print("\nTASK 02 COMPLETED SUCCESSFULLY.")


if __name__ == "__main__":
    main()
