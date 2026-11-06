
import random
import string
import time
from collections import Counter

calls = [
    "seeds not received seeds delayed",
    "fertiliser price high",
    "seeds price high subsidy not received",
]

STOP = {"not", "high"}

def clean_words(text):
    text = text.lower()

    for symbol in string.punctuation:
        text = text.replace(symbol, " ")

    return [word for word in text.split() if word not in STOP]


def dictionary_count(sentences):
    counts = {}

    for sentence in sentences:
        for word in clean_words(sentence):
            counts[word] = counts.get(word, 0) + 1

    return counts


def top_words(counts, k):
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:k]


print("WORD FREQUENCY:")
counts = dictionary_count(calls)
print(counts)

print("\nTOP THREE WORDS:")
print(top_words(counts, 3))

# setdefault example
district_complaints = [
    ("Chennai", "Seeds delayed"),
    ("Madurai", "Fertiliser issue"),
    ("Chennai", "Water shortage"),
    ("Salem", "Seed quality")
]

grouped = {}

for district, complaint in district_complaints:
    grouped.setdefault(district, []).append(complaint)

print("\nCOMPLAINTS BY DISTRICT:")
print(grouped)

# Complete the code
print("\nCOMPLETE THE CODE:")
print(top_words(dictionary_count(calls), 3))

# Performance comparison
vocabulary = [
    "seeds", "water", "fertiliser", "price", "subsidy",
    "crop", "loan", "market", "soil", "weather"
]

print("\nPERFORMANCE COMPARISON:")

for size in [1000, 10000, 100000]:
    words = [random.choice(vocabulary) for i in range(size)]

    start = time.perf_counter()
    result = {}
    for word in words:
        result[word] = result.get(word, 0) + 1
    dictionary_time = time.perf_counter() - start

    start = time.perf_counter()
    result2 = Counter(words)
    counter_time = time.perf_counter() - start

    start = time.perf_counter()
    result3 = {}
    for word in set(words):
        result3[word] = words.count(word)
    list_time = time.perf_counter() - start

    print("\nWords:", size)
    print("Dictionary time:", dictionary_time)
    print("Counter time:", counter_time)
    print("list.count time:", list_time)

# Edge cases
print("\nEDGE CASES:")
print("Empty:", dictionary_count([]))
print("Case and punctuation:", dictionary_count(["Seeds, SEEDS! seeds."]))
print("Only stop words:", dictionary_count(["not high not high"]))
