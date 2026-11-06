
import copy
import sys
import time

# Tuples as dictionary keys
places = {
    (13.0827, 80.2707): "Chennai",
    (12.9716, 77.5946): "Bengaluru"
}

print("COORDINATE DICTIONARY:")
print(places)
print("CHENNAI:", places[(13.0827, 80.2707)])

# Tuple unpacking
records = [
    ("Tharu", "Chennai"),
    ("Priya", "Madurai"),
    ("Kavi", "Salem")
]

print("\nTUPLE UNPACKING:")
for name, city in records:
    print(name, "-", city)

# Aliasing problem
bad = [[0] * 4] * 3
bad[0][1] = 7

print("\nBAD GRID:")
print(bad)

# Correct independent grid
good = [[0 for j in range(4)] for i in range(3)]
good[0][1] = 7

print("\nGOOD GRID:")
print(good)

print("\nIDENTITY TEST:")
print(bad[0] is bad[1], good[0] is good[1])

# Shallow and deep copy
original = [[1, 2], [3, 4]]

shallow = copy.copy(original)
deep = copy.deepcopy(original)

shallow[0][0] = 99
deep[1][1] = 88

print("\nORIGINAL:", original)
print("SHALLOW COPY:", shallow)
print("DEEP COPY:", deep)

# Slicing copy
numbers = [10, 20, 30]
new_numbers = numbers[:]
new_numbers[0] = 100

print("\nORIGINAL LIST:", numbers)
print("COPIED LIST:", new_numbers)

# Mutable list inside tuple
data = ("Chennai", ["T. Nagar", "Anna Nagar"])
data[1].append("Velachery")

print("\nTUPLE WITH MUTABLE LIST:")
print(data)

# List as dictionary key
try:
    sample = {[1, 2]: "value"}
except TypeError as error:
    print("\nLIST KEY ERROR:", error)

# Memory comparison
values_list = list(range(1000000))
values_tuple = tuple(range(1000000))

print("\nMEMORY COMPARISON:")
print("List memory:", sys.getsizeof(values_list), "bytes")
print("Tuple memory:", sys.getsizeof(values_tuple), "bytes")

# Creation time comparison
start = time.perf_counter()
a = list(range(1000000))
list_time = time.perf_counter() - start

start = time.perf_counter()
b = tuple(range(1000000))
tuple_time = time.perf_counter() - start

print("\nCREATION TIME:")
print("List:", list_time)
print("Tuple:", tuple_time)

# Indexing time comparison
start = time.perf_counter()
for i in range(100000):
    x = values_list[i]
list_index_time = time.perf_counter() - start

start = time.perf_counter()
for i in range(100000):
    x = values_tuple[i]
tuple_index_time = time.perf_counter() - start

print("\nINDEXING TIME:")
print("List:", list_index_time)
print("Tuple:", tuple_index_time)

# Complete the code expected output
bad = [[0] * 4] * 3
bad[0][1] = 7

good = [[0 for j in range(4)] for i in range(3)]
good[0][1] = 7

print("\nCOMPLETE THE CODE:")
print("bad :", bad)
print("good:", good)
print(bad[0] is bad[1], good[0] is good[1])
print(data[1][0])
