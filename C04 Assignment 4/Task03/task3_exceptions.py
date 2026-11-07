import os
import tempfile

class InvalidRecord(Exception):
    """Raised when an attendance line is not in the expected format."""

def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    register_number, date, status = (part.strip() for part in parts)
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")
    if not register_number or not date:
        raise InvalidRecord("register number and date cannot be empty")
    return register_number, date, status

def summarise(path):
    present, absent, errors = 0, 0, []
    try:
        with open(path, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                try:
                    _, _, status = parse_line(line)
                except InvalidRecord as error:
                    errors.append((line_number, str(error)))
                    continue
                if status == "P":
                    present += 1
                else:
                    absent += 1
    except FileNotFoundError as error:
        raise FileNotFoundError(f"attendance file not found: {path}") from error
    except PermissionError as error:
        raise PermissionError(f"permission denied: {path}") from error
    except UnicodeDecodeError as error:
        raise ValueError(f"file is not valid UTF-8: {path}") from error
    else:
        print("File processed successfully.")
    finally:
        print("Attendance processing attempt completed.")
    return present, absent, errors

if __name__ == "__main__":
    data = ("192311001,2026-10-08,P\n192311002,2026-10-08,A\n"
            "192311003,2026-10-08\n192311004,2026-10-08,L\n")
    with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False,
                                     encoding="utf-8") as tmp:
        tmp.write(data)
        temp_name = tmp.name

    print(summarise(temp_name))
    os.remove(temp_name)

    try:
        summarise("file_that_does_not_exist.csv")
    except FileNotFoundError as error:
        print("Handled:", error)
