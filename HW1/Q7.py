def greet(name, greeting="Hello"):
    return greeting + " " + name


print(greet("Priya"))
print(greet("Priya", "Good Morning"))
print(greet(name="Priya"))
print(greet(greeting="Good Evening", name="Priya"))

