def write_reports(records, rates, consecutive, filename="three_modules_report.txt"):
    with open(filename, "w", encoding="utf-8") as file:
        for reg, rate in sorted(rates.items()):
            file.write(f"{reg}: {rate:.2f}%\n")
        file.write("Absent three consecutive days: " + ", ".join(consecutive) + "\n")
