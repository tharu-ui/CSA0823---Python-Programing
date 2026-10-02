roll_number = int(input("Enter roll number: "))

marks = list(map(int, input("Enter 5 marks: ").split()))

email_ids = set(input("Enter email IDs: ").split())

name = input("Enter name: ")
age = int(input("Enter age: "))
student_class = input("Enter class: ")

student = {
    "name": name,
    "age": age,
    "class": student_class
}

book_issued = input("Is book issued? ")

days = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")

print("Roll number:", roll_number)
print("Marks:", marks)
print("Days:", days)
print("Email IDs:", email_ids)
print("Student:", student)
print("Book issued:", book_issued)