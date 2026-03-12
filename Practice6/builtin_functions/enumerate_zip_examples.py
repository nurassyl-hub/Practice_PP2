
# Task: Use enumerate() and zip() for paired iteration
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

print("Paired Data:")
for index, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"{index}. {name} scored {score}")

# Task: Demonstrate type checking and conversions
value = "100"
if isinstance(value, str):
    num = int(value)
    print(f"Converted {type(value)} to {type(num)}")
