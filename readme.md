Sudoku game written in Python

To use, run sudoku-gui.py. Each time it is launched, a randomly generated 
puzzle will be shown. There are 5 dificulty levels.

How to play:
Empty squares show available numbers, with numbers which don't conflict with 
the starting board slightly darker. Right click one of these numbers to select 
that value for the cell. Left click to toggle between the light and darker 
color. Right click a cell you have already set the value for to go back to the 
view of the small numbers, with highlighting updated to reflect the current 
board state.

Use the reset button to reset the board to it's starting configuration. Use the
New button to create a new board at the selected dificulty. Use the dificulty 
selector to change the dificulty level.

Still to do:
Add a way to check your answers.
Add an indicator when the board is correctly filled out.
Improve heuristics for dificulty levels.
