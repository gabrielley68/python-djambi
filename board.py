import sys

from peons import peon_factory


class BoardCell:
    def __init__(self, initial_peon=None):
        self.peons = (initial_peon, None)


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
                        self.cells[row_idx].append(BoardCell(None))

    def move(self, departure, arrival):
        pass
