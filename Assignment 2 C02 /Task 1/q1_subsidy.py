def separate_if(units, ration_card, senior):
    print("\nUsing separate if statements:")

    if units <= 100:
        print("FULL SUBSIDY")

    if units <= 200 and ration_card:
        print("PARTIAL SUBSIDY")

    if units > 200 and senior:
        print("SPECIAL SUBSIDY")

    if units > 200 and not senior:
        print("NO SUBSIDY")


def if_elif_else(units, ration_card, senior):
    print("\nUsing if-elif-else:")

    if units <= 100:
        return "FULL SUBSIDY"
    elif 101 <= units <= 200 and ration_card:
        return "PARTIAL SUBSIDY"
    elif units > 200 and senior:
        return "SPECIAL SUBSIDY"
    else:
        return "NO SUBSIDY"


def match_case(units, ration_card, senior):
    match True:
        case _ if units <= 100:
            return "FULL SUBSIDY"
        case _ if 101 <= units <= 200 and ration_card:
            return "PARTIAL SUBSIDY"
        case _ if units > 200 and senior:
            return "SPECIAL SUBSIDY"
        case _:
            return "NO SUBSIDY"


def lookup_decision(units, ration_card, senior):
    if units <= 100:
        return "FULL SUBSIDY"

    if units > 200:
        if senior:
            return "SPECIAL SUBSIDY"
        return "NO SUBSIDY"

    slabs = [
        (200, "PARTIAL SUBSIDY")
    ]

    for upper_limit, decision in slabs:
        if units <= upper_limit and ration_card:
            return decision

    return "NO SUBSIDY"


test_cases = [
    ("H1", 100, True, False),
    ("H2", 101, True, False),
    ("H3", 101, False, False),
    ("H4", 150, True, False),
    ("H5", 200, True, False),
    ("H6", 200, False, False),
    ("H7", 201, False, True),
    ("H8", 250, True, False)
]


print("ELECTRICITY SUBSIDY ELIGIBILITY")

for name, units, ration_card, senior in test_cases:
    print("\n-----------------------------")
    print("Household:", name)
    print("Units:", units)
    print("Ration Card:", ration_card)
    print("Senior Citizen:", senior)

    separate_if(units, ration_card, senior)

    print("If-elif-else:", if_elif_else(units, ration_card, senior))
    print("Match-case:", match_case(units, ration_card, senior))
    print("Lookup:", lookup_decision(units, ration_card, senior))
