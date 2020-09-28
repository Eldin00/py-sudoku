import random as rnd
import copy


class Grid: 
#The Grid object contains a representation of a sudoku board, along with methods to access a 
#particular row, column, or 3x3 block from the board. Also includes a method to ensure that a board
#contains no contridictions, and a method to determine what values could go in empty cells without 
#creating a contridiction. 

    def __init__(self, board=None):
        """
        __init__(self, board=None)
        Initializes a Grid object. If a board is supplied, it validates the length of the board, and 
        if valid, sets the values in Grid.board accordingly. If no board is supplied, it populates 
        Grid.board with zeros, corresponding to a blank board. It also computes what values could go
        into any blank cell without creating a contridiction.

        Parameters:
            board : A list of integers 0-9 representing a sudoku board. Defaults to None.
        """
        if board is not None and len(board) != 81:
            raise ValueError(
                f"A sudoku grid must contain 81 cells. The supplied grid contains {len(board)} cells."
            )
        self.board = board[:] if board else [0 for _ in range(81)]
        self.original = self.board[:]
        self.find_possible()

    def __repr__(self):
        """
        __repr__(self)
        Returns a list of integers 0-9 representing the current state of the board.
        """
        return self.board

    def __str__(self):
        """
        __str__(self)
        Returns a string representation of the current state of the board.
        """
        return str(self.board)


    def row(self, cell):
        """
        row(self, cell)
        Given a cell on the board, return a list representing the row on the board which contains that
        cell.

        Parameters:
            cell : A number 0-80 representing a cell on the board
        """
        c = cell // 9
        return self.board[c * 9 : c * 9 + 9]

    # Given a cell on the board, return the column which contains that cell.
    def col(self, cell):
        """
        col(self, cell)
        Given a cell on the board, return a list representing the column on the board which contains 
        that cell.

        Parameters:
            cell : A number 0-80 representing a cell on the board
        """
        return self.board[cell % 9 : 81 : 9]

    def block(self, cell):
        """
        block(self, cell)
        Given a cell on the board, return a list representing the 3x3 block on the board which contains 
        that cell.

        Parameters:
            cell : A number 0-80 representing a cell on the board
        """
        r = cell // 27 * 27
        c = cell % 9 // 3 * 3
        return [
            *self.board[r + c : r + c + 3],
            *self.board[r + c + 9 : r + c + 12],
            *self.board[r + c + 18 : r + c + 21],
        ]

    def find_possible(self):
        """
        find_possible(self)
        Based on the current state of the board, determine what values could go in any blank cell
        without creating a contradiction
        """
        possible = [{} for _ in range(81)]
        for i in range(81):
            if self.board[i] == 0:
                possible[i] = set(range(1, 10)) - set(self.row(i)).union(
                    set(self.col(i)), set(self.block(i))
                )
        self.possible = possible

    def is_valid(self):
        """
        Returns true if every blank cell has at least one possible value, and populated cells contain
        no contradictions. Otherwise returns false.
        """
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
    """
    solve(grid, multiple_solutions=False)
    Finds a solution to a sudoku board. Optionally finds a second soluton if one exists, for the purpose
    of verifying that the board has a unique solution.

    Parameters:
        grid : A Grid object representing the sudoku board to be solved.
        multiple_solutions : A boolean indicating whether or not to keep going after finding one
                            solution. Defaults to False.
    """
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
    """
    fill_board(grid)
    Given a sudoku board, aply the heuristic of repeatedly filling in any cell which has only 
    one possible value, then recomputing the possible values for empty cells.

    Parameters:
        grid : A Grid object representing the sudoku board to attempt to fill values for.
    """
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
    """
    generate_random_board()
    Generate a valid, randomly filled, solved sudoku board.
    """
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
    """
    make_playable(gird, dificulty)
    Take a solved sudoku board, blank out cells to create a valid board for the player to solve.

    Parameters:
        grid : A Grid object representing a solved sudoku board.
        dificulty : an integer from 0-4 representing the dificulty of the resulting playable board.
                    Higher numbers will try to blank out more cells.
    """
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
