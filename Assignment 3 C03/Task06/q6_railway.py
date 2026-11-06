
import random
import time

trains = {
    "12601": {
        "name": "Chennai Express",
        "stops": [
            ("Chennai", "08:00", "08:10"),
            ("Katpadi", "10:00", "10:05"),
            ("Bengaluru", "12:00", "12:10")
        ],
        "days": {"Monday", "Wednesday", "Friday"}
    },
    "12602": {
        "name": "Coimbatore Express",
        "stops": [
            ("Chennai", "09:00", "09:10"),
            ("Salem", "12:00", "12:05"),
            ("Coimbatore", "14:00", "14:10")
        ],
        "days": {"Tuesday", "Thursday", "Saturday"}
    },
    "12603": {
        "name": "Madurai Express",
        "stops": [
            ("Chennai", "06:00", "06:10"),
            ("Villupuram", "08:00", "08:05"),
            ("Madurai", "12:00", "12:10")
        ],
        "days": {"Monday", "Tuesday", "Friday"}
    },
    "12604": {
        "name": "Salem Express",
        "stops": [
            ("Bengaluru", "07:00", "07:10"),
            ("Salem", "10:00", "10:05"),
            ("Chennai", "13:00", "13:10")
        ],
        "days": {"Wednesday", "Saturday"}
    },
    "12605": {
        "name": "Southern Express",
        "stops": [
            ("Chennai", "05:00", "05:10"),
            ("Katpadi", "07:00", "07:05"),
            ("Madurai", "11:00", "11:10")
        ],
        "days": {"Sunday", "Monday", "Friday"}
    }
}


def search_without_index(station, day):
    result = []

    for number, details in trains.items():
        if day not in details["days"]:
            continue

        for stop in details["stops"]:
            if stop[0].lower() == station.lower():
                result.append((stop[2], number, details["name"], stop[1]))
                break

    return sorted(result)


def build_station_index(data):
    index = {}

    for number, details in data.items():
        for stop in details["stops"]:
            index.setdefault(stop[0].lower(), []).append(number)

    return index


station_index = build_station_index(trains)


def search_with_index(station, day):
    result = []

    for number in station_index.get(station.lower(), []):
        details = trains[number]

        if day not in details["days"]:
            continue

        for stop in details["stops"]:
            if stop[0].lower() == station.lower():
                result.append((stop[2], number, details["name"], stop[1]))
                break

    return sorted(result)


station = "Chennai"
day = "Monday"

print("TRAINS WITHOUT INDEX:")
for departure, number, name, arrival in search_without_index(station, day):
    print(number, name, "Arrival:", arrival, "Departure:", departure)

print("\nTRAINS WITH INDEX:")
for departure, number, name, arrival in search_with_index(station, day):
    print(number, name, "Arrival:", arrival, "Departure:", departure)

print("\nTHIRD STATION DEPARTURE:")
print(trains["12601"]["stops"][2][2])

print("\nUNKNOWN STATION:")
print(search_with_index("Unknown", "Monday"))

print("\nNON-RUNNING DAY:")
print(search_with_index("Chennai", "Tuesday"))

# Performance investigation
print("\nPERFORMANCE COMPARISON:")

for size in [100, 1000, 10000]:
    data = {}

    for i in range(size):
        number = str(10000 + i)
        stops = [
            ("Chennai", "08:00", "08:10"),
            ("Salem", "10:00", "10:05"),
            ("Madurai", "12:00", "12:10")
        ]

        data[number] = {
            "name": "Train " + number,
            "stops": stops,
            "days": {"Monday", "Wednesday"}
        }

    index = build_station_index(data)

    start = time.perf_counter()
    for number, details in data.items():
        for stop in details["stops"]:
            if stop[0] == "Chennai":
                break
    normal_time = time.perf_counter() - start

    start = time.perf_counter()
    for number in index.get("chennai", []):
        details = data[number]
    indexed_time = time.perf_counter() - start

    print("\nTrains:", size)
    print("Without index:", normal_time)
    print("With index:", indexed_time)
