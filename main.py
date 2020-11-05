from tkinter import Tk

from board import *
from team import *
import const


board = Board(
    data_file='initial_board.data',
    teams=[Team(color) for color in const.COLORS],
)

window = Tk()
board.render(window)

window.mainloop()
