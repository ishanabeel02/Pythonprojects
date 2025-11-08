import random
import os
import time

class RockPaperScissorsAI:
    def __init__(self):
        self.moves = ["rock", "paper", "scissors"]
        self.player_history = []
        self.scores = {"Player": 0, "AI": 0, "Draws": 0}

    def predict_player_move(self):
        if len(self.player_history) < 2:
            return random.choice(self.moves)

        # Count frequencies of player's last move
        last_move = self.player_history[-1]
        move_counts = {m: 0 for m in self.moves}

        for i in range(len(self.player_history) - 1):
            if self.player_history[i] == last_move:
                next_move = self.player_history[i + 1]
                move_counts[next_move] += 1

        # Predict the most likely next move
        predicted_move = max(move_counts, key=move_counts.get)
        return predicted_move

    def ai_choice(self):
        predicted = self.predict_player_move()

        # AI chooses the counter move
        if predicted == "rock":
            return "paper"
        elif predicted == "paper":
            return "scissors"
        else:
            return "rock"

    def decide_winner(self, player, ai):
        if player == ai:
            self.scores["Draws"] += 1
            return "Draw"

        win_conditions = {
            "rock": "scissors",
            "scissors": "paper",
            "paper": "rock"
        }

        if win_conditions[player] == ai:
            self.scores["Player"] += 1
            return "Player"
        else:
            self.scores["AI"] += 1
            return "AI"

    def display_scores(self):
        print("\n📊 Current Scores:")
        for k, v in self.scores.items():
            print(f"  {k}: {v}")
        print("-")


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    game = RockPaperScissorsAI()

    print("""
==============================
 Rock-Paper-Scissors with AI 🎮
==============================
(Type 'quit' to stop playing)
""")

    while True:
        player = input("Choose Rock, Paper, or Scissors: ").strip().lower()

        if player == "quit":
            break
        if player not in ["rock", "paper", "scissors"]:
            print("❌ Invalid choice, try again!")
            continue

        ai = game.ai_choice()
        game.player_history.append(player)

        winner = game.decide_winner(player, ai)

        print(f"You chose: {player.capitalize()}")
        time.sleep(0.5)
        print(f"AI chose: {ai.capitalize()}")
        time.sleep(0.5)

        if winner == "Draw":
            print("🤝 It's a draw!")
        elif winner == "Player":
            print("🎉 You win!")
        else:
            print("🤖 AI wins!")

        game.display_scores()

    print("\n🏁 Final Scores:")
    for k, v in game.scores.items():
        print(f"  {k}: {v}")
    print("Thanks for playing!")


if __name__ == "__main__":
    main()