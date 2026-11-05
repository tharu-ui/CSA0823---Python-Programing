import math

BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30

fat = float(input("Enter fat percentage: "))
snf = float(input("Enter SNF percentage: "))
litres = float(input("Enter litres: "))

fat_steps = round((fat - 3.5) / 0.1)
snf_steps = round((snf - 8.5) / 0.1)

rate = BASE_RATE + fat_steps * FAT_STEP_VALUE + snf_steps * SNF_STEP_VALUE
rate = round(rate, 2)

amount = round(litres * rate, 2)

print("Fat steps:", fat_steps)
print("SNF steps:", snf_steps)
print(f"Rate per litre: Rs. {rate:.2f}")
print(f"Amount: Rs. {amount:.2f}")

print((4.2 - 3.5) / 0.1)
print(0.1 + 0.2 == 0.3)
print(round(2.675, 2))

print("int(-2.7):", int(-2.7))
print("floor(-2.7):", math.floor(-2.7))
