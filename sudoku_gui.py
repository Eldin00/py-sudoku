import pygame
import sudoku
import sys
from pygame.locals import *

GRIDSIZE = 81
GRIDSIZEMULT = 6
WINHEIGHT = GRIDSIZE * GRIDSIZEMULT
GRIDWIDTH = GRIDSIZE * GRIDSIZEMULT
WINWIDTH = GRIDWIDTH + 150
BLOCKSIZE = GRIDSIZE * GRIDSIZEMULT // 3
CELLSIZE = BLOCKSIZE // 3
NUMSUBSIZE = CELLSIZE // 3
FPS = 15

RESETBUTTONPOSX = GRIDWIDTH + 20
RESETBUTTONPOSY = 20
RESETBUTTONHEIGHT = 30
RESETBUTTONWIDTH = 100

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LTGREY = (180, 180, 180)
DKGREY = (75, 75, 75)
BLUE = (0, 0, 200)
LTBLUEGREY = (220, 220, 250)


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, BASICFONTSIZE, LARGEFONT, LARGEFONTSIZE
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINWIDTH, WINHEIGHT))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    pygame.display.set_caption("Sudoku")

    BASICFONTSIZE = 15
    BASICFONT = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)
    LARGEFONTSIZE = 55
    LARGEFONT = pygame.font.Font("freesansbold.ttf", LARGEFONTSIZE)
    DISPLAYSURF.fill(WHITE)
    reset_button_pressed = False

    drawgrid()
    drawbutton(
        RESETBUTTONPOSX,
        RESETBUTTONPOSY,
        RESETBUTTONHEIGHT,
        RESETBUTTONWIDTH,
        "Reset",
        reset_button_pressed,
    )
    solution, grid = sudoku.make_playable(sudoku.generate_random_board(), 2)
    original_grid = grid.board[:]

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
                if mousebutton == pygame.BUTTON_RIGHT and mousex < GRIDWIDTH:
                    grid = togglesubcell(mousex, mousey, grid)
                elif mousebutton == pygame.BUTTON_LEFT:
                    if mousex < GRIDWIDTH:
                        grid = togglecell(mousex, mousey, grid)
                    elif (
                        RESETBUTTONPOSX + 5
                        < mousex
                        < RESETBUTTONPOSX + RESETBUTTONWIDTH
                        and RESETBUTTONPOSY
                        < mousey
                        < RESETBUTTONPOSY + RESETBUTTONHEIGHT
                    ):
                        grid = sudoku.Grid(original_grid)

            if pygame.mouse.get_pressed()[0]:
                if (
                    RESETBUTTONPOSX + 5 < mousex < RESETBUTTONPOSX + RESETBUTTONWIDTH
                    and RESETBUTTONPOSY < mousey < RESETBUTTONPOSY + RESETBUTTONHEIGHT
                ):
                    reset_button_pressed = True
                else:
                    reset_button_pressed = False
            else:
                reset_button_pressed = False

            DISPLAYSURF.fill(WHITE)
            drawgrid()
            drawbutton(
                RESETBUTTONPOSX,
                RESETBUTTONPOSY,
                RESETBUTTONHEIGHT,
                RESETBUTTONWIDTH,
                "Reset",
                reset_button_pressed,
            )
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
                DISPLAYSURF, LTGREY, (0, i * CELLSIZE), (GRIDWIDTH, i * CELLSIZE)
            )
        else:
            pygame.draw.line(
                DISPLAYSURF, BLACK, (i * CELLSIZE, 0), (i * CELLSIZE, WINHEIGHT)
            )
            pygame.draw.line(
                DISPLAYSURF, BLACK, (0, i * CELLSIZE), (GRIDWIDTH, i * CELLSIZE)
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
    x = mousex * 9 // GRIDWIDTH
    y = mousey * 9 // WINHEIGHT
    cell = x + y * 9
    if grid.original[cell]:
        return grid
    xsub = (mousex * 27) // GRIDWIDTH
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
    x = mousex * 9 // GRIDWIDTH
    y = mousey * 9 // WINHEIGHT
    xsub = (mousex * 27) // GRIDWIDTH
    ysub = (mousey * 27) // WINHEIGHT
    cell = x + y * 9
    if grid.board[cell]:
        return grid

    xsub = (mousex * 27) // GRIDWIDTH
    ysub = (mousey * 27) // WINHEIGHT
    value = (xsub % 3) + (3 * (ysub % 3)) + 1

    if value in grid.possible[cell]:
        grid.possible[cell].remove(value)
    else:
        grid.possible[cell].add(value)
    return grid


def drawbox(mousex, mousey):
    boxx = ((mousex * 27) // GRIDWIDTH) * (NUMSUBSIZE)
    boxy = ((mousey * 27) // WINHEIGHT) * (NUMSUBSIZE)
    if boxx < GRIDWIDTH:
        pygame.draw.rect(DISPLAYSURF, BLUE, (boxx, boxy, NUMSUBSIZE, NUMSUBSIZE), 1)


def drawbutton(posx, posy, height, width, text, pressed):
    BUTTONFONT = pygame.font.Font("freesansbold.ttf", int(height * 0.8))
    cellsurf = BUTTONFONT.render("%s" % text, True, BLACK)
    cellrect = cellsurf.get_rect()
    if not pressed:
        pygame.draw.rect(DISPLAYSURF, DKGREY, (posx, posy + 5, width - 5, height), 0)
        pygame.draw.rect(DISPLAYSURF, WHITE, (posx + 5, posy, width, height), 0)
        pygame.draw.rect(DISPLAYSURF, BLACK, (posx + 5, posy, width, height), 1)
        cellrect.topleft = (
            posx + 5 + (width - cellsurf.get_width()) // 2,
            posy + (height - cellsurf.get_height()) // 2,
        )
    else:
        pygame.draw.rect(DISPLAYSURF, WHITE, (posx, posy + 5, width - 5, height), 0)
        pygame.draw.rect(DISPLAYSURF, BLACK, (posx, posy + 5, width - 5, height), 1)
        cellrect.topleft = (
            posx + (width - cellsurf.get_width()) // 2,
            posy + 5 + (height - cellsurf.get_height()) // 2,
        )
    DISPLAYSURF.blit(cellsurf, cellrect)


if __name__ == "__main__":
    main()
