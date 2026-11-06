import matplotlib.pyplot as plt

# Actual measurements from Codespaces
n_values = [10, 20, 25, 30]

original_time = [0.000021, 0.001633, 0.019056, 0.445328]
redesigned_time = [0.000006, 0.000009, 0.000014, 0.000026]

# Create performance graph
plt.figure(figsize=(9, 5))

plt.plot(n_values, original_time, marker='o',
         label='Original Recursive Program')

plt.plot(n_values, redesigned_time, marker='s',
         label='Redesigned Memoized Program')

plt.xlabel('Input Value (n)')
plt.ylabel('Execution Time (seconds)')
plt.title('Performance Comparison: Original vs Redesigned Program')

plt.xticks(n_values)
plt.grid(True)
plt.legend()

plt.tight_layout()

# Save graph
plt.savefig(
    'Assignment 2 C02 /Task 7/q7_performance_graph.png',
    dpi=300
)

plt.show()

print("Q7 performance graph saved successfully!")