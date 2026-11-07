from pathlib import Path
from collections import defaultdict
import csv

def process_month(input_folder, percentage_file, below_file, error_file):
    # Each register number maps to [present_count, absent_count].
    counts = defaultdict(lambda: [0, 0])
    errors = []

    daily_files = sorted(Path(input_folder).glob("*.txt"))

    for file_path in daily_files:
        try:
            with file_path.open("r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    parts = [part.strip() for part in line.strip().split(",")]
                    if len(parts) != 3:
                        errors.append((file_path.name, line_number, line.strip(),
                                       "expected 3 fields"))
                        continue

                    register_number, date, status = parts
                    if not register_number or not date or status not in ("P", "A"):
                        errors.append((file_path.name, line_number, line.strip(),
                                       "invalid register number, date or status"))
                        continue

                    if status == "P":
                        counts[register_number][0] += 1
                    else:
                        counts[register_number][1] += 1

        except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as error:
            errors.append((file_path.name, 0, "", str(error)))

    with open(percentage_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Register Number", "Present", "Absent", "Percentage"])
        for register_number in sorted(counts):
            present, absent = counts[register_number]
            total = present + absent
            percentage = (present / total * 100) if total else 0
            writer.writerow([register_number, present, absent, f"{percentage:.2f}"])

    with open(below_file, "w", encoding="utf-8") as file:
        file.write("Students below 75% attendance\n")
        for register_number in sorted(counts):
            present, absent = counts[register_number]
            total = present + absent
            percentage = (present / total * 100) if total else 0
            if percentage < 75:
                file.write(f"{register_number}: {percentage:.2f}%\n")

    with open(error_file, "w", encoding="utf-8") as file:
        file.write("File,Line Number,Rejected Data,Reason\n")
        for filename, line_number, data, reason in errors:
            file.write(f"{filename},{line_number},{data},{reason}\n")

    print(f"Daily files processed: {len(daily_files)}")
    print(f"Students processed: {len(counts)}")
    print(f"Damaged records: {len(errors)}")
    print(f"Created: {percentage_file}, {below_file}, {error_file}")

if __name__ == "__main__":
    base = Path(__file__).parent
    process_month(base / "daily_files", base / "attendance_percentage.csv",
                  base / "below_75.txt", base / "damaged_lines.csv")
