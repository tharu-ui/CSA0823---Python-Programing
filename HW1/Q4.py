def convert(temp, unit):
    if unit == "C":
        return (temp * 9 / 5) + 32
    elif unit == "F":
        return (temp - 32) * 5 / 9
    else:
        return "Invalid unit"


temp = float(input("Enter temperature: "))
unit = input("Enter unit (C/F): ").upper()

result = convert(temp, unit)

print("Temperature:", result)
