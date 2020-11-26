from tkinter import Button, Label
import sys

import const
from peons import peon_factory
from team import Team
from utils import ImageCache, get_adjacent_alive_enemies


class BoardCell:
    def __init__(self, image_cache, initial_peon=None):
        self.peons = (initial_peon, None)
        self.image_cache = image_cache
        self.tk_button = None

    def render(self, master, board):
        """
        Return a tkinter representation of the cell
        :param master:
        :param board: the board, necessary to create the callbacks
        :return: tkinter.Button
        """
        # images must stay in memory to be displayed by tkinter so keep a reference in the class
        image = self.image_cache[self.primary_peon.image_path if self.primary_peon else None]

        self.tk_button = Button(
            master,
            bg=const.COLORS_HEX[self.primary_peon.team.color] if not self.is_empty else '#D3D3D3',
            image=image,
            # use pixel size for images, font size for empty cells
            width=const.CELL_WIDTH_PIXEL,
            height=const.CELL_HEIGHT_PIXEL,
            command=lambda: self.handle_click(board)
        )
        return self.tk_button

    @property
    def is_empty(self):
        return self.primary_peon is None

    @property
    def primary_peon(self):
        """
        Return the main peon of the cell. There may be 0, 1 or 2 peons.
        :return:
        """
        return self.peons[0]

    @property
    def secondary_peon(self):
        """
        Return the second peon on the cell if there's one.
        :return:
        """
        return self.peons[1]

    @property
    def position(self):
        """
        Get coordinates in the grid
        :return:
        """
        grid_info = self.tk_button.grid_info()
        return grid_info["row"], grid_info["column"]

    def redraw_image(self):
        """
        Replace the current image on the tk button
        :param peon:
        :return:
        """
        color = "#D3D3D3"
        if self.primary_peon and not self.primary_peon.alive:
            color = "#808080"
        elif self.primary_peon:
            color = const.COLORS_HEX[self.primary_peon.team.color]
        image = self.image_cache[self.primary_peon.image_path if self.primary_peon else None]
        self.update_tk(
            image=image,
            bg=color,
        )

    def update_tk(self, **kwargs):
        """
        Update the tk representation
        :param kwargs:
        :return:
        """
        self.tk_button.configure(**kwargs)

    def handle_click(self, board):
        """
        Callback onD button press
        :param board:
        :return:
        """
        if board.state == const.BOARD_STATE_STANDARD:
            self.handle_click_standard(board)
        elif board.state == const.BOARD_STATE_MOVING_PEON:
            self.handle_click_moving_peon(board)
        elif board.state == const.BOARD_STATE_SELECT_ADJACENT:
            self.handle_click_selecting_adjacent(board)

    def handle_click_standard(self, board):
        """
        Handles selecting and moving it's peon based on play turn
        :param board:
        :return:
        """
        # Select a peon first
        if not board.selected_cell:
            # Empty cell
            if self.is_empty:
                return
            if self.primary_peon.team is not board.current_team:
                return
            if self.primary_peon.alive:
                board.select_peon(self)
        else:
            if (
                self.primary_peon
                and self.primary_peon.team is board.current_team
                and self.primary_peon.alive
            ):
                # Replace selected peon
                board.select_peon(self)
            else:
                if self.position in board.selected_cell.primary_peon.available_moves():
                    selected_peon = board.selected_cell.primary_peon
                    board.selected_cell.peons = (None, None)
                    board.selected_cell.redraw_image()
                    board.move(selected_peon, self, activate_peon_after_move=True)

    def handle_click_moving_peon(self, board):
        if self.is_empty:
            board.move(board.selected_cell.secondary_peon, self)
            board.next_turn()

    def handle_click_selecting_adjacent(self, board):
        if self.position in get_adjacent_alive_enemies(board.selected_cell.primary_peon):
            board.selected_cell.primary_peon.select_adjacent(self.primary_peon)


class Board:
    def __init__(self, data_file, teams):
        self.cells = []
        self.teams_alive = teams
        self.current_team = teams[0]
        self._state_text_label = None
        self.selected_cell = None
        self.state = const.BOARD_STATE_STANDARD

        self.image_cache = ImageCache()

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
                        self.cells[row_idx].append(BoardCell(
                            image_cache=self.image_cache,
                            initial_peon=peon_factory(
                                board=self,
                                peon_type=peon,
                                team=Team.get_by_color(teams, color),
                                position=(row_idx, col_idx)
                            )
                        ))
                    else:
                        # Add an empty cell
                        self.cells[row_idx].append(BoardCell(
                            image_cache=self.image_cache
                        ))

    def get_state_text(self) -> str:
        """
        Return the label to show in the tkinter representation given the current game state
        :return:
        """
        if len(self.teams_alive) == 1:
            return f"{self.teams_alive[0]} won !"
        if self.state == const.BOARD_STATE_MOVING_PEON:
            return f"Place {self.selected_cell.secondary_peon} on an empty cell"
        elif self.state == const.BOARD_STATE_SELECT_ADJACENT:
            return "Select an adjacent peon"
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
        """
        Select a peon, making its cell's button 'sunken'
        :param cell:
        :return:
        """
        if self.selected_cell:
            self.selected_cell.update_tk(
                relief='raised'
            )
        self.selected_cell = cell
        cell.update_tk(
            relief='sunken'
        )
        self.update_text()

    def next_turn(self):
        self.selected_cell = None
        self.current_team = self.teams_alive[(self.teams_alive.index(self.current_team) + 1) % len(self.teams_alive)]
        self.state = const.BOARD_STATE_STANDARD
        self.update_text()

    def move(self, peon, arrival_cell, activate_peon_after_move=False):
        """
        Move a peon from one cell to another
        :param peon:
        :param arrival_cell:
        :param activate_peon_after_move:
        :return:
        """
        peon.position = arrival_cell.position
        arrival_cell.peons = (peon, arrival_cell.primary_peon)
        arrival_cell.redraw_image()
        if activate_peon_after_move:
            peon.after_move()
