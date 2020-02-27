import random


board = [
    7,
    8,
    0,
    4,
    0,
    0,
    1,
    2,
    0,
    6,
    0,
    0,
    0,
    7,
    5,
    0,
    0,
    9,
    0,
    0,
    0,
    6,
    0,
    1,
    0,
    7,
    8,
    0,
    0,
    7,
    0,
    4,
    0,
    2,
    6,
    0,
    0,
    0,
    1,
    0,
    5,
    0,
    9,
    3,
    0,
    9,
    0,
    4,
    0,
    6,
    0,
    0,
    0,
    5,
    0,
    7,
    0,
    3,
    0,
    0,
    0,
    1,
    2,
    1,
    2,
    0,
    0,
    0,
    7,
    4,
    0,
    0,
    0,
    4,
    9,
    2,
    0,
    6,
    0,
    0,
    7,
]

potential = [{i + 1 for i in range(9)} for j in range(81)]


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


def reduce_(board, potential):
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
    (newboard, newpot) = reduce_(board, potential)
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


