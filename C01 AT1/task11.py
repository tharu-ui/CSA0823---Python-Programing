import json
from decimal import Decimal

with open("task11_ratecard.json", "r") as file:
    rates = json.load(file)

BASE_RATE = Decimal(rates["base_rate"])
FAT_STEP_VALUE = Decimal(rates["fat_step_value"])
SNF_STEP_VALUE = Decimal(rates["snf_step_value"])

def rate_per_litre(fat, snf):
    """Calculate the rate per litre."""
    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)

    rate = BASE_RATE + Decimal(fat_steps) * FAT_STEP_VALUE
    rate += Decimal(snf_steps) * SNF_STEP_VALUE

    return rate.quantize(Decimal("0.01"))

def payout(litres, fat, snf):
    """Calculate the payment."""
    return (litres * rate_per_litre(fat, snf)).quantize(
        Decimal("0.01")
    )

litres = Decimal(input("Enter litres: "))
fat = float(input("Enter fat percentage: "))
snf = float(input("Enter SNF percentage: "))

if litres < 0 or not 2.0 <= fat <= 7.0:
    print("Invalid entry")
else:
    rate = rate_per_litre(fat, snf)
    amount = payout(litres, fat, snf)

    print(f"Rate per litre: Rs. {rate:.2f}")
    print(f"Payment: Rs. {amount:.2f}")
