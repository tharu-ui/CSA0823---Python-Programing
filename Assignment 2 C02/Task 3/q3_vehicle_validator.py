import re


def normalise(registration):
    registration = registration.strip()
    registration = registration.replace(" ", "")
    registration = registration.replace("-", "")
    registration = registration.upper()

    return registration


def is_valid(registration):
    reg = normalise(registration)

    if len(reg) != 9 and len(reg) != 10:
        return False

    state = reg[0:2]
    district = reg[2:4]
    series = reg[4:-4]
    number = reg[-4:]

    if not state.isalpha():
        return False

    if not district.isdigit():
        return False

    if not series.isalpha():
        return False

    if len(series) < 1 or len(series) > 2:
        return False

    if not number.isdigit():
        return False

    return True


def format_receipt(registration):
    reg = normalise(registration)

    if not is_valid(reg):
        return "Invalid registration number"

    state = reg[0:2]
    district = reg[2:4]
    series = reg[4:-4]
    number = reg[-4:]

    return state + " " + district + " " + series + " " + number


def regex_validation(registration):
    reg = normalise(registration)

    pattern = r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}"

    return re.fullmatch(pattern, reg) is not None


test_cases = [
    "tn 09 ab 1234",
    "KA-01-M-0007",
    "Tn09Ab1234",
    "TN9AB1234",
    "TN 22 1234 AB",
    "TN-09-ABC-1234"
]


print("VEHICLE REGISTRATION VALIDATOR")

for registration in test_cases:
    print("\nInput:", registration)

    if is_valid(registration):
        print("Status: Valid")
        print("Receipt:", format_receipt(registration))
    else:
        print("Status: Invalid")

    print("Regex Validation:", regex_validation(registration))