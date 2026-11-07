from pathlib import Path

def read_attendance(folder):
    records = {}
    for path in sorted(Path(folder).glob("*.txt")):
        with path.open(encoding="utf-8") as file:
            for line in file:
                parts = [x.strip() for x in line.strip().split(",")]
                if len(parts) == 3 and parts[2] in ("P", "A"):
                    reg, date, status = parts
                    records.setdefault(reg, []).append((date, status))
    return records

def percentage(records):
    result = {}
    for reg, rows in records.items():
        present = sum(status == "P" for _, status in rows)
        result[reg] = present / len(rows) * 100 if rows else 0
    return result

def absent_three_consecutive(records):
    result = []
    for reg, rows in records.items():
        statuses = [status for _, status in sorted(rows)]
        if any(statuses[i:i+3] == ["A", "A", "A"]
               for i in range(len(statuses)-2)):
            result.append(reg)
    return result

def write_reports(records):
    rates = percentage(records)
    with open("single_script_report.txt", "w", encoding="utf-8") as file:
        for reg, rate in sorted(rates.items()):
            file.write(f"{reg}: {rate:.2f}%\n")
        file.write("Absent three consecutive days: " +
                   ", ".join(absent_three_consecutive(records)) + "\n")

if __name__ == "__main__":
    data = read_attendance("sample_days")
    write_reports(data)
    print("Single-script reports created.")
