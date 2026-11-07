from pathlib import Path

def read_attendance(folder):
    records = {}
    for path in sorted(Path(folder).glob("*.txt")):
        with path.open(encoding="utf-8") as file:
            for line in file:
                p = [x.strip() for x in line.strip().split(",")]
                if len(p) == 3 and p[2] in ("P", "A"):
                    records.setdefault(p[0], []).append((p[1], p[2]))
    return records

def percentage(records):
    return {reg: sum(s == "P" for _, s in rows) / len(rows) * 100
            for reg, rows in records.items() if rows}

def absent_three_consecutive(records):
    return [reg for reg, rows in records.items()
            if any([s for _, s in sorted(rows)][i:i+3] == ["A","A","A"]
                   for i in range(len(rows)-2))]
