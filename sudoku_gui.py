import pygame
import sys
import sudoku
from pygame.locals import *

WINSIZE = 81
WINSIZEMULT = 6
WINHEIGHT = WINSIZE * WINSIZEMULT
WINWIDTH = WINSIZE * WINSIZEMULT
BLOCKSIZE = WINSIZE * WINSIZEMULT / 3
CELLSIZE = BLOCKSIZE / 3
NUMSUBSIZE = CELLSIZE / 3
FPS = 15


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LTGREY = (200, 200, 200)


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode((WINHEIGHT, WINWIDTH))
    FPSCLOCK = pygame.time.Clock()
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    pygame.display.set_caption("Sudoku")
    global BASICFONT, BASICFONTSIZE
    BASICFONTSIZE = 15
    BASICFONT = pygame.font.Font("freesansbold.ttf", BASICFONTSIZE)

    DISPLAYSURF.fill(WHITE)
    drawgrid()
    drawcells(sudoku.Grid())
    while True:  # main game loop
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
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
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    for i in range(81):
        for j in grid.possible[i]:
            popcells(
                j,
                (i // 9 * CELLSIZE) + ((j - 1) % 3 * NUMSUBSIZE) + 2,
                (i % 9 * CELLSIZE) + ((j - 1) // 3 * NUMSUBSIZE) + 1,
            )


def popcells(celldata, x, y):
    cellSurf = BASICFONT.render("%s" % (celldata), True, LTGREY)
    cellRect = cellSurf.get_rect()
    cellRect.topleft = (x, y)
    DISPLAYSURF.blit(cellSurf, cellRect)


if __name__ == "__main__":
    main()
