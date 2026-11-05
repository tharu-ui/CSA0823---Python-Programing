# Demonstrating mutable default arguments

def add_item_buggy(item, order=[]):
    order.append(item)
    return order


# Corrected version using None

def add_item(item, order=None):
    if order is None:
        order = []

    order.append(item)
    return order


# Function with a default argument

def calculate_bill(amount, gst_rate=0.05):
    gst = amount * gst_rate
    total = amount + gst

    return total, gst


# Global variable

count = 0


def update_global():
    global count
    count += 1
    print("Global count:", count)


# Local variable example

def local_example():
    message = "This is a local variable"
    print(message)


# Nonlocal variable example

def nonlocal_example():
    value = 10

    def update_value():
        nonlocal value
        value += 5
        print("Updated enclosing value:", value)

    update_value()


# Passing a separate list explicitly

def add_item_explicit(item, order):
    order.append(item)
    return order


# Closure example

def create_order():
    order = []

    def add(item):
        order.append(item)
        return order.copy()

    return add


print("MUTABLE DEFAULT ARGUMENT DEMONSTRATION")

print("First call:", add_item_buggy("Tea"))
print("Second call:", add_item_buggy("Vada"))

print("\nCORRECTED FUNCTION")

print("First customer:", add_item("Tea"))
print("Second customer:", add_item("Vada"))

print("\nDEFAULT ARGUMENT IN BILL CALCULATION")

total, gst = calculate_bill(1000)

print("Bill amount: Rs.1000")
print("GST:", gst)
print("Total:", total)

print("\nGLOBAL VARIABLE")

update_global()
update_global()

print("\nLOCAL VARIABLE")
local_example()

print("\nNONLOCAL VARIABLE")
nonlocal_example()

print("\nSEPARATE CUSTOMER ORDERS")

customer1 = []
customer2 = []
customer3 = []

print("Customer 1:", add_item_explicit("Tea", customer1))
print("Customer 2:", add_item_explicit("Coffee", customer2))
print("Customer 3:", add_item_explicit("Juice", customer3))

print("\nCLOSURE-BASED ORDERS")

order1 = create_order()
order2 = create_order()

print("Order 1:", order1("Sandwich"))
print("Order 1:", order1("Juice"))
print("Order 2:", order2("Pizza"))