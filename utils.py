from PIL import Image, ImageTk

import const

EMPTY = 'empty'
BODY = 'body'
ALLY = 'ally'
ENEMY = 'enemy'


def get_cell_state(initial_cell, cell):
    """
    Get the state of a given cell
    Available states :
    - EMPTY : No peon of the cell
    - BODY : A peon is there but is dead
    - ALLY : A peon from the same team is there
    - ENEMY : A peon from an opponent team is here
    :param initial_cell:
    :param cell:
    :return:
    """
    if cell.is_empty:
        return EMPTY
    if not cell.primary_peon.alive:
        return BODY
    if initial_cell.primary_peon.team is cell.primary_peon.team:
        return ALLY
    return ENEMY


def get_directions(board, initial_pos):
    return (
        [(y, initial_pos[1]) for y in range(initial_pos[0] - 1, 0, -1)],  # vertical up
        [(y, initial_pos[1]) for y in range(initial_pos[0] + 1, len(board.cells))],  # vertical down
        [(initial_pos[0], x) for x in range(initial_pos[1] - 1, 0, -1)],  # horizontal left
        [(initial_pos[0], x) for x in range(initial_pos[1] + 1, len(board.cells[0]))],  # horizontal right
        [
            (initial_pos[0] + i, initial_pos[1] + i)
            for i in range(1, min(len(board.cells) - initial_pos[0], len(board.cells[0]) - initial_pos[1]))
        ],  # diagonale down-right
        [
            (initial_pos[0] + i, initial_pos[1] - i)
            for i in range(1, min(len(board.cells) - initial_pos[0], initial_pos[1] + 1))
        ],  # diagonale down-left
        [
            (initial_pos[0] - i, initial_pos[1] - i)
            for i in range(1, min(initial_pos[0] + 1, initial_pos[1]))
        ],  # diagonale up-left
        [
            (initial_pos[0] - i, initial_pos[1] + i)
            for i in range(1, min(initial_pos[0] + 1, len(board.cells[0]) - initial_pos[1]))
        ],  # diagonale up-right
    )


def get_available_moves(board, initial_pos, can_use_enemy=False, can_use_body=False, maximum_steps=0):
    """
    Return a list of available move through a board
    :param initial_pos:
    :param board:
    :param can_use_enemy:
    :param can_use_body:
    :param maximum_steps:
    :return:
    """
    available_moves = list()

    directions = get_directions(board, initial_pos)

    for direction in directions:
        interation_index = 0
        for current_position in direction:
            if maximum_steps and interation_index >= maximum_steps:
                break
            interation_index += 1
            cell_state = get_cell_state(
                board.cells[initial_pos[0]][initial_pos[1]],
                board.cells[current_position[0]][current_position[1]]
            )
            if cell_state == BODY:
                if can_use_body:
                    available_moves.append(current_position)
                break
            elif cell_state == ALLY:
                break
            elif cell_state == ENEMY:
                if can_use_enemy:
                    available_moves.append(current_position)
                break
            else:
                available_moves.append(current_position)

    return available_moves


def get_adjacent_alive_enemies(peon):
    """
    Get the position of all enemies peon that are alive
    :param peon:
    :return:
    """
    board = peon.board
    enemies_coordinates = list()
    row_index, col_index = peon.position
    for y in range(max(0, row_index-1), min(len(board.cells), row_index+2)):
        for x in range(max(0, col_index-1), min(len(board.cells[y]), col_index+2)):
            if (y, x) == peon.position:
                continue
            other_peon = board.cells[y][x].primary_peon
            if not other_peon:
                continue
            if other_peon.team != peon.team and other_peon.alive:
                enemies_coordinates.append(other_peon.position)

    return enemies_coordinates


class ImageCache:
    """
    ImageCache so we don't reload all images for each cell
    Meant to be used ONLY with the 'get dict' syntax using image's filepath.
    the image will be opened and saved automatically
    eg: my_image = my_image_cache['file/to/image.png']
    """
    def __init__(self):
        self.cache = {}

    def _add(self, key):
        image = Image.open(key)
        image = image.resize((const.CELL_WIDTH_PIXEL, const.CELL_HEIGHT_PIXEL))
        image = ImageTk.PhotoImage(image)
        self.cache[key] = image

    def __getitem__(self, item):
        if item is None:
            item = 'assets/icons/blank.png'
        if item not in self.cache:
            self._add(item)
        return self.cache[item]
