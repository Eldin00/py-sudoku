import pygame
import sudoku
import sys
from pygame.locals import *


# Constants that we need for drawing the grid and numbers.
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
NEWBUTTONPOSX = GRIDWIDTH + 20
NEWBUTTONPOSY = 60
NEWBUTTONHEIGHT = 30
NEWBUTTONWIDTH = 100

DIFMINUSPOSX = GRIDWIDTH + 25
DIFMINUSWIDTH = 30
DIFVALUEPOSX = DIFMINUSPOSX + DIFMINUSWIDTH
DIFVALUEWIDTH = 30
DIFPLUSPOSX = DIFVALUEPOSX + DIFVALUEWIDTH
DIFPLUSWIDTH = 30
DIFPOSY = 130
DIFHEIGHT = 30


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LTGREY = (180, 180, 180)
DKGREY = (75, 75, 75)
BLUE = (0, 0, 200)
LTBLUEGREY = (220, 220, 250)
MIDBLUEGREY = (100, 100, 180)
DKBLUEGREY = (50, 50, 120)
GREEN = (0, 200, 0)

def main():
    """
    main()
    Begin by setting up the board, then enter the main game loop.
    """
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
    dificulty = 2

    reset_button_pressed = False
    new_button_pressed = False
    minus_pressed = False
    plus_pressed = False

    draw_grid()
    draw_button(
        RESETBUTTONPOSX,
        RESETBUTTONPOSY,
        RESETBUTTONHEIGHT,
        RESETBUTTONWIDTH,
        "Reset",
        reset_button_pressed,
    )

    draw_button(
        NEWBUTTONPOSX,
        NEWBUTTONPOSY,
        NEWBUTTONHEIGHT,
        NEWBUTTONWIDTH,
        "New",
        new_button_pressed,
    )

    draw_dif_control(dificulty, minus_pressed, plus_pressed)

    solution, grid = sudoku.make_playable(sudoku.generate_random_board(), dificulty)
    original_grid = grid.board[:]

    draw_cells(grid, False)
    mousex = 999999999
    mousey = 999999999

    while True:  # main game loop
        winner = (grid.board == solution)
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
                    grid = toggle_subcell(mousex, mousey, grid)
                elif mousebutton == pygame.BUTTON_LEFT:
                    if mousex < GRIDWIDTH:
                        grid = toggle_cell(mousex, mousey, grid)
                    elif (
                        RESETBUTTONPOSX + 5
                        < mousex
                        < RESETBUTTONPOSX + RESETBUTTONWIDTH
                        and RESETBUTTONPOSY
                        < mousey
                        < RESETBUTTONPOSY + RESETBUTTONHEIGHT
                    ):
                        grid = sudoku.Grid(original_grid)
                    elif (
                        NEWBUTTONPOSX + 5 < mousex < NEWBUTTONPOSX + NEWBUTTONWIDTH
                        and NEWBUTTONPOSY < mousey < NEWBUTTONPOSY + NEWBUTTONHEIGHT
                    ):
                        solution, grid = sudoku.make_playable(
                            sudoku.generate_random_board(), dificulty
                        )
                        original_grid = grid.board[:]
                    elif (
                        DIFMINUSPOSX  < mousex < DIFMINUSPOSX + DIFMINUSWIDTH
                        and DIFPOSY < mousey < DIFPOSY + DIFHEIGHT 
                        and dificulty > 0
                    ):
                        dificulty -= 1
                    elif (
                        DIFPLUSPOSX  < mousex < DIFPLUSPOSX + DIFPLUSWIDTH
                        and DIFPOSY < mousey < DIFPOSY + DIFHEIGHT 
                        and dificulty < 4
                    ):
                        dificulty += 1

            if pygame.mouse.get_pressed()[0]:
                if (
                    RESETBUTTONPOSX + 5 < mousex < RESETBUTTONPOSX + RESETBUTTONWIDTH
                    and RESETBUTTONPOSY < mousey < RESETBUTTONPOSY + RESETBUTTONHEIGHT
                ):
                    reset_button_pressed = True
                else:
                    reset_button_pressed = False

                if (
                    NEWBUTTONPOSX + 5 < mousex < NEWBUTTONPOSX + NEWBUTTONWIDTH
                    and NEWBUTTONPOSY < mousey < NEWBUTTONPOSY + NEWBUTTONHEIGHT
                ):
                    new_button_pressed = True
                else:
                    new_button_pressed = False

                if (
                    DIFMINUSPOSX < mousex < DIFMINUSPOSX + DIFMINUSWIDTH
                    and DIFPOSY < mousey < DIFPOSY + DIFHEIGHT
                ):
                    minus_pressed = True
                else:
                    minus_pressed = False

                if (
                    DIFPLUSPOSX < mousex < DIFPLUSPOSX + DIFPLUSWIDTH
                    and DIFPOSY < mousey < DIFPOSY + DIFHEIGHT
                ):
                    plus_pressed = True
                else:
                    plus_pressed = False

            else:
                reset_button_pressed = False
                new_button_pressed = False
                minus_pressed = False
                plus_pressed = False

            DISPLAYSURF.fill(WHITE)
            draw_grid()
            draw_button(
                RESETBUTTONPOSX,
                RESETBUTTONPOSY,
                RESETBUTTONHEIGHT,
                RESETBUTTONWIDTH,
                "Reset",
                reset_button_pressed,
            )

            draw_button(
                NEWBUTTONPOSX,
                NEWBUTTONPOSY,
                NEWBUTTONHEIGHT,
                NEWBUTTONWIDTH,
                "New",
                new_button_pressed,
            )

            draw_dif_control(dificulty, minus_pressed, plus_pressed)

            draw_cells(grid, winner)
            draw_box(mousex, mousey)



        pygame.display.update()
   


def draw_grid():
    """
    drawgrid()
    Draws the 3x3 grid of lines on the board, including the seperator between the grid and the button area.
    """
    for i in range(1, 10):
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


def draw_cells(grid: sudoku.Grid, winner: bool):
    """
    drawcells(grid: sudoku.Grid)
    Draws numbers on the board based on the values of cells in the Grid.

    Parameters:
        grid : A Grid object.
    """
    for i in range(81):
        if grid.board[i] == 0:
            for j in range(1, 10):
                if winner:
                    color = GREEN
                elif j in grid.possible[i]:
                    color = DKBLUEGREY
                else:
                    color = LTGREY
                populate_subcells(
                    j,
                    (i % 9 * CELLSIZE) + ((j - 1) % 3 * NUMSUBSIZE) + 2,
                    (i // 9 * CELLSIZE) + ((j - 1) // 3 * NUMSUBSIZE) + 1,
                    color,
                )
        else:
            if winner:
                color = GREEN
            elif grid.original[i]:
                color = BLACK
            else:
                color = MIDBLUEGREY
            populate_cells(
                grid.board[i], (i % 9 * CELLSIZE) + 10, (i // 9 * CELLSIZE), color
            )


def populate_cells(celldata, x, y, color):
    """
    populatecells(celldata,x,y,color)
    Draws the number the cell is set to in the cell.

    Parameters are:
        celldata : A number 1-9 to draw in the cell.
        x, y : Coordinates of the upper left hand corner of the cell.
        color : The color to use when drawing the number.
    """
    cellsurf = LARGEFONT.render("%s" % (celldata), True, color)
    cellrect = cellsurf.get_rect()
    cellrect.topleft = (x, y)
    DISPLAYSURF.blit(cellsurf, cellrect)


def populate_subcells(celldata, x, y, color):
    """
    populatesubcells(celldata,x,y,color)
    Draws a number in a sub-cell. Each cell has 9 sub-cells aranged in a 3x3 grid.

    Parameters are:
        celldata : A number 1-9 to draw in the subcell.
        x, y : Coordinates of the upper left hand corner of the subcell.
        color : The color to use when drawing the number.
    """
    cellsurf = BASICFONT.render("%s" % (celldata), True, color)
    cellrect = cellsurf.get_rect()
    cellrect.topleft = (x, y)
    DISPLAYSURF.blit(cellsurf, cellrect)


def toggle_cell(mousex, mousey, grid):
    """
    togglecell(mousex, mousey, grid)
    Sets the value of a cell based the mouse location, and whether or not the cell under the mouse is
    currently set. If the cell is not currently set, it is changed based on which subgrid the mouse is
    over. Otherwise, if the cell is currently set, it un-sets it.

    Returns a grid which is updated to reflect the change.

    Parameters:
        mousex : x coordinate of mouse cursor
        mousey : y coordinate of mouse cursor
        grid : a Grid object which corresponds to the current board state.
    """
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


def toggle_subcell(mousex, mousey, grid):
    """
    togglesubcell(mousex, mousey, grid)
    Colors the number in a sub-cell based the mouse location, and whether or not the sub-cell under the
    mouse correlates to a possible value of for the containing cell. If the number of the sub-cell is
    currently a posibility, change it to the lighter color. If it is not, change it to the darker
    color. Update the Grid accordingly.

    Returns the updated Grid.

    Parameters:
        mousex : The x coordinate of mouse cursor
        mousey : The y coordinate of mouse cursor
        grid : A Grid object which corresponds to the current board state.
    """
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


def draw_box(mousex, mousey):
    """
    drawbox(mousex, mousey)
    Draws a box around the sub-cell under the mouse.

    Parameters:
        mousex : The x coordinate of the mouse.
        mousey : The y coordinate of the mouse.
    """
    boxx = ((mousex * 27) // GRIDWIDTH) * (NUMSUBSIZE)
    boxy = ((mousey * 27) // WINHEIGHT) * (NUMSUBSIZE)
    if boxx < GRIDWIDTH:
        pygame.draw.rect(DISPLAYSURF, BLUE, (boxx, boxy, NUMSUBSIZE, NUMSUBSIZE), 1)


def draw_button(posx, posy, height, width, text, pressed):
    """
    drawbutton(posx, posy, height, width, text, pressed)
    Draws a button with text.

    Parameters:
        posx, posy : Coordinates of the upper left hand corner of the button.
        height : The height of the button.
        width : The width of the button in pixels.
        text : Text to display on the button in pixels.
        pressed : A boolean indicating whether or not the button is pressed.
    """
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

def draw_dif_control(dificulty, minuspressed, pluspressed):
    """ 
    drawdifcontrol(dificulty, minuspressed, pluspressed)
    Draws the dificulty selector control.

    Parameters: 
    dificulty : An integer representing the currently selected dificulty.
    minuspressed : A boolean indicating whether or not the '-' portion of the control is pressed.
    pluspressed : A boolean indicatinh whether or not the '+' portion of the control is pressed.
    """
    CTLFONT = pygame.font.Font("freesansbold.ttf", int(DIFHEIGHT * 0.8))
    minus = CTLFONT.render("-", True, BLACK)
    plus = CTLFONT.render("+", True, BLACK)
    dif = CTLFONT.render("%s" % (dificulty + 1), True, BLACK)
    minusrect = minus.get_rect()
    plusrect = plus.get_rect()
    difrect = dif.get_rect()
    minusrect.topleft = (DIFMINUSPOSX + (DIFMINUSWIDTH - minus.get_width()) // 2,
                         DIFPOSY + (DIFHEIGHT - minus.get_height()) // 2,)
    plusrect.topleft = (DIFPLUSPOSX + (DIFPLUSWIDTH - plus.get_width()) // 2,
                         DIFPOSY + (DIFHEIGHT - plus.get_height()) // 2,)
    difrect.topleft = (DIFVALUEPOSX + (DIFVALUEWIDTH - dif.get_width()) // 2,
                         DIFPOSY + (DIFHEIGHT - dif.get_height()) // 2,)

    minuscolor = LTGREY if minuspressed else WHITE
    pluscolor = LTGREY if pluspressed else WHITE
    pygame.draw.rect(DISPLAYSURF, minuscolor, (DIFMINUSPOSX,DIFPOSY,DIFMINUSWIDTH,DIFHEIGHT),0)
    pygame.draw.rect(DISPLAYSURF, BLACK, (DIFMINUSPOSX,DIFPOSY,DIFMINUSWIDTH,DIFHEIGHT),1)
    pygame.draw.rect(DISPLAYSURF, WHITE, (DIFVALUEPOSX,DIFPOSY,DIFVALUEWIDTH,DIFHEIGHT),0)
    pygame.draw.rect(DISPLAYSURF, BLACK, (DIFVALUEPOSX,DIFPOSY,DIFVALUEWIDTH,DIFHEIGHT),1)
    pygame.draw.rect(DISPLAYSURF, pluscolor, (DIFPLUSPOSX,DIFPOSY,DIFPLUSWIDTH,DIFHEIGHT),0)
    pygame.draw.rect(DISPLAYSURF, BLACK, (DIFPLUSPOSX,DIFPOSY,DIFPLUSWIDTH,DIFHEIGHT),1)
    DISPLAYSURF.blit(minus, minusrect)
    DISPLAYSURF.blit(dif, difrect)
    DISPLAYSURF.blit(plus, plusrect)


if __name__ == "__main__":
    main()
