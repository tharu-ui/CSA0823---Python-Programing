farmer_id = input("Enter farmer ID: ")
litres = float(input("Enter litres: "))
fat = float(input("Enter fat percentage: "))
snf = float(input("Enter SNF percentage: "))
shift = input("Enter shift: ")

BASE_RATE = 30.00
FAT_STEP_VALUE = 0.40
SNF_STEP_VALUE = 0.30

if litres < 0:
    print("Invalid litres")
elif fat < 2.0 or fat > 7.0:
    print("Invalid fat percentage")
else:
    print("Farmer ID:", farmer_id)
    print("Litres:", litres)
    print("Fat:", fat)
    print("SNF:", snf)
    print("Shift:", shift)
    print("Base rate:", BASE_RATE)