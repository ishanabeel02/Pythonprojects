import random

class WordList:
    def __init__(self):
        self.words = []
        self.add_default_words()

    def add_default_words(self):
        self.words.extend([
            "python", "computer", "program", "science",
            "algorithm", "function", "variable", "object",
            "database", "integer", "string", "network",
            "hardware", "software", "keyboard", "mouse",
            "monitor", "memory", "graphics", "internet"
        ])

    def add_word(self, word):
        word = word.strip().lower()
        if word and word not in self.words:
            self.words.append(word)
            print(f"Word '{word}' added to the game.")
        else:
            print("Word is empty or already exists.")

    def list_words(self):
        print("\n--- Word List ---")
        for idx, word in enumerate(self.words):
            print(f"{idx+1}. {word}")

    def get_random_word(self):
        return random.choice(self.words) if self.words else None

class GameStats:
    def __init__(self):
        self.games_played = 0
        self.games_won = 0
        self.total_attempts = 0

    def record_game(self, won, attempts):
        self.games_played += 1
        if won:
            self.games_won += 1
        self.total_attempts += attempts

    def show_stats(self):
        print("\n--- Game Stats ---")
        print(f"Games Played: {self.games_played}")
        print(f"Games Won: {self.games_won}")
        if self.games_played:
            print(f"Average Attempts per Game: {self.total_attempts / self.games_played:.2f}")

class WordGuessGame:
    def __init__(self):
        self.word_list = WordList()
        self.stats = GameStats()

    def play_game(self):
        print("\n--- New Game ---")
        word = self.word_list.get_random_word()
        if not word:
            print("No words available. Add words first!")
            return
        attempts = 0
        guessed_letters = set()
        display_word = ['_' for _ in word]
        print("Guess the word!")
        while True:
            print("Word: " + " ".join(display_word))
            guess = input("Enter a letter or guess the word: ").strip().lower()
            attempts += 1
            if len(guess) == 1 and guess.isalpha():
                if guess in guessed_letters:
                    print("You already guessed that letter.")
                    continue
                guessed_letters.add(guess)
                if guess in word:
                    print("Good guess!")
                    for i, ch in enumerate(word):
                        if ch == guess:
                            display_word[i] = guess
                    if "_" not in display_word:
                        print(f"Congratulations! You guessed the word '{word}'.")
                        self.stats.record_game(True, attempts)
                        break
                else:
                    print("Wrong guess.")
            elif len(guess) == len(word):
                if guess == word:
                    print(f"Excellent! You guessed the word '{word}'.")
                    self.stats.record_game(True, attempts)
                    break
                else:
                    print("Incorrect word guess.")
            else:
                print("Invalid input. Try again.")
            if attempts >= 10:
                print(f"Out of attempts! The word was '{word}'.")
                self.stats.record_game(False, attempts)
                break

    def add_word(self):
        print("\n--- Add Word ---")
        word = input("Enter new word: ")
        self.word_list.add_word(word)

    def list_words(self):
        self.word_list.list_words()

    def show_stats(self):
        self.stats.show_stats()

    def menu(self):
        while True:
            print("\n=== Word Guess Game ===")
            print("1. Play Game")
            print("2. Add Word")
            print("3. List Words")
            print("4. Show Stats")
            print("5. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.play_game()
            elif choice == "2":
                self.add_word()
            elif choice == "3":
                self.list_words()
            elif choice == "4":
                self.show_stats()
            elif choice == "5":
                print("Thanks for playing!")
                break
            else:
                print("Invalid choice. Try again.")

if __name__ == "__main__":
    wgg = WordGuessGame()
    wgg.menu()