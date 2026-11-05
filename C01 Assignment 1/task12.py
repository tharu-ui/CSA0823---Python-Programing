from decimal import Decimal, ROUND_HALF_UP

def rate_per_litre(fat, snf, month):
    """Calculate the rate using the selected season."""
    if month.lower() in ["april", "may", "june"]:
        base_rate = Decimal("32.00")
        fat_step_value = Decimal("0.45")
    else:
        base_rate = Decimal("30.00")
        fat_step_value = Decimal("0.40")

    snf_step_value = Decimal("0.30")

    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)

    rate = base_rate + Decimal(fat_steps) * fat_step_value
    rate += Decimal(snf_steps) * snf_step_value

    return rate.quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

def payout(litres, fat, snf, month):
    """Calculate the payment for one entry."""
    rate = rate_per_litre(fat, snf, month)
    return (litres * rate).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

def bonus(total_litres):
    """Calculate the ten-day bonus."""
    if total_litres > 500:
        return (total_litres * Decimal("0.50")).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )

    return Decimal("0.00")

month = input("Enter month: ").strip()
count = int(input("Enter number of entries: "))

total_litres = Decimal("0.00")
total_payment = Decimal("0.00")

for i in range(count):
    print("Entry", i + 1)

    litres = Decimal(input("Enter litres: "))
    fat = float(input("Enter fat percentage: "))
    snf = float(input("Enter SNF percentage: "))

    if litres < 0 or not 2.0 <= fat <= 7.0:
        print("Invalid entry")
        continue

    rate = rate_per_litre(fat, snf, month)
    amount = payout(litres, fat, snf, month)

    total_litres += litres
    total_payment += amount

    print(f"Rate per litre: Rs. {rate:.2f}")
    print(f"Payment: Rs. {amount:.2f}")

extra = bonus(total_litres)
total_payment = (total_payment + extra).quantize(
    Decimal("0.01"), rounding=ROUND_HALF_UP
)

print(f"Total litres: {total_litres}")
print(f"Bonus: Rs. {extra:.2f}")
print(f"Ten-day total: Rs. {total_payment:.2f}")
