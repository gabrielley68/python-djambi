from tkinter import Button, Label
import sys

import const
from peons import peon_factory
from team import Team
from utils import ImageCache, get_adjacent_alive_enemies, is_surrounded_by_bodies


class BoardCell:
    """
    A cell of the board.
    A cell can contains nothing or up to 2 peons
    When a peon come on a cell to kill or replace a peon, we store both of them on the Cell while the player
    choose where to move the old one).
    Those are stored on the tuple(?Peon, ?Peon)
    """
    def __init__(self, image_cache, initial_peon=None):
        self.peons = (initial_peon, None)
        self.image_cache = image_cache
        self.tk_button = None

    def render(self, master, board):
        """
        Return a tkinter representation of the cell
        :param master: the Tk container
        :param board: the board, necessary to create the on_click events callbacks
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
        Return the main peon of the cell if there's one.
        :return: Peon
        """
        return self.peons[0]

    @property
    def secondary_peon(self):
        """
        Return the second peon on the cell if there's one.
        :return: Peon
        """
        return self.peons[1]

    @property
    def position(self):
        """
        Get coordinates in the grid
        :return: tuple(int, int)
        """
        grid_info = self.tk_button.grid_info()
        return grid_info["row"], grid_info["column"]

    def redraw_image(self):
        """
        Replace the current image on the tk button according to the cell's state
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
        :param kwargs: param: value
        """
        self.tk_button.configure(**kwargs)

    def handle_click(self, board):
        """
        Callback on button press according to current board state
        :param board:
        """
        if board.state == const.BOARD_STATE_STANDARD:
            self.handle_click_standard(board)
        elif board.state == const.BOARD_STATE_MOVING_PEON:
            self.handle_click_moving_peon(board)
        elif board.state == const.BOARD_STATE_SELECT_ADJACENT:
            self.handle_click_selecting_adjacent(board)

    def handle_click_standard(self, board):
        """
        Player can select a peon and move it on the board
        :param board:
        """
        # Select a peon first
        if not board.selected_cell:
            # Empty cell
            if self.is_empty:
                return
            # Don't let move other player peons
            if self.primary_peon.team is not board.current_team:
                return
            # Can't move dead peons
            if self.primary_peon.alive:
                board.select_peon(self)
        # Peon is selected, select where to move it
        else:
            if (
                self.primary_peon
                and self.primary_peon.team is board.current_team
                and self.primary_peon.alive
            ):
                # Replace selected peon if user changed his mind
                board.select_peon(self)
            else:
                # Peon have different movesets depending on it's type
                if self.position in board.selected_cell.primary_peon.available_moves():
                    selected_peon = board.selected_cell.primary_peon
                    # Remove the peon from its original position
                    board.selected_cell.peons = (None, None)
                    board.selected_cell.redraw_image()
                    # Move it and activate its effect
                    board.move(selected_peon, self, activate_peon_after_move=True)

    def handle_click_moving_peon(self, board):
        """
        Move the current select peon to an empty cell
        :param board:
        """
        if self.is_empty:
            board.move(board.selected_cell.secondary_peon, self)
            board.next_turn()

    def handle_click_selecting_adjacent(self, board):
        """
        Reporter can select adjacent peons on move
        :param board:
        """
        if self.position in get_adjacent_alive_enemies(board.selected_cell.primary_peon):
            board.selected_cell.primary_peon.select_adjacent(self.primary_peon)


class Board:
    """
    Contains the state of the whole game.
    """
    def __init__(self, data_file, teams):
        """
        Initialise board with a text file representing initial peon positions
        :param data_file: file path
        :param teams: list[Team]
        """
        self.cells = []
        self.teams_alive = teams
        self.current_team = teams[0]
        self._state_text_label = None
        self.selected_cell = None
        self.state = const.BOARD_STATE_STANDARD

        # Initialize a cache to only load image once
        self.image_cache = ImageCache()

        with open(data_file) as initial_board:
            # Read initial_board and iterate on each line
            for row_idx, row_data in enumerate([row.rstrip('\n') for row in initial_board]):
                self.cells.append(list())
                for col_idx, col_data in enumerate(row_data.split()):
                    try:
                        peon, color = col_data.split("_")
                    except ValueError:
                        print("Error parsing initial_board.txt, please verify format", file=sys.stderr)
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
        Return a tkinter representation of the♥2board
        :param master:
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
        """
        self._state_text_label.configure(text=self.get_state_text())

    def select_peon(self, cell):
        """
        Select a peon, making its cell's button 'sunken'
        :param cell:
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
        """
        End the current turn, changing current player
        """
        current_team_index = self.teams_alive.index(self.current_team)
        self.selected_cell = None
        for row in self.cells:
            for cell in row:
                if cell.primary_peon and cell.primary_peon.die_if_surrounded_by_bodies:
                    if is_surrounded_by_bodies(cell.primary_peon):
                        cell.primary_peon.die(self.current_team)

        self.current_team = self.teams_alive[(current_team_index + 1) % len(self.teams_alive)]
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
