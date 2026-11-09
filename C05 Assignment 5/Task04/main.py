
import sqlite3
import time
import re
import csv
import statistics
from pathlib import Path

BASE = Path(__file__).parent
DATA = BASE / "data"
OUTPUT = BASE / "outputs"

DATA.mkdir(exist_ok=True)
OUTPUT.mkdir(exist_ok=True)

POSITIVE = {
    "good", "clean", "fast", "helpful", "improved",
    "better", "excellent", "safe", "fresh", "pleasant"
}

NEGATIVE = {
    "bad", "dirty", "slow", "rude", "smoke",
    "broken", "polluted", "poor", "unsafe", "noise"
}

NEGATORS = {"not", "never", "no"}

STOPWORDS = {
    "the", "is", "are", "was", "were", "a", "an",
    "and", "or", "but", "in", "on", "at", "to",
    "of", "for", "from", "it", "this", "that",
    "with", "very", "has", "have", "been", "our",
    "we", "they", "their", "there", "today"
}

COMPLAINTS = [
    ("The roads are clean and the air is fresh.", "positive"),
    ("The factory smoke makes the air bad.", "negative"),
    ("The bus service is fast and helpful.", "positive"),
    ("The streets are dirty and polluted.", "negative"),
    ("The air quality is good today.", "positive"),
    ("The waste collection service is slow.", "negative"),
    ("The staff are helpful and polite.", "positive"),
    ("There is too much smoke near the factory.", "negative"),
    ("The roads have improved significantly.", "positive"),
    ("The drainage system is broken.", "negative"),
    ("The environment is clean and safe.", "positive"),
    ("The air is polluted and unpleasant.", "negative"),
    ("Public transport is better now.", "positive"),
    ("The garbage creates a bad smell.", "negative"),
    ("The new park is pleasant and clean.", "positive"),
    ("The traffic noise is terrible.", "negative"),
    ("The bus arrived fast and on time.", "positive"),
    ("The water supply is poor.", "negative"),
    ("The pollution levels have improved.", "positive"),
    ("The factory releases dirty smoke.", "negative"),
    ("The workers are helpful.", "positive"),
    ("The roads are unsafe at night.", "negative"),
    ("The air is fresh after cleaning.", "positive"),
    ("The drainage is slow and broken.", "negative"),
    ("The new system is excellent.", "positive"),
    ("There is heavy smoke every morning.", "negative"),
    ("The streets are clean and pleasant.", "positive"),
    ("The public service is rude.", "negative"),
    ("The environment has become better.", "positive"),
    ("The garbage disposal is poor.", "negative"),
    ("The transport service is fast.", "positive"),
    ("The air is dirty near the highway.", "negative"),
    ("The new cleaning team is helpful.", "positive"),
    ("The pollution is very bad.", "negative"),
    ("The roads are better and safer.", "positive"),
    ("The factory smoke is harmful.", "negative"),
    ("The surroundings are fresh and clean.", "positive"),
    ("The public toilets are dirty.", "negative"),
    ("The service has improved.", "positive"),
    ("The air quality is poor today.", "negative"),
    ("The buses are clean and fast.", "positive"),
    ("The garbage collection is slow.", "negative"),
    ("The neighbourhood is pleasant.", "positive"),
    ("The streets are polluted and unsafe.", "negative"),
    ("The new road is excellent.", "positive"),
    ("The smoke causes a bad smell.", "negative"),
    ("The staff are polite and helpful.", "positive"),
    ("The drainage is broken and dirty.", "negative"),
    ("The air is fresh and clean.", "positive"),
    ("The pollution problem is serious.", "negative")
]


def score(text):
    words = re.findall(r"\b[\w']+\b", text.lower())

    total = 0

    for i, word in enumerate(words):
        value = 0

        if word in POSITIVE:
            value = 1
        elif word in NEGATIVE:
            value = -1

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


def summarise(text, sentence_count=2):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())

    if len(sentences) <= sentence_count:
        return text

    word_frequency = {}

    for sentence in sentences:
        words = re.findall(r"\b[a-zA-Z]+\b", sentence.lower())

        for word in words:
            if word not in STOPWORDS and len(word) > 2:
                word_frequency[word] = (
                    word_frequency.get(word, 0) + 1
                )

    ranked = []

    for index, sentence in enumerate(sentences):
        words = re.findall(r"\b[a-zA-Z]+\b", sentence.lower())

        sentence_score = sum(
            word_frequency.get(word, 0)
            for word in words
        )

        ranked.append((sentence_score, index, sentence))

    selected = sorted(
        ranked,
        key=lambda item: (-item[0], item[1])
    )[:sentence_count]

    selected.sort(key=lambda item: item[1])

    return " ".join(item[2] for item in selected)


def analyse_complaints():
    print("\n--- SENTIMENT ANALYSIS ---")

    correct = 0
    results = []

    for complaint, actual_label in COMPLAINTS:
        predicted = label(complaint)

        if predicted == actual_label:
            correct += 1

        results.append([
            complaint, actual_label, predicted,
            "Yes" if predicted == actual_label else "No"
        ])

        print(
            f"Actual: {actual_label:8} "
            f"Predicted: {predicted:8} | {complaint}"
        )

    agreement = correct / len(COMPLAINTS) * 100

    print("\nTotal complaints:", len(COMPLAINTS))
    print("Correct predictions:", correct)
    print("Incorrect predictions:", len(COMPLAINTS) - correct)
    print(f"Agreement: {agreement:.2f}%")

    with open(
        OUTPUT / "sentiment_results.csv",
        "w",
        newline=""
    ) as file:
        writer = csv.writer(file)
        writer.writerow([
            "Complaint", "Manual Label",
            "Predicted Label", "Agreement"
        ])
        writer.writerows(results)

    return agreement



def test_summariser():
    print("\n--- EXTRACTIVE SUMMARISATION ---")

    text = " ".join(
        complaint for complaint, actual_label in COMPLAINTS
    )

    summary = summarise(text, 5)

    print("Total complaints:", len(COMPLAINTS))
    print("\nGenerated summary:")
    print(summary)

    with open(
        OUTPUT / "summary.txt",
        "w",
        encoding="utf-8"
    ) as file:
        file.write(summary)


def create_database():
    database = DATA / "air_quality.db"

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

    print("\nGenerating database records...")

    stations = [f"Station_{i}" for i in range(1, 13)]
    batch = []

    for station in stations:
        for day in range(365):
            day_text = f"2026-{day + 1:03d}"

            for hour in range(24):
                pm25 = 30 + (day % 30) + hour * 0.5

                batch.append((
                    station, day_text, hour, pm25
                ))

                if len(batch) >= 10000:
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

    cur.execute("SELECT COUNT(*) FROM readings")
    print("Total database records:", cur.fetchone()[0])

    return con


def measure_query(cur, repetitions=1000):
    query = """
        SELECT AVG(pm25)
        FROM readings
        WHERE station = ? AND day = ?
    """

    start = time.perf_counter()

    for _ in range(repetitions):
        cur.execute(
            query,
            ("Station_5", "2026-150")
        )
        cur.fetchone()

    return time.perf_counter() - start


def test_index():
    print("\n--- DATABASE INDEX PERFORMANCE ---")

    con = create_database()
    cur = con.cursor()

    print("\nMeasuring query without index...")

    before = measure_query(cur)

    print(f"Without index: {before:.6f} seconds")

    cur.execute("""
        CREATE INDEX idx_station_day
        ON readings(station, day)
    """)

    con.commit()

    print("\nMeasuring query with index...")

    after = measure_query(cur)

    print(f"With index: {after:.6f} seconds")

    if after > 0:
        improvement = ((before - after) / before) * 100
        print(f"Time reduction: {improvement:.2f}%")

    cur.execute("EXPLAIN QUERY PLAN SELECT AVG(pm25) FROM readings WHERE station = ? AND day = ?", ("Station_5", "2026-150"))

    print("\nQuery execution plan:")
    for row in cur.fetchall():
        print(row)

    con.close()


def main():
    print("FINAL ENGINEERING DECISION")
    print("=" * 50)

    agreement = analyse_complaints()

    test_summariser()

    test_index()

    print("\n--- FINAL STATUS ---")
    print("Sentiment agreement:", f"{agreement:.2f}%")
    print("Complaint summary generated.")
    print("Database index tested.")
    print("Results saved in outputs folder.")

    print("\nTASK 04 COMPLETED SUCCESSFULLY.")


if __name__ == "__main__":
    main()
