import time
from functools import lru_cache


original_calls = 0
redesigned_calls = 0


# Original program: recursion without memoisation

def original_ways(n):
    global original_calls
    original_calls += 1

    if n <= 1:
        return 1

    return original_ways(n - 1) + original_ways(n - 2)


# Redesigned program: recursion with memoisation

@lru_cache(maxsize=None)
def redesigned_ways(n):
    global redesigned_calls
    redesigned_calls += 1

    if n <= 1:
        return 1

    return redesigned_ways(n - 1) + redesigned_ways(n - 2)


# Performance comparison

sizes = [10, 20, 25, 30]

print("PROGRAM REDESIGN USING MEMOISATION")
print("Original vs Redesigned Program")

for n in sizes:

    original_calls = 0
    redesigned_calls = 0

    redesigned_ways.cache_clear()

    start = time.perf_counter()
    original_result = original_ways(n)
    original_time = time.perf_counter() - start

    start = time.perf_counter()
    redesigned_result = redesigned_ways(n)
    redesigned_time = time.perf_counter() - start

    print("\n===================================")
    print("Input n:", n)

    print("\nOriginal Program")
    print("Result:", original_result)
    print("Function calls:", original_calls)
    print("Execution time:", round(original_time, 6), "seconds")

    print("\nRedesigned Program")
    print("Result:", redesigned_result)
    print("Function calls:", redesigned_calls)
    print("Execution time:", round(redesigned_time, 6), "seconds")

    print("\nResults are identical:",
          original_result == redesigned_result)