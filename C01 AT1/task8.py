BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30

count = int(input("Enter number of entries: "))
total = 0.0

for i in range(count):
    print("Entry", i + 1)

    litres = float(input("Enter litres: "))
    fat = float(input("Enter fat percentage: "))
    snf = float(input("Enter SNF percentage: "))

    if litres < 0 or fat < 2.0 or fat > 7.0:
        print("Invalid entry")
        continue

    fat_steps = round((fat - 3.5) / 0.1)
    snf_steps = round((snf - 8.5) / 0.1)

    rate = BASE_RATE + fat_steps * FAT_STEP_VALUE
    rate += snf_steps * SNF_STEP_VALUE

    amount = round(litres * rate, 2)
    total = round(total + amount, 2)

    print(f"Payment: Rs. {amount:.2f}")

print(f"Total payment: Rs. {total:.2f}")
