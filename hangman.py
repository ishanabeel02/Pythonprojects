import random
import os


class Hangman:
    def __init__(self):
        self.words = {
            'easy': ['apple', 'house', 'table', 'water', 'happy'],
            'medium': ['elephant', 'bicycle', 'guitar', 'diamond', 'jungle'],
            'hard': ['xylophone', 'quintessential', 'jazz', 'awkward', 'pneumonia']
        }
        self.hangman_stages = [
            """
            ------
            |    |
            |
            |
            |
            |
            -
            """,
            """
            ------
            |    |
            |    O
            |
            |
            |
            -
            """,
            """
            ------
            |    |
            |    O
            |    |
            |
            |
            -
            """,
            """
            ------
            |    |
            |    O
            |   /|
            |
            |
            -
            """,
            """
            ------
            |    |
            |    O
            |   /|\\
            |
            |
            -
            """,
            """
            ------
            |    |
            |    O
            |   /|\\
            |   /
            |
            -
            """,
            """
            ------
            |    |
            |    O
            |   /|\\
            |   / \\
            |
            -
            """
        ]
        self.score = 0
        self.load_score()

    def load_score(self):
        if os.path.exists('hangman_score.txt'):
            with open('hangman_score.txt', 'r') as f:
                self.score = int(f.read())

    def save_score(self):
        with open('hangman_score.txt', 'w') as f:
            f.write(str(self.score))

    def choose_word(self, difficulty):
        return random.choice(self.words[difficulty.lower()])

    def display_word(self, word, guessed_letters):
        display = []
        for letter in word:
            if letter in guessed_letters:
                display.append(letter)
            else:
                display.append('_')
        return ' '.join(display)

    def play(self):
        print("Welcome to Hangman!")
        print(f"Your current score: {self.score}\n")

        # Select difficulty
        while True:
            difficulty = input("Choose difficulty (easy/medium/hard): ").lower()
            if difficulty in ['easy', 'medium', 'hard']:
                break
            print("Invalid difficulty!")

        word = self.choose_word(difficulty)
        guessed_letters = set()
        incorrect_guesses = 0
        max_attempts = len(self.hangman_stages) - 1

        while incorrect_guesses < max_attempts:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.hangman_stages[incorrect_guesses])
            print("\n" + self.display_word(word, guessed_letters))
            print(f"\nIncorrect guesses left: {max_attempts - incorrect_guesses}")
            print(f"Guessed letters: {' '.join(sorted(guessed_letters))}\n")

            guess = input("Guess a letter: ").lower()

            if len(guess) != 1 or not guess.isalpha():
                print("Please enter a single letter!")
                continue

            if guess in guessed_letters:
                print("You already guessed that letter!")
                continue

            guessed_letters.add(guess)

            if guess not in word:
                incorrect_guesses += 1
                print("Incorrect guess!")
            else:
                print("Correct guess!")

            # Check if player won
            if all(letter in guessed_letters for letter in word):
                os.system('cls' if os.name == 'nt' else 'clear')
                print(f"\nCongratulations! You won! The word was: {word}")
                points = (max_attempts - incorrect_guesses) * len(word)
                self.score += points
                print(f"You earned {points} points! Total score: {self.score}")
                self.save_score()
                break

        if incorrect_guesses == max_attempts:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(self.hangman_stages[incorrect_guesses])
            print(f"\nGame Over! The word was: {word}")
            print(f"Your final score: {self.score}")


def main():
    game = Hangman()
    while True:
        game.play()
        if input("\nPlay again? (y/n): ").lower() != 'y':
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()