from reader import read_attendance
from stats import percentage, absent_three_consecutive
from report import write_reports

if __name__ == "__main__":
    records = read_attendance("../sample_days")
    write_reports(records, percentage(records), absent_three_consecutive(records))
    print("Three-module reports created.")
