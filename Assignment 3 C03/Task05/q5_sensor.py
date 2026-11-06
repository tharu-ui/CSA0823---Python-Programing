
import random
import time
import sys

readings = [-60, -20, 0, 3, 5, 9, 12, 55, 7, 2, 8, 60]

# Clean valid readings
cleaned = [x for x in readings if -50 <= x <= 50]

# Celsius to Fahrenheit
fahrenheit = [(x * 9 / 5) + 32 for x in cleaned]

# Alarm readings outside 2 to 8 degrees
alarms = [x for x in cleaned if x < 2 or x > 8]

print("ORIGINAL READINGS:", readings)
print("CLEANED READINGS:", cleaned)
print("FAHRENHEIT:", fahrenheit)
print("ALARM READINGS:", alarms)

# Display alarm positions
print("\nALARM POSITIONS:")
for index, value in enumerate(cleaned):
    if value < 2 or value > 8:
        print("Position:", index, "Temperature:", value)

# map and filter
filtered = list(filter(lambda x: -50 <= x <= 50, readings))
converted = list(map(lambda x: (x * 9 / 5) + 32, filtered))

print("\nUSING MAP AND FILTER:")
print(filtered)
print(converted)

print("\nRESULTS IDENTICAL:",
      cleaned == filtered and fahrenheit == converted)

# Performance comparison
print("\nPERFORMANCE COMPARISON:")

for size in [10000, 100000, 1000000]:
    data = [random.randint(-60, 60) for i in range(size)]

    start = time.perf_counter()
    result1 = [x for x in data if -50 <= x <= 50]
    comprehension_time = time.perf_counter() - start

    start = time.perf_counter()
    result2 = list(filter(lambda x: -50 <= x <= 50, data))
    filter_time = time.perf_counter() - start

    print("\nSize:", size)
    print("List comprehension:", comprehension_time)
    print("Filter:", filter_time)
    print("Same result:", result1 == result2)

# Memory comparison
data = list(range(100000))
generator = (x for x in range(100000))

print("\nMEMORY COMPARISON:")
print("List size:", sys.getsizeof(data), "bytes")
print("Generator size:", sys.getsizeof(generator), "bytes")

# Edge cases
print("\nEDGE CASES:")
print("All valid:", [x for x in [2, 3, 4, 5] if -50 <= x <= 50])
print("All invalid:", [x for x in [60, 70, 80] if -50 <= x <= 50])
