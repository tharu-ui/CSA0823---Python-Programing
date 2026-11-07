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
