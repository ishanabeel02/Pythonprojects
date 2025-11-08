import random
import os
import sys
import tty
import termios

# Maze generator + player solver
class MazeGame:
    def __init__(self, width=21, height=15):
        self.width = width if width % 2 == 1 else width + 1
        self.height = height if height % 2 == 1 else height + 1
        self.maze = [["#"] * self.width for _ in range(self.height)]
        self.player_pos = (1, 1)
        self.exit_pos = (self.height - 2, self.width - 2)

    def generate_maze(self):
        def carve(x, y):
            dirs = [(2, 0), (-2, 0), (0, 2), (0, -2)]
            random.shuffle(dirs)
            for dx, dy in dirs:
                nx, ny = x + dx, y + dy
                if 1 <= nx < self.height - 1 and 1 <= ny < self.width - 1:
                    if self.maze[nx][ny] == "#":
                        self.maze[nx - dx // 2][ny - dy // 2] = " "
                        self.maze[nx][ny] = " "
                        carve(nx, ny)

        # Start point
        self.maze[1][1] = " "
        carve(1, 1)
        # Exit
        self.maze[self.exit_pos[0]][self.exit_pos[1]] = "E"

    def print_maze(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        for i, row in enumerate(self.maze):
            line = ""
            for j, cell in enumerate(row):
                if (i, j) == self.player_pos:
                    line += "P"
                else:
                    line += cell
            print(line)

    def move_player(self, dx, dy):
        x, y = self.player_pos
        nx, ny = x + dx, y + dy
        if 0 <= nx < self.height and 0 <= ny < self.width:
            if self.maze[nx][ny] != "#":
                self.player_pos = (nx, ny)

    def play(self):
        self.generate_maze()

        while True:
            self.print_maze()
            if self.player_pos == self.exit_pos:
                print("🎉 Congratulations! You solved the maze!")
                break
            key = get_key()
            if key == "w":
                self.move_player(-1, 0)
            elif key == "s":
                self.move_player(1, 0)
            elif key == "a":
                self.move_player(0, -1)
            elif key == "d":
                self.move_player(0, 1)
            elif key == "q":
                print("👋 Quit game.")
                break


def get_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch


if __name__ == "__main__":
    game = MazeGame(21, 15)
    game.play()