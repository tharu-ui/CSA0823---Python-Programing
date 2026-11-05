import time
import statistics


def build_plus(count):
    result = ""

    for i in range(count):
        item = f"Item{i}:Rs{i % 50}"
        result += item + ";"

    return result


def build_join(count):
    items = []

    for i in range(count):
        item = f"Item{i}:Rs{i % 50}"
        items.append(item)

    return ";".join(items) + ";"


def build_fstring(count):
    items = []

    for i in range(count):
        items.append(f"Item{i}:Rs{i % 50}")

    result = f"{';'.join(items)};"

    return result


def measure_time(function, count):
    times = []

    for run in range(3):
        start = time.perf_counter()
        result = function(count)
        end = time.perf_counter()

        times.append(end - start)

    return statistics.mean(times), result


sizes = [1000, 10000, 200000]

print("STRING BUILDING PERFORMANCE COMPARISON")
print("Each method is executed three times.")
print("Time shown is the average in seconds.")

for size in sizes:
    print("\n================================")
    print("Number of items:", size)

    plus_time, plus_result = measure_time(build_plus, size)
    join_time, join_result = measure_time(build_join, size)
    fstring_time, fstring_result = measure_time(build_fstring, size)

    print("Outputs are identical:",
          plus_result == join_result == fstring_result)

    print("Repeated + time:", round(plus_time, 6), "seconds")
    print("Join time:", round(join_time, 6), "seconds")
    print("F-string and join time:", round(fstring_time, 6), "seconds")
    