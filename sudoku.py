import random as rnd
import copy


class Grid:
    def __init__(self, board=None):
        if board is not None and len(board) != 81:
            raise ValueError(
                f"A sudoku grid must contain 81 cells. The supplied grid contains {len(board)} cells."
            )
        self.board = board[:] if board else [0 for _ in range(81)]
        self.original = self.board[:]
        self.find_possible()

    def __repr__(self):
        return self.board

    def __str__(self):
        return str(self.board)

    # Given a cell on the board, return the row which contains that cell.
    def row(self, cell):
        c = cell // 9
        return self.board[c * 9 : c * 9 + 9]

    # Given a cell on the board, return the column which contains that cell.
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


def solve(grid, multiple_solutions=False):
    solutions = []
    board_stack = []
    solved = 0
    s = 2 if multiple_solutions else 1
    while solved < s:
        if 0 in grid.board:
            # improve the efficiency of backtracking by starting from the cells with the fewest posible options.
            m = min(p for p in grid.possible if len(p) > 0)
            i = grid.possible.index(m)
            board_stack.append(
                {
                    "brd": grid.board[:],
                    "index": i,
                    "value": min(grid.possible[i]),
                    "pos": copy.deepcopy(grid.possible),
                }
            )
            grid.board[i] = min(grid.possible[i])
            grid.find_possible()
            fill_board(grid)

        if grid.is_valid() and grid.board not in solutions:
            if grid.board.count(0) == 0:
                solved += 1

                solutions.append(grid.board[:])

        else:
            if not board_stack:
                break
            else:
                while True:
                    t = board_stack.pop()
                    grid.board = t["brd"]
                    grid.possible = t["pos"]
                    grid.possible[t["index"]].remove(t["value"])
                    if len(grid.possible[t["index"]]) > 0 or not board_stack:
                        break
        if not board_stack and 0 in grid.board:
            break
    return (solutions, grid)


def fill_board(grid):
    done = False
    while not done:
        done = True
        for i in range(81):
            if grid.board[i] == 0 and len(grid.possible[i]) == 1:
                grid.board[i] = grid.possible[i].pop()
                grid.find_possible()
                done = False
    return grid


def generate_random_board():
    grid = Grid()
    complete = False
    while not complete:
        i = grid.board.index(0)
        grid.board[i] = rnd.choice(list(grid.possible[i]))
        grid.find_possible()
        grid = fill_board(grid)
        if not grid.is_valid():
            grid = Grid()
        else:
            if grid.board.count(0) == 0:
                complete = True
    return grid


def make_playable(grid, dificulty):
    difs = [15, 22, 33, 49, 70]
    # I'm using number of missing values as a proxy for dificulty for now. May look into adding a 
    # better dificulty heuristic in the future.
    original = grid.board[:]
    r = rnd.sample(range(81), difs[dificulty])
    for i in r:
        grid.board[i] = 0
    grid.find_possible()
    unsolved = grid.board[:]
    valid = False
    while not valid:
        solutions, _ = solve(grid, True)
        if len(solutions) == 1:
            valid = True
        else:
            i = rnd.choice(r)
            unsolved[i] = original[i]
            r.remove(i)
            grid.board = unsolved[:]
            grid.find_possible()
    
    return ([original], Grid(unsolved))
