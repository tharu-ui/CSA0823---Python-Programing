import matplotlib.pyplot as plt

# Actual measurements from Codespaces
items = [1000, 10000, 200000]

repeated_plus = [0.000444, 0.004144, 0.186266]
join_method = [0.000299, 0.003080, 0.120280]
fstring_join = [0.000276, 0.002884, 0.071510]

# Create line graph
plt.figure(figsize=(9, 5))

plt.plot(items, repeated_plus, marker='o', label='Repeated +')
plt.plot(items, join_method, marker='s', label='Join()')
plt.plot(items, fstring_join, marker='^', label='F-string + Join()')

plt.xscale('log')

plt.xlabel('Number of Items')
plt.ylabel('Execution Time (seconds)')
plt.title('Performance Comparison of String Building Methods')

plt.xticks(items, ['1,000', '10,000', '200,000'])
plt.grid(True)
plt.legend()

plt.tight_layout()

# Save graph
plt.savefig('Assignment 2 C02 /Task 4/q4_performance_graph.png',
            dpi=300)

plt.show()

print("Performance graph saved successfully!")