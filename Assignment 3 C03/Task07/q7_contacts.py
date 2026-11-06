
import random
import time


def normalize_phone(phone):
    if not phone:
        return ""

    return "".join(character for character in phone if character.isdigit())


def normalize_name(name):
    if not name:
        return ""

    return " ".join(name.lower().split())


def merge_contacts(contacts):
    merged = {}
    missing_phone = []

    for contact in contacts:
        name = contact.get("name", "").strip()
        phone = normalize_phone(contact.get("phone", ""))
        email = contact.get("email", "").strip().lower()

        if not phone:
            missing_phone.append({
                "name": name,
                "phones": set(),
                "emails": {email} if email else set()
            })
            continue

        if phone not in merged:
            merged[phone] = {
                "name": name,
                "normalized_name": normalize_name(name),
                "phones": set(),
                "emails": set()
            }

        if phone:
            merged[phone]["phones"].add(phone)

        if email:
            merged[phone]["emails"].add(email)

        if not merged[phone]["name"] and name:
            merged[phone]["name"] = name

    result = []

    for details in merged.values():
        result.append({
            "name": details["name"],
            "phones": sorted(details["phones"]),
            "emails": sorted(details["emails"])
        })

    for details in missing_phone:
        result.append({
            "name": details["name"],
            "phones": sorted(details["phones"]),
            "emails": sorted(details["emails"])
        })

    return result


contacts = [
    {
        "name": "Tharu Priya",
        "phone": "+91 98765-43210",
        "email": "tharu@example.com"
    },
    {
        "name": "Tharu  Priya",
        "phone": "9876543210",
        "email": "tharu.work@example.com"
    },
    {
        "name": "Kavi",
        "phone": "91234-56789",
        "email": "kavi@example.com"
    },
    {
        "name": "Priya",
        "phone": "",
        "email": "priya@example.com"
    },
    {
        "name": "Kavi",
        "phone": "9123456789",
        "email": "kavi@example.com"
    }
]

print("MERGED CONTACTS:")

result = merge_contacts(contacts)

for contact in result:
    print(contact)


# Small pairwise comparison implementation
def pairwise_duplicate_count(records):
    count = 0

    for i in range(len(records)):
        for j in range(i + 1, len(records)):
            phone1 = normalize_phone(records[i].get("phone", ""))
            phone2 = normalize_phone(records[j].get("phone", ""))

            if phone1 and phone1 == phone2:
                count += 1

    return count


print("\nPAIRWISE DUPLICATE PAIRS:")
print(pairwise_duplicate_count(contacts))


# Performance comparison
print("\nPERFORMANCE COMPARISON:")

for size in [1000, 100000]:
    data = []

    for i in range(size):
        phone = str(9000000000 + (i // 2))

        data.append({
            "name": "Person " + str(i),
            "phone": phone,
            "email": "person" + str(i) + "@example.com"
        })

    start = time.perf_counter()
    merged_result = merge_contacts(data)
    dictionary_time = time.perf_counter() - start

    print("\nContacts:", size)
    print("Dictionary merging time:", dictionary_time)
    print("Merged contact count:", len(merged_result))

# Pairwise comparison on smaller dataset
small_data = data[:1000]

start = time.perf_counter()
pairs = pairwise_duplicate_count(small_data)
pairwise_time = time.perf_counter() - start

print("\nPAIRWISE TEST WITH 1000 CONTACTS:")
print("Duplicate pairs:", pairs)
print("Pairwise time:", pairwise_time)

# Edge cases
print("\nEDGE CASES:")
print("Empty contacts:", merge_contacts([]))
print("Missing phone:", merge_contacts([{"name": "Arun", "phone": "", "email": ""}]))
print("Missing email:", merge_contacts([{"name": "Ravi", "phone": "9876543210"}]))
