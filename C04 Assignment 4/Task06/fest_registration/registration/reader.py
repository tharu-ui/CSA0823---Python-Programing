from pathlib import Path

def read_department_files(folder, error_log):
    records = []
    for path in sorted(Path(folder).glob("*.txt")):
        try:
            with path.open("r", encoding="utf-8") as file:
                for line_number, line in enumerate(file, start=1):
                    if not line.strip():
                        continue
                    parts = [part.strip() for part in line.rstrip("\n").split(",")]
                    if len(parts) != 5:
                        log_error(error_log, path.name, line_number,
                                  "damaged record: expected 5 comma-separated fields")
                        continue
                    reg, name, department, email, events_text = parts
                    records.append({
                        "register_number": reg,
                        "name": name,
                        "department": department,
                        "email": email,
                        "events": [event.strip() for event in events_text.split(";")
                                   if event.strip()]
                    })
        except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as error:
            log_error(error_log, path.name, 0,
                      f"{type(error).__name__}: {error}")
    return records

def log_error(error_log, filename, line_number, message):
    with open(error_log, "a", encoding="utf-8") as file:
        file.write(f"{filename}, line {line_number}: {message}\n")
