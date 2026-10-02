# Method 1: Using global

count = 0

def increase():
    global count
    count = count + 1

increase()

print("After increase:", count)


# Method 2: Using parameters and return value

def increase_count(count):
    count = count + 1
    return count

count = 0
count = increase_count(count)

print("After increase:", count)
