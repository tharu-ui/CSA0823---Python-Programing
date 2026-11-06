
import random
import time

ai_elective = {
    "192311001", "192311004", "192311007", "192311009"
}

iot_elective = {
    "192311002", "192311004", "192311009", "192311010"
}

all_students = {
    f"1923110{i:02d}" for i in range(1, 11)
}

clash = ai_elective & iot_elective
exactly_one = ai_elective ^ iot_elective
neither = all_students - (ai_elective | iot_elective)

print("clash      :", sorted(clash))
print("exactly one:", sorted(exactly_one))
print("neither    :", sorted(neither))

# Set methods
print("\nUSING SET METHODS:")
print("Intersection:", sorted(ai_elective.intersection(iot_elective)))
print("Union:", sorted(ai_elective.union(iot_elective)))
print("Difference:", sorted(ai_elective.difference(iot_elective)))
print("Symmetric difference:", sorted(ai_elective.symmetric_difference(iot_elective)))

# Edge cases
print("\nEDGE CASES:")
print("Empty intersection:", set() & ai_elective)
print("Identical sets:", ai_elective & ai_elective)

# Membership performance
print("\nMEMBERSHIP PERFORMANCE:")

for size in [10000, 100000, 1000000]:
    numbers = list(range(size))
    number_set = set(numbers)
    target = size - 1

    start = time.perf_counter()
    target in numbers
    list_time = time.perf_counter() - start

    start = time.perf_counter()
    target in number_set
    set_time = time.perf_counter() - start

    print("\nSize:", size)
    print("List membership:", list_time)
    print("Set membership:", set_time)

# Nested-loop comparison on a smaller dataset
a = list(range(1000))
b = list(range(500, 1500))

start = time.perf_counter()
common = []

for x in a:
    for y in b:
        if x == y:
            common.append(x)

nested_time = time.perf_counter() - start

start = time.perf_counter()
common_set = set(a) & set(b)
set_time = time.perf_counter() - start

print("\nCOMPARISON:")
print("Nested-loop time:", nested_time)
print("Set intersection time:", set_time)
print("Same result:", set(common) == common_set)
