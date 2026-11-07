from attendance import read_attendance, percentage, absent_three_consecutive, write_reports

if __name__ == "__main__":
    records = read_attendance("../sample_days")
    write_reports(records, percentage(records), absent_three_consecutive(records))
    print("Package-based reports created.")
