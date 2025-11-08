import tkinter as tk
import random
import time

# Fruit emojis (at least 8 unique for a 4x4 grid)
FRUITS = [
    "🍎", "🍌", "🍇", "🍉", "🍓", "🍒", "🍍", "🥝",
    "🍑", "🍐", "🍊", "🍋", "🥥", "🥭", "🍈", "🍅"
]

class Card:
    def __init__(self, value):
        self.value = value
        self.flipped = False
        self.matched = False

class MemoryGame:
    def __init__(self, root, rows=4, cols=4):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.size = rows * cols
        self.moves = 0
        self.start_time = None
        self.cards = []
        self.buttons = []
        self.flipped_indices = []
        self.matched_indices = set()
        self.status = None
        self.timer_label = None
        self.reset_button = None
        self.create_cards()
        self.create_board()
        self.create_status_bar()
        self.create_timer()
        self.create_reset_button()
        self.update_timer()

    def create_cards(self):
        # Select fruits and create pairs
        unique_fruits = FRUITS[:self.size // 2]
        values = unique_fruits * 2
        random.shuffle(values)
        self.cards = [Card(value) for value in values]

    def create_board(self):
        for j in range(self.size):
            btn = tk.Button(self.root, text="?", width=6, height=3,
                            font=("Arial", 18),
                            command=lambda i=j: self.flip_card(i))
            btn.grid(row=j // self.cols, column=j % self.cols)
            self.buttons.append(btn)

    def create_status_bar(self):
        self.status = tk.Label(self.root, text="Moves: 0", font=("Arial", 12))
        self.status.grid(row=self.rows, column=0, columnspan=self.cols)

    def create_timer(self):
        self.timer_label = tk.Label(self.root, text="Time: 0s", font=("Arial", 12))
        self.timer_label.grid(row=self.rows + 1, column=0, columnspan=self.cols)
        self.start_time = time.time()

    def create_reset_button(self):
        self.reset_button = tk.Button(self.root, text="Reset", font=("Arial", 12), command=self.reset_game)
        self.reset_button.grid(row=self.rows + 2, column=0, columnspan=self.cols)

    def flip_card(self, idx):
        if self.cards[idx].flipped or self.cards[idx].matched:
            return
        self.cards[idx].flipped = True
        self.buttons[idx]['text'] = self.cards[idx].value
        self.flipped_indices.append(idx)
        if len(self.flipped_indices) == 2:
            self.root.after(700, self.check_match)

    def check_match(self):
        idx1, idx2 = self.flipped_indices
        card1, card2 = self.cards[idx1], self.cards[idx2]
        if card1.value == card2.value:
            card1.matched = True
            card2.matched = True
            self.matched_indices.add(idx1)
            self.matched_indices.add(idx2)
            self.buttons[idx1]['state'] = 'disabled'
            self.buttons[idx2]['state'] = 'disabled'
        else:
            card1.flipped = False
            card2.flipped = False
            self.buttons[idx1]['text'] = "?"
            self.buttons[idx2]['text'] = "?"
        self.flipped_indices = []
        self.moves += 1
        self.status['text'] = f"Moves: {self.moves}"
        if len(self.matched_indices) == self.size:
            elapsed = int(time.time() - self.start_time)
            self.status['text'] += f" - You win! (Time: {elapsed}s)"
            self.timer_label['text'] = "Game Over!"

    def update_timer(self):
        if len(self.matched_indices) < self.size:
            elapsed = int(time.time() - self.start_time)
            self.timer_label['text'] = f"Time: {elapsed}s"
            self.root.after(1000, self.update_timer)

    def reset_game(self):
        for btn in self.buttons:
            btn.destroy()
        self.buttons = []
        self.cards = []
        self.flipped_indices = []
        self.matched_indices = set()
        self.moves = 0
        self.start_time = time.time()
        self.create_cards()
        self.create_board()
        self.status['text'] = "Moves: 0"
        self.timer_label['text'] = "Time: 0s"
        self.update_timer()

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Memory Game")
    game = MemoryGame(root, rows=4, cols=4)
    root.mainloop()