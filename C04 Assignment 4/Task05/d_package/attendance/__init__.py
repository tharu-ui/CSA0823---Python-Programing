"""Attendance processing package."""
from .reader import read_attendance
from .stats import percentage, absent_three_consecutive
from .report import write_reports
