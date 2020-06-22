import random as rnd
import copy


class Grid:
    def __init__(self, board=None):
        self.board = board[:] if board and len(board) == 81 else [0 for _ in range(81)]
        self.find_possible()

    def __repr__(self):
        return self.board

    def __str__(self):
        return str(self.board)

    def row(self, cell):
        c = cell // 9
        return self.board[c * 9 : c * 9 + 9]

    def col(self, cell):
        return self.board[cell % 9 : 81 : 9]

    def block(self, cell):
        r = cell // 27 * 27
        c = cell % 9 // 3 * 3
        return [
            *self.board[r + c : r + c + 3],
            *self.board[r + c + 9 : r + c + 12],
            *self.board[r + c + 18 : r + c + 21],
        ]

    def find_possible(self):
        possible = [{} for _ in range(81)]
        for i in range(81):
            if self.board[i] == 0:
                possible[i] = set(range(1, 10)) - set(self.row(i)).union(
                    set(self.col(i)), set(self.block(i))
                )
        self.possible = possible

    def is_valid(self):
        rv = False
        for i in range(81):
            rv = True
            if self.board[i] == 0:
                if len(self.possible[i]) < 1:
                    rv = False
                    break
                else:
                    continue
            if (
                (self.row(i).count(self.board[i]) > 1)
                or (self.col(i).count(self.board[i]) > 1)
                or (self.block(i).count(self.board[i]) > 1)
            ):
                rv = False
                break
        return rv


class Solver:
    def __init__(self, board=None):
        self.board = board if board else Grid()
        self.solutions = []

    def solve(self, multiple_solutions=False):
        board_stack = []
        solved = 0
        s = 2 if multiple_solutions else 1
        while solved < s:
            if 0 in self.board.board:
                # improve the efficiency of backtracking by starting from the cells with the fewest posible options.
                m = min(p for p in self.board.possible if len(p) > 0)
                i = self.board.possible.index(m)
                board_stack.append(
                    {
                        "brd": self.board.board[:],
                        "index": i,
                        "value": min(self.board.possible[i]),
                        "pos": copy.deepcopy(self.board.possible),
                    }
                )
                self.board.board[i] = min(self.board.possible[i])
                self.board.find_possible()
                self.fill()

            if self.board.is_valid() and self.board.board not in self.solutions:
                if self.board.board.count(0) == 0:
                    solved += 1

                    self.solutions.append(self.board.board[:])

            else:
                if not board_stack:
                    break
                else:
                    while True:
                        t = board_stack.pop()
                        self.board.board = t["brd"]
                        self.board.possible = t["pos"]
                        self.board.possible[t["index"]].remove(t["value"])
                        if len(self.board.possible[t["index"]]) > 0 or not board_stack:
                            break
            if not board_stack and self.board.board.count(0) == 0:
                break
        return (self.solutions, self.board)

    def fill(self):
        done = False
        while not done:
            done = True
            for i in range(81):
                if self.board.board[i] == 0 and len(self.board.possible[i]) == 1:
                    self.board.board[i] = self.board.possible[i].pop()
                    self.board.find_possible()
                    done = False
        return self.board


class RandomBoard:
    def generate(self):
        self.board = Grid()
        complete = False
        while not complete:
            i = self.board.board.index(0)
            self.board.board[i] = rnd.choice(list(self.board.possible[i]))
            self.board.find_possible()
            self.board = Solver(self.board).fill()
            if not self.board.is_valid():
                self.board = Grid()
            else:
                if self.board.board.count(0) == 0:
                    complete = True
        return self.board


