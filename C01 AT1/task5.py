try:
    farmer_id = input("Enter farmer ID: ")
    litres = float(input("Enter litres: "))
    fat = float(input("Enter fat percentage: "))
    snf = float(input("Enter SNF percentage: "))

    if litres < 0:
        print("Litres cannot be negative.")
    elif not 2.0 <= fat <= 7.0:
        print("Fat must be between 2.0 and 7.0.")
    else:
        print("\nPayment Entry")
        print(f"{'Farmer ID':<15}{farmer_id}")
        print(f"{'Litres':<15}{litres:8.2f}")
        print(f"{'Fat':<15}{fat:8.2f}")
        print(f"{'SNF':<15}{snf:8.2f}")

except ValueError:
    print("Invalid input. Enter numbers correctly.")
