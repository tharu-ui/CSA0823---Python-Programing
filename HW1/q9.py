def analyze(numbers):
    minimum = min(numbers)
    maximum = max(numbers)
    average = sum(numbers) / len(numbers)

    return minimum, maximum, average


numbers = list(map(int, input("Enter numbers: ").split()))

minimum, maximum, average = analyze(numbers)

print("Minimum:", minimum)
print("Maximum:", maximum)
print("Average:", average)

result = analyze(numbers)

print("Returned values:", result)
print("Return type:", type(result).__name__)
