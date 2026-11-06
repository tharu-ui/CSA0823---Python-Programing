
import random
import time

random.seed(42)

readings = [random.randint(0, 50) for i in range(365)]

print("TOTAL NUMBER OF DAYS:", len(readings))

weekly_totals = []

for i in range(0, len(readings), 7):
    week = readings[i:i + 7]
    weekly_totals.append(sum(week))

print("\nWEEKLY RAINFALL TOTALS:")
print(weekly_totals)

maximum = max(readings)
minimum = min(readings)

max_days = [i + 1 for i, value in enumerate(readings) if value == maximum]
min_days = [i + 1 for i, value in enumerate(readings) if value == minimum]

print("\nMAXIMUM RAINFALL:", maximum, "mm")
print("DAY(S):", max_days)

print("\nMINIMUM RAINFALL:", minimum, "mm")
print("DAY(S):", min_days)

print("\nWETTEST WEEK:", weekly_totals.index(max(weekly_totals)) + 1)
print("DRIEST WEEK:", weekly_totals.index(min(weekly_totals)) + 1)

def naive_average(data):
    averages = []

    if len(data) < 7:
        return averages

    for i in range(len(data) - 6):
        total = sum(data[i:i + 7])
        averages.append(total / 7)

    return averages


def running_average(data):
    averages = []

    if len(data) < 7:
        return averages

    current_sum = sum(data[:7])
    averages.append(current_sum / 7)

    for i in range(7, len(data)):
        current_sum = current_sum - data[i - 7] + data[i]
        averages.append(current_sum / 7)

    return averages


naive_result = naive_average(readings)
running_result = running_average(readings)

print("\nNUMBER OF MOVING AVERAGES:", len(running_result))
print("FIRST FIVE MOVING AVERAGES:", running_result[:5])

print("BOTH METHODS GIVE SAME RESULT:",
      all(abs(a - b) < 1e-9 for a, b in zip(naive_result, running_result)))

dry_days = [i + 1 for i, value in enumerate(readings) if value == 0]

print("\nDRY DAYS:", dry_days)
print("NUMBER OF DRY DAYS:", len(dry_days))

print("\nEDGE CASE TESTS")
print("Empty list:", running_average([]))
print("Five readings:", running_average([2, 4, 6, 8, 10]))

print("\nPERFORMANCE COMPARISON")

for size in [365, 36500, 365000]:
    data = [random.randint(0, 50) for i in range(size)]

    start = time.perf_counter()
    naive_average(data)
    naive_time = time.perf_counter() - start

    start = time.perf_counter()
    running_average(data)
    running_time = time.perf_counter() - start

    print("\nReadings:", size)
    print("Naive time:", naive_time)
    print("Running-sum time:", running_time)
