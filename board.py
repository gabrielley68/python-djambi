from tkinter import Button, Label
import sys
from PIL import Image, ImageTk

from peons import peon_factory
import const
from team import Team


class BoardCell:
    def __init__(self, initial_peon=None):
        self.peons = (initial_peon, None)
        self.image_cache = {}
        self.tk_button = None

    def render(self, master, board):
        """
        Return a tkinter representation of the cell
        :param master:
        :param board: the board, necessary to create the callbacks
        :return: tkinter.Button
        """
        # images must stayed in memory to be displayed by tkinter so keep a reference in the class
        if not self.is_empty and type(self.peons[0]) not in self.image_cache:
            image = Image.open(self.primary_peon.image_path())
            image = image.resize((const.CELL_WIDTH_PIXEL, const.CELL_HEIGHT_PIXEL))
            image = ImageTk.PhotoImage(image)
            self.image_cache[type(self.primary_peon)] = image
        image = self.image_cache[type(self.primary_peon)] if not self.is_empty else None

        self.tk_button = Button(
            master,
            bg=const.COLORS_HEX[self.primary_peon.team.color] if not self.is_empty else '#D3D3D3',
            image=image,
            # use pixel size for images, font size for empty cells
            width=const.CELL_WIDTH_PIXEL if image else const.CELL_WIDTH_TEXT,
            height=const.CELL_HEIGHT_PIXEL if image else const.CELL_HEIGHT_TEXT,
            command=lambda: self.handle_click(board)
        )
        return self.tk_button

    @property
    def is_empty(self):
        return self.primary_peon is None

    @property
    def primary_peon(self):
        return self.peons[0]

    def update_tk(self, **kwargs):
        """
        Update the tk representation
        :param kwargs:
        :return:
        """
        self.tk_button.configure(**kwargs)

    def handle_click(self, board):
        # Select a peon first
        if not board.selected_cell:
            # Empty cell
            if self.is_empty:
                return
            if self.primary_peon.team is not board.current_team:
                return
            board.select_peon(self)
        else:
            if self.primary_peon.team is board.current_team:
                # Replace selected peon
                board.select_peon(self)


class Board:
    def __init__(self, data_file, teams):
        self.cells = []
        self.teams_alive = teams
        self.current_team = teams[0]
        self._state_text_label = None
        self.selected_cell = None

        with open(data_file) as initial_board:
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
                            team=Team.get_by_color(teams, color),
                            position=(row_idx, col_idx)
                        )))
                    else:
                        # Add an empty cell
                        self.cells[row_idx].append(BoardCell())

    def get_state_text(self) -> str:
        """
        Return the label to show in the tkinter representation given the current game state
        :return:
        """
        if len(self.teams_alive) == 1:
            return f"{self.teams_alive[0]} won !"
        if self.selected_cell:
            return f"{self.selected_cell.primary_peon} selected"
        return f"It's {self.current_team}'s turn"

    def render(self, master):
        """
        Return a tkinter representation
        :param master:
        :return:
        """
        for row_idx, row in enumerate(self.cells):
            for col_idx, cell in enumerate(row):
                cell.render(master, self).grid(row=row_idx, column=col_idx)
        self._state_text_label = Label(master, text=self.get_state_text())
        self._state_text_label.grid(
            row=len(self.cells),
            column=0, columnspan=len(self.cells[0])
        )

    def update_text(self):
        """
        Update the TK text according to board state
        :return:
        """
        self._state_text_label.configure(text=self.get_state_text())

    def select_peon(self, cell):
        if self.selected_cell:
            self.selected_cell.update_tk(
                relief='raised'
            )
        self.selected_cell = cell
        cell.update_tk(
            relief='sunken'
        )
        self.update_text()

    def move(self, departure, arrival):
        pass
