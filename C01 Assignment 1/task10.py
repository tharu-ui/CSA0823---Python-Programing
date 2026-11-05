from decimal import Decimal
import time

sizes = [300, 6000, 150000]

for n in sizes:
    payments = ["33.40"] * n

    start = time.perf_counter()
    float_total = 0.0

    for amount in payments:
        float_total += float(amount)

    float_time = time.perf_counter() - start

    start = time.perf_counter()
    decimal_total = Decimal("0.00")

    for amount in payments:
        decimal_total += Decimal(amount)

    decimal_time = time.perf_counter() - start

    difference = abs(Decimal(str(float_total)) - decimal_total)

    print("Payments:", n)
    print("Float total:", float_total)
    print("Decimal total:", decimal_total)
    print("Difference:", difference)
    print(f"Float time: {float_time:.6f} seconds")
    print(f"Decimal time: {decimal_time:.6f} seconds")
    print()
