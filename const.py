COLOR_RED = 'red'
COLOR_BLUE = 'blue'
COLOR_YELLOW = 'yellow'
COLOR_GREEN = 'green'

COLORS = (COLOR_RED, COLOR_BLUE, COLOR_YELLOW, COLOR_GREEN)

COLORS_HEX = {
    COLOR_RED: "#ff0000",
    COLOR_BLUE: "#0000ff",
    COLOR_YELLOW: "#ffff00",
    COLOR_GREEN: "#00ff00",
}

# Tkinter use both text units or pixel units depending if it's displaying an image or text
# Text units
CELL_WIDTH_TEXT = 8
CELL_HEIGHT_TEXT = 4

# Pixel units
CELL_WIDTH_PIXEL = CELL_HEIGHT_PIXEL = 62

# Board states
# Standard : Composed of 2 states : select a peon, then move it on an availale cell
BOARD_STATE_STANDARD = 1

# Moving peon : some peons have the ability to move peon (alive or not)
# from one cell to another, board has a specific state to select the cell where to move these peons
BOARD_STATE_MOVING_PEON = 2

# Select adjacent : some peons (only reporter currently) can select a peon around him to interact with him from distance
# board has a specific state to select the adjacent cell
BOARD_STATE_SELECT_ADJACENT = 3
