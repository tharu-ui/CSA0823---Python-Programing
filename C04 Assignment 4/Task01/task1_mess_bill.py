from decimal import Decimal, InvalidOperation

def process_mess_file(filename):
    total = Decimal("0.00")
    report_rows = []
    rejected_lines = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue

                parts = [part.strip() for part in line.split(",")]
                if len(parts) != 3:
                    rejected_lines.append((line_number, line, "expected 3 fields"))
                    continue

                register_number, name, amount_text = parts
                try:
                    amount = Decimal(amount_text)
                except InvalidOperation:
                    rejected_lines.append((line_number, line, "invalid amount"))
                    continue

                if not amount.is_finite():
                    rejected_lines.append((line_number, line, "amount must be finite"))
                    continue

                total += amount
                report_rows.append(f"{name} {amount:.2f}")

    except FileNotFoundError:
        print(f"Error: file '{filename}' was not found.")
        return

    print("Mess Bill Report")
    for row in report_rows:
        print(row)
    print(f"Total: {total:.2f}")

    print("Rejected Lines:")
    if rejected_lines:
        for line_number, line, reason in rejected_lines:
            print(f"Line {line_number}: {line} ({reason})")
    else:
        print("None")

if __name__ == "__main__":
    from pathlib import Path
    process_mess_file(Path(__file__).parent / "mess_oct.txt")
