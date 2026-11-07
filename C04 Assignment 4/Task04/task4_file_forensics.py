from pathlib import Path

def save_returns(books, log_name="returns.log"):
    with open(log_name, "a", encoding="utf-8") as log:
        for book in books:
            if book:
                log.write(book + "\n")

def write_error(message, error_name="error.log"):
    with open(error_name, "a", encoding="utf-8") as error_file:
        error_file.write(message + "\n")

def process(day_file, log_name="returns.log", error_name="error.log"):
    try:
        with open(day_file, "r", encoding="utf-8") as file:
            books = [line.strip() for line in file if line.strip()]
        save_returns(books, log_name)
    except (FileNotFoundError, PermissionError, UnicodeDecodeError, OSError) as error:
        message = f"{day_file}: {type(error).__name__}: {error}"
        write_error(message, error_name)
        print("Error recorded:", message)

if __name__ == "__main__":
    base = Path(__file__).parent
    log = base / "returns.log"
    errors = base / "error.log"
    # Start this demonstration with clean log files.
    log.write_text("", encoding="utf-8")
    errors.write_text("", encoding="utf-8")

    for day in ("day1.txt", "day2.txt", "day3.txt", "missing_day.txt"):
        process(str(base / day), str(log), str(errors))

    print("Returns log:")
    print(log.read_text(encoding="utf-8"))
    print("Error log:")
    print(errors.read_text(encoding="utf-8"))
