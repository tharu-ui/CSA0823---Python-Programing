from pathlib import Path
from registration.reader import read_department_files
from registration.processor import clean_records
from registration.report import write_outputs

def main():
    base = Path(__file__).parent
    error_log = base / "output" / "error.log"
    error_log.parent.mkdir(parents=True, exist_ok=True)
    error_log.write_text("", encoding="utf-8")

    records = read_department_files(base / "department_files", error_log)
    clean = clean_records(records, error_log)
    write_outputs(clean, base / "output")
    print(f"Input records read: {len(records)}")
    print(f"Valid unique registrations: {len(clean)}")
    print(f"Output folder: {base / 'output'}")
    print(f"Error log: {error_log}")

if __name__ == "__main__":
    main()
