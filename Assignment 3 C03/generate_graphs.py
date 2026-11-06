
import os
import matplotlib.pyplot as plt

# Base directory: Assignment 3 C03
BASE = os.path.dirname(os.path.abspath(__file__))


# Function to save individual graphs
def save_graph(folder, filename, title, x_label, y_label,
               labels, values, log_scale=False):

    output_folder = os.path.join(BASE, folder)
    os.makedirs(output_folder, exist_ok=True)

    plt.figure(figsize=(9, 5))

    bars = plt.bar(labels, values)

    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    if log_scale:
        plt.yscale("log")

    for bar, value in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.6g}",
            ha="center",
            va="bottom",
            fontsize=8
        )

    plt.tight_layout()

    path = os.path.join(output_folder, filename)
    plt.savefig(path, dpi=300)
    plt.close()

    print("Saved:", path)


# ==================================================
# QUESTION 1 - LISTS AND SLICING
# ==================================================

sizes = ["365", "36,500", "365,000"]

naive_times = [
    0.000092794,
    0.009330441,
    0.131179974
]

running_times = [
    0.000032832,
    0.003899775,
    0.038644614
]

plt.figure(figsize=(9, 5))

x = range(len(sizes))
width = 0.35

plt.bar(
    [i - width / 2 for i in x],
    naive_times,
    width,
    label="Naive Method"
)

plt.bar(
    [i + width / 2 for i in x],
    running_times,
    width,
    label="Running-Sum Method"
)

plt.xticks(list(x), sizes)
plt.xlabel("Number of Readings")
plt.ylabel("Execution Time (seconds)")
plt.title("Q1 - Moving Average Performance Comparison")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()

q1_folder = os.path.join(BASE, "Task01")
os.makedirs(q1_folder, exist_ok=True)

plt.savefig(
    os.path.join(q1_folder, "q1_moving_average_comparison.png"),
    dpi=300
)
plt.close()

print("Saved Q1 graph.")


# ==================================================
# QUESTION 2 - TUPLES AND COPYING
# ==================================================

save_graph(
    "Task02",
    "q2_memory_comparison.png",
    "Q2 - List and Tuple Memory Comparison",
    "Data Structure",
    "Memory Usage (Bytes)",
    ["List", "Tuple"],
    [8000056, 8000048]
)

save_graph(
    "Task02",
    "q2_creation_time.png",
    "Q2 - List and Tuple Creation Time",
    "Data Structure",
    "Execution Time (seconds)",
    ["List", "Tuple"],
    [0.034056011, 0.044968517]
)

save_graph(
    "Task02",
    "q2_indexing_time.png",
    "Q2 - List and Tuple Indexing Time",
    "Data Structure",
    "Execution Time (seconds)",
    ["List", "Tuple"],
    [0.013628641, 0.007445179]
)


# ==================================================
# QUESTION 3 - DICTIONARIES
# ==================================================

sizes = ["1,000", "10,000", "100,000"]

dictionary_times = [
    0.000132558,
    0.001377553,
    0.035158101
]

counter_times = [
    0.000057116,
    0.000415767,
    0.016216515
]

list_count_times = [
    0.000125695,
    0.001281093,
    0.044500674
]

plt.figure(figsize=(9, 5))

x = range(len(sizes))
width = 0.25

plt.bar(
    [i - width for i in x],
    dictionary_times,
    width,
    label="Dictionary"
)

plt.bar(
    list(x),
    counter_times,
    width,
    label="Counter"
)

plt.bar(
    [i + width for i in x],
    list_count_times,
    width,
    label="list.count()"
)

plt.xticks(list(x), sizes)
plt.xlabel("Number of Words")
plt.ylabel("Execution Time (seconds)")
plt.title("Q3 - Word Frequency Performance Comparison")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()

q3_folder = os.path.join(BASE, "Task03")
os.makedirs(q3_folder, exist_ok=True)

plt.savefig(
    os.path.join(q3_folder, "q3_word_frequency_comparison.png"),
    dpi=300
)
plt.close()

print("Saved Q3 graph.")


# ==================================================
# QUESTION 4 - SETS
# ==================================================

sizes = ["10,000", "100,000", "1,000,000"]

list_times = [
    0.000078277,
    0.000807580,
    0.016992885
]

set_times = [
    0.000000572,
    0.000001172,
    0.000001693
]

plt.figure(figsize=(9, 5))

x = range(len(sizes))
width = 0.35

plt.bar(
    [i - width / 2 for i in x],
    list_times,
    width,
    label="List Membership"
)

plt.bar(
    [i + width / 2 for i in x],
    set_times,
    width,
    label="Set Membership"
)

plt.xticks(list(x), sizes)
plt.xlabel("Number of Elements")
plt.ylabel("Execution Time (seconds)")
plt.title("Q4 - List and Set Membership Performance")
plt.yscale("log")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()

q4_folder = os.path.join(BASE, "Task04")
os.makedirs(q4_folder, exist_ok=True)

plt.savefig(
    os.path.join(q4_folder, "q4_membership_comparison.png"),
    dpi=300
)
plt.close()

save_graph(
    "Task04",
    "q4_intersection_comparison.png",
    "Q4 - Nested Loop and Set Intersection",
    "Method",
    "Execution Time (seconds)",
    ["Nested Loop", "Set Intersection"],
    [0.192915766, 0.000094777],
    log_scale=True
)


# ==================================================
# QUESTION 5 - LIST COMPREHENSION
# ==================================================

sizes = ["10,000", "100,000", "1,000,000"]

comprehension_times = [
    0.003755065,
    0.005992294,
    0.085760163
]

filter_times = [
    0.001436713,
    0.014035260,
    0.183301233
]

plt.figure(figsize=(9, 5))

x = range(len(sizes))
width = 0.35

plt.bar(
    [i - width / 2 for i in x],
    comprehension_times,
    width,
    label="List Comprehension"
)

plt.bar(
    [i + width / 2 for i in x],
    filter_times,
    width,
    label="Filter"
)

plt.xticks(list(x), sizes)
plt.xlabel("Number of Readings")
plt.ylabel("Execution Time (seconds)")
plt.title("Q5 - List Comprehension and Filter Performance")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()

q5_folder = os.path.join(BASE, "Task05")
os.makedirs(q5_folder, exist_ok=True)

plt.savefig(
    os.path.join(q5_folder, "q5_execution_time.png"),
    dpi=300
)
plt.close()

save_graph(
    "Task05",
    "q5_memory_comparison.png",
    "Q5 - List and Generator Memory Comparison",
    "Data Structure",
    "Memory Usage (Bytes)",
    ["List", "Generator"],
    [800056, 200]
)


# ==================================================
# QUESTION 6 - RAILWAY TIMETABLE
# ==================================================

sizes = ["100", "1,000", "10,000"]

without_index = [
    0.000018454,
    0.000144900,
    0.001514179
]

with_index = [
    0.000009157,
    0.000080310,
    0.000966466
]

plt.figure(figsize=(9, 5))

x = range(len(sizes))
width = 0.35

plt.bar(
    [i - width / 2 for i in x],
    without_index,
    width,
    label="Without Index"
)

plt.bar(
    [i + width / 2 for i in x],
    with_index,
    width,
    label="With Index"
)

plt.xticks(list(x), sizes)
plt.xlabel("Number of Trains")
plt.ylabel("Execution Time (seconds)")
plt.title("Q6 - Railway Search Performance Comparison")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.5)
plt.tight_layout()

q6_folder = os.path.join(BASE, "Task06")
os.makedirs(q6_folder, exist_ok=True)

plt.savefig(
    os.path.join(q6_folder, "q6_index_comparison.png"),
    dpi=300
)
plt.close()


# ==================================================
# QUESTION 7 - CONTACT MERGING
# ==================================================

save_graph(
    "Task07",
    "q7_merging_comparison.png",
    "Q7 - Dictionary Merging and Pairwise Comparison",
    "Method (1,000 Contacts)",
    "Execution Time (seconds)",
    ["Dictionary Merging", "Pairwise Comparison"],
    [0.002560663, 1.494804197],
    log_scale=True
)

save_graph(
    "Task07",
    "q7_dictionary_scaling.png",
    "Q7 - Dictionary Merging with Increasing Contacts",
    "Number of Contacts",
    "Execution Time (seconds)",
    ["1,000", "100,000"],
    [0.002560663, 0.986334662]
)


# ==================================================
# COMPLETION MESSAGE
# ==================================================

print("\n======================================")
print("ALL GRAPH FILES GENERATED SUCCESSFULLY")
print("======================================")
print("Total graphs: 12")
print("Check Task01 to Task07 folders.")
