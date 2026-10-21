from decimal import Decimal, ROUND_HALF_UP

BASE_RATE = Decimal("30.00")
FAT_STEP_VALUE = Decimal("0.40")
SNF_STEP_VALUE = Decimal("0.30")

def rate_per_litre(fat, snf):
    """Calculate the milk rate."""
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)

    rate = BASE_RATE
    rate += Decimal(fat_steps) * FAT_STEP_VALUE
    rate += Decimal(snf_steps) * SNF_STEP_VALUE

    return rate.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def payout(litres, fat, snf):
    """Calculate the payment."""
    return (litres * rate_per_litre(fat, snf)).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

def valid_entry(litres, fat, snf):
    """Check the entry values."""
    return litres >= 0 and 2.0 <= fat <= 7.0

# Five entries tested by the program
tests = [
    (10, 3.5, 8.5, "300.00"),
    (8.5, 4.2, 8.7, "283.90"),
    (12, 3.1, 8.3, "333.60"),
    (5, 2.0, 8.5, "270.00"),
    (5, 7.0, 8.5, "375.00")
]

total = Decimal("0.00")

for litres, fat, snf, expected in tests:
    amount = payout(Decimal(str(litres)), fat, snf)
    assert amount == Decimal(expected)
    total += amount
    print(f"Expected: Rs. {expected}, Actual: Rs. {amount:.2f}, PASS")

print(f"Five-entry total: Rs. {total:.2f}")

# Invalid-entry checks
assert not valid_entry(-1, 3.5, 8.5)
assert not valid_entry(10, 1.5, 8.5)
assert not valid_entry(10, 7.5, 8.5)

print("Invalid-entry tests: PASS")

# Interactive input
try:
    litres = Decimal(input("Enter litres: "))
    fat = float(input("Enter fat percentage: "))
    snf = float(input("Enter SNF percentage: "))

    if not valid_entry(litres, fat, snf):
        print("Invalid entry")
    else:
        print(f"Payment: Rs. {payout(litres, fat, snf):.2f}")

except Exception as error:
    if isinstance(error, (ValueError, ArithmeticError)):
        print("Invalid input")
    else:
        raise
