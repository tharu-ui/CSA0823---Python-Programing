import task7 as mr

farmer_id = input("Enter farmer ID: ")
litres = float(input("Enter litres: "))
fat = float(input("Enter fat percentage: "))
snf = float(input("Enter SNF percentage: "))

rate = mr.rate_per_litre(fat, snf)
amount = mr.payout(litres, fat, snf)

print("Farmer ID:", farmer_id)
print(f"Rate per litre: Rs. {rate:.2f}")
print(f"Payment: Rs. {amount:.2f}")
