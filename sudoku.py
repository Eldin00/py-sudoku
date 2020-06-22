import random as rnd
import copy


class Grid:
    def __init__(self, board=None):
        if board and len(board) == 81:
            self.board = board[:]
        else:
            self.board = self.random_board()
        self.solutions = []
        self.find_possible()
        self.fill()

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

    def fill(self):
        done = False
        while not done:
            done = True
            for i in range(81):
                if self.board[i] == 0 and len(self.possible[i]) == 1:
                    self.board[i] = self.possible[i].pop()
                    self.find_possible()
                    done = False

    def is_valid(self):
        rv = False
        for i in range(81):
            rv = True
            if self.board[i] == 0:
                if len(self.possible[i]) < 2:
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

    def solve(self, multiple_solutions=False):
        board_stack = []
        solved = 0
        s = 2 if multiple_solutions else 1
        while solved < s:
            if 0 in self.board:
                #improve the efficiency of backtracking by starting from the cells with the fewest posible options.
                m = min(p for p in self.possible if len(p) > 0)
                i = self.possible.index(m)
                board_stack.append(
                    {
                        "brd": self.board[:],
                        "index": i,
                        "value": min(self.possible[i]),
                        "pos": copy.deepcopy(self.possible),
                    }
                )
                self.board[i] = min(self.possible[i])
                self.find_possible()
                self.fill()

            if self.is_valid() and self.board not in self.solutions:
                if self.board.count(0) == 0:
                    solved += 1

                    self.solutions.append(self.board[:])

            else:
                if len(board_stack) == 0:
                    break
                else:
                    while True:
                        t = board_stack.pop()
                        self.board = t["brd"]
                        self.possible = t["pos"]
                        self.possible[t["index"]].remove(t["value"])
                        if len(self.possible[t["index"]]) > 0 or len(board_stack) == 0:
                            break
            if len(board_stack) == 0 and self.board.count(0) == 0:
                break

    def random_board(self):
        return []