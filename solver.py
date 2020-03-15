import random as rand
import copy


class Grid:
    def __init__(self, board=None):
        if board:
            self.board = board[:]
        else:
            self.board = random_board()
        self.solutions = []
        self.find_possible()
        self.fill()

    def row(self, cell):
        return self.board[cell // 9 : cell // 9 + 9]

    def col(self, cell):
        return self.board[cell % 9 : 81 : 9]

    def block(self, cell):
        r = cell // 27
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
                if self.board[i] and len(self.possible[i]) == 1:
                    self.board[i] = self.possible[i].pop()
                    self.find_possible()
                    done = False

    def solve(self, multiple_solutions = False):
        pass



def random_board():
    board = [0 for _ in range(81)]
    potential = [{i + 1 for i in range(9)} for j in range(81)]
    while not solved(board, potential):
        i = board.index(0)
        board[i] = rand.choice(tuple(potential[i]))
        board, potential = fill(board, potential)
    return board, potential


def row(board, x):
    return board[x * 9 : x * 9 + 9]


def col(board, y):
    return board[y:81:9]


def block(board, n):
    r = (n // 3) * 27
    c = (n % 3) * 3
    return [
        *board[c + r : c + r + 3],
        *board[c + r + 9 : c + r + 12],
        *board[c + r + 18 : c + r + 21],
    ]


def fill(board, potential):
    newboard, newpot = list(board), list(potential)
    done = False
    while not done:
        done = True
        for i in range(81):
            if newboard[i] == 0:
                newpot[i] = set(newpot[i]) - set(
                    row(newboard, i // 9)
                    + col(newboard, i % 9)
                    + block(newboard, i // 27 * 3 + i % 9 // 3)
                )
            else:
                newpot[i] = set([])
            if len(newpot[i]) == 1:
                newboard[i] = newpot[i].pop()
                done = False
    return (newboard, newpot)


def valid_board(board, potential):
    rv = False
    for i in range(81):
        rv = True
        if board[i] == 0:
            if len(potential[i]) < 2:
                rv = False
                break
            else:
                continue

        if (
            (row(board, i // 9).count(board[i]) > 1)
            or (col(board, i % 9).count(board[i]) > 1)
            or (block(board, i // 27 + i % 9 // 3).count(board[i]) > 1)
        ):
            rv = False
            break

    return rv


def solved(board, potential):
    return valid_board(board, potential) and board.count(0) == 0


def solve(board, potential):
    (newboard, newpot) = fill(board, potential)
    if solved(newboard, newpot):
        return newboard, newpot, True
    else:
        s = False
        while not s:
            i = newboard.index(0)
            if len(newpot[i]) == 0:
                return board, potential, False
            newboard[i] = newpot[i].pop()
            (newboard, newpot, s) = solve(list(newboard), list(newpot))
        return newboard, newpot, s


b, p = random_board()

print(b)
