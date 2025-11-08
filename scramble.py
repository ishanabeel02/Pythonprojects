import random
import time

# Word list (can be expanded)
WORDS = [
    "python", "programming", "computer", "keyboard", "laptop",
    "artificial", "intelligence", "machine", "learning", "science",
    "university", "student", "project", "research", "algorithm",
    "database", "network", "hardware", "software", "developer"
]

LEADERBOARD_FILE = "leaderboard.txt"


def scramble(word):
    """Return a scrambled version of a word."""
    letters = list(word)
    random.shuffle(letters)
    return "".join(letters)


def load_leaderboard():
    """Load leaderboard from file."""
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            scores = [line.strip().split(",") for line in f]
            return [(name, int(score)) for name, score in scores]
    except FileNotFoundError:
        return []


def save_leaderboard(scores):
    """Save leaderboard to file."""
    with open(LEADERBOARD_FILE, "w") as f:
        for name, score in scores:
            f.write(f"{name},{score}\n")


def update_leaderboard(player, score):
    """Update leaderboard with new score."""
    scores = load_leaderboard()
    scores.append((player, score))
    scores.sort(key=lambda x: x[1], reverse=True)  # sort by score (desc)
    save_leaderboard(scores[:10])  # keep top 10


def show_leaderboard():
    """Display leaderboard."""
    scores = load_leaderboard()
    print("\n🏆 Leaderboard 🏆")
    if not scores:
        print("No scores yet. Be the first!")
    else:
        for i, (name, score) in enumerate(scores, 1):
            print(f"{i}. {name} - {score} points")
    print("-" * 30)


def play_round(word, attempts=3):
    """Play one round of the scramble game."""
    scrambled = scramble(word)
    print(f"\n🔀 Scrambled word: {scrambled}")
    print(f"Hint: First letter is '{word[0]}' | Word length: {len(word)}")

    for attempt in range(1, attempts + 1):
        guess = input(f"Attempt {attempt}/{attempts} → Your guess: ").lower()

        if guess == word:
            print("✅ Correct!")
            return True
        else:
            print("❌ Wrong guess.")
    print(f"Out of attempts! The correct word was: '{word}'.")
    return False


def play_game():
    """Main game loop."""
    print("\n🔀 Welcome to the Advanced Word Scramble Game! 🔀")
    name = input("Enter your name: ").capitalize()
    print(f"Hello {name}! Let's start...\n")
    time.sleep(1)

    score = 0
    rounds = 5  # total words per game

    for r in range(1, rounds + 1):
        print(f"\n🎮 Round {r}/{rounds}")
        word = random.choice(WORDS)
        if play_round(word):
            score += 10
            print(f"🎯 Score: {score}")
        else:
            print(f"😢 Score remains: {score}")
        time.sleep(1)

    print(f"\nGame over, {name}! Your final score is: {score}")
    update_leaderboard(name, score)
    show_leaderboard()


# Run the game loop
while True:
    play_game()
    again = input("\nDo you want to play again? (y/n): ").lower()
    if again != "y":
        print("Thanks for playing! 👋")
        break
