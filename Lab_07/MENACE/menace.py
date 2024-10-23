from collections import Counter
import random

class Board:
    def __init__(self):
        self.board = [' '] * 9

    def __str__(self):
        return("\n 0 | 1 | 2     %s | %s | %s\n"
               "---+---+---   ---+---+---\n"
               " 3 | 4 | 5     %s | %s | %s\n"
               "---+---+---   ---+---+---\n"
               " 6 | 7 | 8     %s | %s | %s" % (self.board[0], self.board[1], self.board[2],
                                                self.board[3], self.board[4], self.board[5],
                                                self.board[6], self.board[7], self.board[8]))

    def valid_move(self, move):
        if move.isdigit() and 0 <= int(move) <= 8 and self.board[int(move)] == ' ':
            return True
        return False

    def winning(self):
        win_conditions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), 
                          (0, 3, 6), (1, 4, 7), (2, 5, 8), 
                          (0, 4, 8), (2, 4, 6)]
        for a, b, c in win_conditions:
            if self.board[a] == self.board[b] == self.board[c] and self.board[a] != ' ':
                return True
        return False

    def draw(self):
        return all((x != ' ' for x in self.board))

    def play_move(self, position, marker):
        self.board[position] = marker

    def board_string(self):
        return ''.join(self.board)


class MenacePlayer:
    def __init__(self):
        self.matchboxes = {}
        self.num_win = 0
        self.num_draw = 0
        self.num_lose = 0

    def start_game(self):
        self.moves_played = []

    def get_move(self, board):
        board_str = board.board_string()
        if board_str not in self.matchboxes:
            new_beads = [i for i, mark in enumerate(board_str) if mark == ' ']
            self.matchboxes[board_str] = new_beads * ((len(new_beads) + 2) // 2)

        beads = self.matchboxes[board_str]
        if len(beads):
            bead = random.choice(beads)
            self.moves_played.append((board_str, bead))
        else:
            bead = -1  # No valid moves, so resign
        return bead

    def win_game(self):
        for (board, bead) in self.moves_played:
            self.matchboxes[board].extend([bead] * 3)
        self.num_win += 1

    def draw_game(self):
        for (board, bead) in self.moves_played:
            self.matchboxes[board].append(bead)
        self.num_draw += 1

    def lose_game(self):
        for (board, bead) in self.moves_played:
            matchbox = self.matchboxes[board]
            if bead in matchbox:
                matchbox.remove(bead)
        self.num_lose += 1

    def print_stats(self):
        print(f"Learned {len(self.matchboxes)} boards")
        print(f"Win/Draw/Lose: {self.num_win}/{self.num_draw}/{self.num_lose}")

    def print_probability(self, board):
        board_str = board.board_string()
        try:
            print("Stats for this board: " +
                  str(Counter(self.matchboxes[board_str]).most_common()))
        except KeyError:
            print("MENACE has never seen this board before.")


class HumanPlayer:
    def start_game(self):
        print("Game starting. Good luck!")

    def get_move(self, board):
        while True:
            move = input('Enter your move (0-8): ')
            if board.valid_move(move):
                return int(move)
            print("Invalid move. Please try again.")

    def win_game(self):
        print("Congratulations, you won!")

    def draw_game(self):
        print("It's a draw.")

    def lose_game(self):
        print("You lost. Better luck next time!")

    def print_probability(self, board):
        pass


def play_game(first, second, silent=False):
    first.start_game()
    second.start_game()
    board = Board()

    if not silent:
        print("\nStarting a new game!")
        print(board)

    while True:
        if not silent:
            first.print_probability(board)
        move = first.get_move(board)
        if move == -1:
            if not silent:
                print("Player resigns")
            first.lose_game()
            second.win_game()
            break
        board.play_move(move, 'X')
        if not silent:
            print(board)
        if board.winning():
            first.win_game()
            second.lose_game()
            break
        if board.draw():
            first.draw_game()
            second.draw_game()
            break

        if not silent:
            second.print_probability(board)
        move = second.get_move(board)
        if move == -1:
            if not silent:
                print("Player resigns")
            second.lose_game()
            first.win_game()
            break
        board.play_move(move, 'O')
        if not silent:
            print(board)
        if board.winning():
            second.win_game()
            first.lose_game()
            break


if __name__ == '__main__':
    menace1 = MenacePlayer()
    menace2 = MenacePlayer()
    human = HumanPlayer()

    # Let MENACE play against itself for 1000 games
    for i in range(1000):
        play_game(menace1, menace2, silent=True)

    menace1.print_stats()
    menace2.print_stats()

    # Now play against the human player
    play_game(menace1, human)
    play_game(human, menace2)
