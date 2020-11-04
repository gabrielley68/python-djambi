from tkinter import Button, PhotoImage
import sys
from PIL import Image, ImageTk

from peons import peon_factory
import const


class BoardCell:
    def __init__(self, initial_peon=None):
        self.peons = (initial_peon, None)
        self.image_cache = {}

    def render(self, master):
        """
        return a tkinter representation of the cell
        :param master:
        :return: tkinter.Button
        """
        # images must stayed in memory to be displayed by tkinter so keep a reference in the class
        if self.peons[0] and type(self.peons[0]) not in self.image_cache:
            image = Image.open(self.peons[0].image_path())
            image = image.resize((const.CELL_WIDTH_PIXEL, const.CELL_HEIGHT_PIXEL))
            image = ImageTk.PhotoImage(image)
            self.image_cache[type(self.peons[0])] = image
        image = self.image_cache[type(self.peons[0])] if self.peons[0] else None
        button = Button(
            master,
            bg=const.COLORS_HEX[self.peons[0].color] if self.peons[0] else '#D3D3D3',
            image=image,
            # use pixel size for images, font size for empty cells
            width=const.CELL_WIDTH_PIXEL if image else const.CELL_WIDTH_TEXT,
            height=const.CELL_HEIGHT_PIXEL if image else const.CELL_HEIGHT_TEXT,
        )
        return button


class Board:
    def __init__(self):
        self.cells = []
        with open('initial_board.data') as initial_board:
            # Read initial_board and iterate on each line
            for row_idx, row_data in enumerate([row.rstrip('\n') for row in initial_board]):
                self.cells.append(list())
                for col_idx, col_data in enumerate(row_data.split()):
                    try:
                        peon, color = col_data.split("_")
                    except ValueError:
                        print("Error parsing initial_board.data, please verify format", file=sys.stderr)
                    if peon and color:
                        # Add peon according to their type
                        self.cells[row_idx].append(BoardCell(peon_factory(
                            board=self,
                            peon_type=peon,
                            color=color,
                            position=(row_idx, col_idx)
                        )))
                    else:
                        # Add an empty cell
                        self.cells[row_idx].append(BoardCell(None))

    def move(self, departure, arrival):
        pass
