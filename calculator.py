import math

# ---- Basic Operations ----
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Error! Division by zero."

def modulus(a, b):
    try:
        return a % b
    except ZeroDivisionError:
        return "Error! Modulus by zero."

# ---- Advanced Operations ----
def power(a, b):
    return a ** b

def square_root(a):
    try:
        if a < 0:
            return "Error! Square root of negative number."
        return math.sqrt(a)
    except ValueError:
        return "Error!"

def factorial(n):
    try:
        if n < 0:
            return "Error! Factorial of negative number."
        return math.factorial(int(n))
    except (ValueError, OverflowError):
        return "Error!"

def sine(deg):
    return math.sin(math.radians(deg))

def cosine(deg):
    return math.cos(math.radians(deg))

def tangent(deg):
    try:
        return math.tan(math.radians(deg))
    except Exception:
        return "Error!"

def logarithm(a):
    try:
        if a <= 0:
            return "Error! Log undefined for <= 0."
        return math.log10(a)
    except ValueError:
        return "Error!"

# ---- Main Calculator ----
def calculator():
    while True:
        print("\n===== 🔢 Scientific Calculator =====")
        print("1. Addition (+)")
        print("2. Subtraction (-)")
        print("3. Multiplication (*)")
        print("4. Division (/)")
        print("5. Modulus (%)")
        print("6. Power (x^y)")
        print("7. Square Root (√x)")
        print("8. Factorial (n!)")
        print("9. Sine (sin x°)")
        print("10. Cosine (cos x°)")
        print("11. Tangent (tan x°)")
        print("12. Logarithm (log10 x)")
        print("13. Exit")

        try:
            choice = int(input("👉 Enter choice (1-13): "))

            if choice == 13:
                print("✅ Exiting Calculator. Goodbye!")
                break

            # Operations needing 2 inputs
            if choice in [1, 2, 3, 4, 5, 6]:
                try:
                    num1 = float(input("Enter first number: "))
                    num2 = float(input("Enter second number: "))
                except ValueError:
                    print("⚠ Invalid input! Enter numbers only.")
                    continue

                if choice == 1:
                    print(f"Result: {num1} + {num2} = {add(num1, num2)}")
                elif choice == 2:
                    print(f"Result: {num1} - {num2} = {subtract(num1, num2)}")
                elif choice == 3:
                    print(f"Result: {num1} * {num2} = {multiply(num1, num2)}")
                elif choice == 4:
                    print(f"Result: {num1} / {num2} = {divide(num1, num2)}")
                elif choice == 5:
                    print(f"Result: {num1} % {num2} = {modulus(num1, num2)}")
                elif choice == 6:
                    print(f"Result: {num1}^{num2} = {power(num1, num2)}")

            # Operations needing 1 input
            elif choice in [7, 8, 9, 10, 11, 12]:
                try:
                    num = float(input("Enter number: "))
                except ValueError:
                    print("⚠ Invalid input! Enter numbers only.")
                    continue

                if choice == 7:
                    print(f"√{num} = {square_root(num)}")
                elif choice == 8:
                    print(f"{int(num)}! = {factorial(num)}")
                elif choice == 9:
                    print(f"sin({num}°) = {sine(num)}")
                elif choice == 10:
                    print(f"cos({num}°) = {cosine(num)}")
                elif choice == 11:
                    print(f"tan({num}°) = {tangent(num)}")
                elif choice == 12:
                    print(f"log10({num}) = {logarithm(num)}")

            else:
                print("⚠ Invalid choice! Enter between 1–13.")

        except ValueError:
            print("⚠ Please enter a valid integer choice.")

# Run calculator
calculator()
