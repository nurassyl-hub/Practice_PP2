
from functools import reduce

nums = [1, 2, 3, 4, 5, 6]

# Task: Use map() and filter()
squared = list(map(lambda x: x**2, nums))
evens = list(filter(lambda x: x % 2 == 0, nums))

# Task: Aggregate with reduce()
total_sum = reduce(lambda x, y: x + y, nums)

print(f"Original: {nums}")
print(f"Squared (map): {squared}")
print(f"Evens (filter): {evens}")
print(f"Sum (reduce): {total_sum}")
