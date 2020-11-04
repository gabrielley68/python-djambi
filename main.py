from tkinter import Tk

from board import *
from team import *
import const


teams = [Team(color) for color in const.COLORS]
board = Board()

window = Tk()

for row_idx, row in enumerate(board.cells):
    for col_idx, cell in enumerate(row):
        cell.render(window).grid(row=row_idx, column=col_idx)

window.mainloop()
