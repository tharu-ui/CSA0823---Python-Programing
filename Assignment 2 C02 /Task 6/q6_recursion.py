import sys
from functools import lru_cache


calls = 0


# Recursive solution without memoisation

def ways_naive(n):
    global calls
    calls += 1

    if n <= 1:
        return 1

    return ways_naive(n - 1) + ways_naive(n - 2)


# Recursive solution with memoisation

calls_memo = 0


@lru_cache(maxsize=None)
def ways_memo(n):
    global calls_memo
    calls_memo += 1

    if n <= 1:
        return 1

    return ways_memo(n - 1) + ways_memo(n - 2)


# Iterative solution

def ways_loop(n):
    if n <= 1:
        return 1

    previous = 1
    current = 1

    for i in range(2, n + 1):
        previous, current = current, previous + current

    return current


print("STAIRCASE PROBLEM")

print("\nResults for n = 1 to 6")

for n in range(1, 7):
    print("n =", n, "Ways =", ways_loop(n))


print("\nFUNCTION CALL COMPARISON")

for n in [10, 20, 25, 30]:
    calls = 0
    naive_result = ways_naive(n)
    naive_calls = calls

    calls_memo = 0
    ways_memo.cache_clear()
    memo_result = ways_memo(n)
    memo_calls = calls_memo

    loop_result = ways_loop(n)

    print("\nn =", n)
    print("Naive result:", naive_result)
    print("Memoised result:", memo_result)
    print("Iterative result:", loop_result)
    print("Naive function calls:", naive_calls)
    print("Memoised function calls:", memo_calls)
    print("All results match:", naive_result == memo_result == loop_result)


print("\nLARGE INPUT USING ITERATION")

n = 1000

print("Number of stairs:", n)
print("Number of ways:", ways_loop(n))

print("\nPython recursion limit:", sys.getrecursionlimit())