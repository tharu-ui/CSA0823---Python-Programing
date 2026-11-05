BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30

def rate_per_litre(fat, snf):
    """Calculate the rate per litre."""
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)

    rate = BASE_RATE + fat_steps * FAT_STEP_VALUE
    rate += snf_steps * SNF_STEP_VALUE

    return round(rate, 2)

def payout(litres, fat, snf):
    """Calculate the payment for milk supplied."""
    rate = rate_per_litre(fat, snf)
    return round(litres * rate, 2)

def ten_day_total(payments):
    """Calculate the total payment for ten days."""
    total = 0.0

    for amount in payments:
        total += amount

    return round(total, 2)

farmer_id = input("Enter farmer ID: ")
litres = float(input("Enter litres: "))
fat = float(input("Enter fat percentage: "))
snf = float(input("Enter SNF percentage: "))

rate = rate_per_litre(fat, snf)
amount = payout(litres, fat, snf)
total = ten_day_total([amount])

print("Farmer ID:", farmer_id)
print(f"Rate per litre: Rs. {rate:.2f}")
print(f"Payment: Rs. {amount:.2f}")
print(f"Ten-day total so far: Rs. {total:.2f}")
