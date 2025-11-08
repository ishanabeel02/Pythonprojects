import random

def number_guess_game():
    print("🎯 Welcome to the Advanced Number Guessing Game!")

    while True:  # Play again loop
        print("\nChoose a difficulty level:")
        print("1. Easy   (1-20, 7 attempts)")
        print("2. Medium (1-50, 6 attempts)")
        print("3. Hard   (1-100, 5 attempts)")

        # Select difficulty
        while True:
            try:
                level = int(input("👉 Select level (1-3): "))
                if level == 1:
                    low, high, max_attempts = 1, 20, 7
                elif level == 2:
                    low, high, max_attempts = 1, 50, 6
                elif level == 3:
                    low, high, max_attempts = 1, 100, 5
                else:
                    print("⚠ Please select 1, 2, or 3 only.")
                    continue
                break
            except ValueError:
                print("⚠ Invalid input! Enter a number (1-3).")

        # Ask for hints option
        while True:
            hint_choice = input("👉 Do you want hints? (yes/no): ").strip().lower()
            if hint_choice in ["yes", "y"]:
                hints = True
                break
            elif hint_choice in ["no", "n"]:
                hints = False
                break
            else:
                print("⚠ Please type 'yes' or 'no'.")

        # Generate secret number
        secret_number = random.randint(low, high)
        attempts = 0

        print(f"\n✅ I picked a number between {low} and {high}. You have {max_attempts} attempts!")

        # Game loop
        while attempts < max_attempts:
            try:
                guess = int(input(f"\nAttempt {attempts+1}/{max_attempts} - Enter your guess: "))
                attempts += 1

                if guess < low or guess > high:
                    print(f"⚠ Guess within the range {low}-{high}!")
                    continue

                if guess == secret_number:
                    print(f"🎉 Correct! You guessed it in {attempts} attempts.")
                    break
                else:
                    if hints:  # give hints only if enabled
                        if guess < secret_number:
                            print("📉 Too low!")
                        else:
                            print("📈 Too high!")
                    else:
                        print("❌ Wrong guess!")
            except ValueError:
                print("⚠ Invalid input! Please enter a number.")
                continue
        else:
            print(f"❌ Game Over! The number was {secret_number}.")

        # Ask if user wants to play again
        play_again = input("\n🔄 Do you want to play again? (yes/no): ").strip().lower()
        if play_again not in ["yes", "y"]:
            print("👋 Thanks for playing! Goodbye.")
            break


# Run the game
number_guess_game()
