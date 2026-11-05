CORRECT_OTP = "4821"


def verify_while():
    print("\nOTP VERIFICATION USING WHILE LOOP")

    attempts = 0
    maximum_attempts = 3

    while attempts < maximum_attempts:
        otp = input("Enter OTP: ").strip()

        if otp == "":
            print("OTP cannot be empty.")
            continue

        attempts += 1

        if otp == CORRECT_OTP:
            pass
            print("OTP verified successfully!")
            break
        else:
            print("Incorrect OTP.")
            print("Attempts used:", attempts)

        if attempts == 3:
            answer = input("Answer security question? (yes/no): ").lower()

            if answer == "yes":
                maximum_attempts = 5
                print("Two extra attempts granted.")
            else:
                maximum_attempts = attempts

    else:
        print("Maximum attempts reached. Account locked.")


def verify_for():
    print("\nOTP VERIFICATION USING FOR LOOP")

    for attempt in range(5):
        if attempt == 3:
            answer = input("Answer security question? (yes/no): ").lower()

            if answer != "yes":
                print("Account locked.")
                break

            print("Two extra attempts granted.")

        while True:
            otp = input("Enter OTP: ").strip()

            if otp == "":
                print("OTP cannot be empty.")
                continue

            break

        if otp == CORRECT_OTP:
            pass
            print("OTP verified successfully!")
            break
        else:
            print("Incorrect OTP.")
            print("Attempts used:", attempt + 1)

    else:
        print("Maximum attempts reached. Account locked.")


def verify_recursive(attempts=0):
    if attempts == 3:
        print("Maximum attempts reached. Account locked.")
        return

    otp = input("Enter OTP: ").strip()

    if otp == "":
        print("OTP cannot be empty.")
        verify_recursive(attempts)
        return

    if otp == CORRECT_OTP:
        print("OTP verified successfully!")
        return

    print("Incorrect OTP.")
    verify_recursive(attempts + 1)


print("1. While Loop")
print("2. For Loop")
print("3. Recursive Verification")

choice = input("Choose an option: ")

if choice == "1":
    verify_while()
elif choice == "2":
    verify_for()
elif choice == "3":
    print("\nOTP VERIFICATION USING RECURSION")
    verify_recursive()
else:
    print("Invalid choice.")