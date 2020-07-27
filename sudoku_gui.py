import pygame
import sudoku
from pygame.locals import *

WINSIZE = 81
WINSIZEMULT = 6
WINHEIGHT = WINSIZE * WINSIZEMULT
WINWIDTH = WINSIZE * WINSIZEMULT
BLOCKSIZE = WINSIZE * WINSIZEMULT // 3
CELLSIZE = BLOCKSIZE // 3
NUMSUBSIZE = CELLSIZE // 3
FPS = 15


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LTGREY = (180, 180, 180)
DKGREY = (75, 75, 75)
BLUE = (0, 0, 200)
LTBLUEGREY = (220, 220, 250)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BASICFONTSIZE, LARGEFONT, LARGEFONTSIZE
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINHEIGHT, WINWIDTH))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    pygame.display.set_caption("Sudoku")

    BASICFONTSIZE = 15
    BASICFONT = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)
    LARGEFONTSIZE = 55
    LARGEFONT = pygame.font.Font("freesansbold.ttf", LARGEFONTSIZE)
    DISPLAYSURF.fill(WHITE)
    drawgrid()
    grid = sudoku.make_playable(sudoku.generate_random_board(), 2)
    drawcells(grid)
    mousex = 999999999
    mousey = 999999999

    while True:  # main game loop
        mouseclicked = False
        mousebutton = 0
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # mouse movement commands
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            # Mouse click commands
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseclicked = True
                mousebutton = event.button

            if mouseclicked:
                if mousebutton == pygame.BUTTON_RIGHT:
                    grid = togglesubcell(mousex, mousey, grid)
                elif mousebutton == pygame.BUTTON_LEFT:
                    grid = togglecell(mousex, mousey, grid)

            DISPLAYSURF.fill(WHITE)
            drawgrid()
            drawcells(grid)
            drawbox(mousex, mousey)

        pygame.display.update()


def drawgrid():
    for i in range(1, 9):
        if i % 3:
            pygame.draw.line(
                DISPLAYSURF, LTGREY, (i * CELLSIZE, 0), (i * CELLSIZE, WINHEIGHT)
            )
            pygame.draw.line(
                DISPLAYSURF, LTGREY, (0, i * CELLSIZE), (WINHEIGHT, i * CELLSIZE)
            )
        else:
            pygame.draw.line(
                DISPLAYSURF, BLACK, (i * CELLSIZE, 0), (i * CELLSIZE, WINHEIGHT)
            )
            pygame.draw.line(
                DISPLAYSURF, BLACK, (0, i * CELLSIZE), (WINHEIGHT, i * CELLSIZE)
            )


def drawcells(grid: sudoku.Grid):
    for i in range(81):
        if grid.board[i] == 0:
            for j in range(1, 10):
                color = LTGREY if j in grid.possible[i] else LTBLUEGREY
                populatesubcells(
                    j,
                    (i % 9 * CELLSIZE) + ((j - 1) % 3 * NUMSUBSIZE) + 2,
                    (i // 9 * CELLSIZE) + ((j - 1) // 3 * NUMSUBSIZE) + 1,
                    color,
                )
        else:
            color = BLACK if grid.original[i] else DKGREY
            populatecells(
                grid.board[i], (i % 9 * CELLSIZE) + 10, (i // 9 * CELLSIZE), color
            )


def populatecells(celldata, x, y, color):
    cellsurf = LARGEFONT.render("%s" % (celldata), True, color)
    cellrect = cellsurf.get_rect()
    cellrect.topleft = (x, y)
    DISPLAYSURF.blit(cellsurf, cellrect)


def populatesubcells(celldata, x, y, color):
    cellsurf = BASICFONT.render("%s" % (celldata), True, color)
    cellrect = cellsurf.get_rect()
    cellrect.topleft = (x, y)
    DISPLAYSURF.blit(cellsurf, cellrect)


def togglecell(mousex, mousey, grid):
    x = mousex * 9 // WINWIDTH
    y = mousey * 9 // WINHEIGHT
    cell = x + y * 9
    if grid.original[cell]:
        return grid
    xsub = (mousex * 27) // WINWIDTH
    ysub = (mousey * 27) // WINHEIGHT
    value = (xsub % 3) + (3 * (ysub % 3)) + 1
    if grid.board[cell] == 0:
        grid.board[cell] = value
        grid.possible[cell] = set()
    else:
        grid.board[cell] = 0
        grid.possible[cell] = sudoku.Grid(grid.board).possible[cell]
    return grid


def togglesubcell(mousex, mousey, grid):
    x = mousex * 9 // WINWIDTH
    y = mousey * 9 // WINHEIGHT
    xsub = (mousex * 27) // WINWIDTH
    ysub = (mousey * 27) // WINHEIGHT
    cell = x + y * 9
    if grid.board[cell]:
        return grid

    xsub = (mousex * 27) // WINWIDTH
    ysub = (mousey * 27) // WINHEIGHT
    value = (xsub % 3) + (3 * (ysub % 3)) + 1

    if value in grid.possible[cell]:
        grid.possible[cell].remove(value)
    else:
        grid.possible[cell].add(value)
    return grid


def drawbox(mousex, mousey):
    boxx = ((mousex * 27) // WINWIDTH) * (NUMSUBSIZE)
    boxy = ((mousey * 27) // WINHEIGHT) * (NUMSUBSIZE)
    pygame.draw.rect(DISPLAYSURF, BLUE, (boxx, boxy, NUMSUBSIZE, NUMSUBSIZE), 1)


if __name__ == "__main__":
    main()
