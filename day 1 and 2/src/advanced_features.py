from functools import reduce

# List comprehension
squares = [x**2 for x in range(10)]
print("Squares:", squares)

# Dictionary comprehension
cubes = {x: x**3 for x in range(5)}
print("Cubes:", cubes)

# Lambda
double = lambda x: x * 2
print("Double of 5:", double(5))

# Map
numbers = [1, 2, 3, 4]
mapped = list(map(lambda x: x * 2, numbers))
print("Map:", mapped)

# Filter
filtered = list(filter(lambda x: x % 2 == 0, numbers))
print("Filter:", filtered)

# Reduce
summed = reduce(lambda x, y: x + y, numbers)
print("Reduce:", summed)

# *args and **kwargs
def demo(*args, **kwargs):
    print("Args:", args)
    print("Kwargs:", kwargs)

demo(1, 2, 3, name="Kanishk", role="Intern")

# Context Manager
with open("sample.txt", "w") as file:
    file.write("Hello from context manager")