import time
import random
import os
from datetime import datetime


class TypingTest:
    def __init__(self):
        self.sentences = {
            'easy': [
                "The quick brown fox jumps over the lazy dog.",
                "Python is an interpreted high-level programming language.",
                "Always code as if the guy who ends up maintaining your code will be a violent psychopath."
            ],
            'medium': [
                "Programming isn't about what you know; it's about what you can figure out.",
                "The best way to predict the future is to invent it.",
                "Debugging is twice as hard as writing the code in the first place."
            ],
            'hard': [
                "The mathematician's patterns, like the painter's or the poet's, must be beautiful.",
                "Computer science is no more about computers than astronomy is about telescopes.",
                "The Internet? Is that thing still around?"
            ]
        }
        self.results = []
        self.load_results()

    def load_results(self):
        if os.path.exists('typing_results.txt'):
            with open('typing_results.txt', 'r') as f:
                for line in f:
                    if line.strip():
                        self.results.append(line.strip())

    def save_results(self, wpm, accuracy, difficulty):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        result = f"{timestamp} | {difficulty} | {wpm:.1f} WPM | {accuracy:.1f}%"
        self.results.append(result)
        with open('typing_results.txt', 'a') as f:
            f.write(result + '\n')

    def get_random_sentence(self, difficulty):
        return random.choice(self.sentences[difficulty.lower()])

    def calculate_wpm(self, typed_chars, time_sec):
        words = typed_chars / 5  # Standard word length in typing tests
        minutes = time_sec / 60
        return words / minutes if minutes > 0 else 0

    def calculate_accuracy(self, original, typed):
        correct = 0
        for o, t in zip(original, typed):
            if o == t:
                correct += 1
        return (correct / len(original)) * 100 if original else 0

    def run_test(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Typing Speed Test ===")

        # Select difficulty
        while True:
            difficulty = input("Choose difficulty (easy/medium/hard): ").lower()
            if difficulty in ['easy', 'medium', 'hard']:
                break
            print("Invalid difficulty!")

        sentence = self.get_random_sentence(difficulty)
        print(f"\nType the following sentence:\n\n{sentence}\n")
        input("Press Enter when ready...")

        start_time = time.time()
        user_input = input("\nStart typing: ")
        end_time = time.time()

        time_taken = end_time - start_time
        wpm = self.calculate_wpm(len(user_input), time_taken)
        accuracy = self.calculate_accuracy(sentence, user_input)

        print(f"\nTime: {time_taken:.1f} seconds")
        print(f"Speed: {wpm:.1f} WPM")
        print(f"Accuracy: {accuracy:.1f}%")

        self.save_results(wpm, accuracy, difficulty.capitalize())

    def show_history(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=== Your Typing History ===")
        if not self.results:
            print("No results yet!")
            return

        for result in self.results[-10:]:  # Show last 10 results
            print(result)


def main():
    test = TypingTest()
    while True:
        print("\n1. Start Typing Test")
        print("2. View History")
        print("3. Exit")
        choice = input("Choose option: ")

        if choice == '1':
            test.run_test()
        elif choice == '2':
            test.show_history()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()