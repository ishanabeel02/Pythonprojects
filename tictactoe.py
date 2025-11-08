import random


def print_board(board):
    """Display Tic Tac Toe board (clean style, no side |)"""
    print("\n    0   1   2")
    for i, row in enumerate(board):
        print(f"{i}   " + " | ".join(row))
        if i < 2:
            print("   " + "---+---+---")
    print()


def check_winner(board, player):
    """Check if the player has won"""
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_full(board):
    """Check if the board is full"""
    return all(cell != " " for row in board for cell in row)


def player_move(board, player):
    """Handle human player move"""
    while True:
        try:
            row = int(input(f"👉 Player {player}, enter row (0-2): "))
            col = int(input(f"👉 Player {player}, enter column (0-2): "))

            if row not in range(3) or col not in range(3):
                print("⚠ Invalid position! Choose numbers between 0–2.")
                continue

            if board[row][col] != " ":
                print("⚠ That spot is already taken. Try again.")
                continue

            board[row][col] = player
            break
        except ValueError:
            print("⚠ Please enter valid numbers (0–2).")


def computer_move(board):
    """Computer picks a random empty spot"""
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]
    row, col = random.choice(empty_cells)
    print(f"🤖 Computer chose: {row}, {col}")
    board[row][col] = "O"


def play_game(mode):
    """Play one full game"""
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"

    while True:
        print_board(board)

        if mode == "pvp" or (mode == "pvc" and current_player == "X"):
            player_move(board, current_player)
        else:
            computer_move(board)

        # Check for win
        if check_winner(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins!")
            break

        # Check for draw
        if is_full(board):
            print_board(board)
            print("🤝 It's a draw!")
            break

        # Switch turn
        current_player = "O" if current_player == "X" else "X"


def tic_tac_toe():
    """Main menu with replay option"""
    print("🎮 Welcome to Tic Tac Toe!")

    while True:
        print("\nChoose a mode:")
        print("1. Player vs Player")
        print("2. Player vs Computer")

        choice = input("👉 Enter choice (1/2): ").strip()
        if choice == "1":
            play_game("pvp")
        elif choice == "2":
            play_game("pvc")
        else:
            print("⚠ Invalid choice! Try again.")
            continue

        # Replay option
        again = input("\n🔄 Do you want to play again? (yes/no): ").strip().lower()
        if again not in ["yes", "y"]:
            print("👋 Thanks for playing! Goodbye.")
            break


# Run the game
tic_tac_toe()
