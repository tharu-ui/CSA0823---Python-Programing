from attendance_utils import read_attendance, percentage, absent_three_consecutive

if __name__ == "__main__":
    records = read_attendance("../sample_days")
    with open("module_report.txt", "w", encoding="utf-8") as file:
        for reg, rate in sorted(percentage(records).items()):
            file.write(f"{reg}: {rate:.2f}%\n")
        file.write("Absent three consecutive days: " +
                   ", ".join(absent_three_consecutive(records)) + "\n")
    print("Module-based reports created.")
