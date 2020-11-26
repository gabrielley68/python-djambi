import abc

from utils import get_available_moves, get_adjacent_alive_enemies
import const


class Peon(abc.ABC):
    """
    Basic abstract class for peons
    """
    def __init__(self, board, position: tuple, team):
        """
        Peon is caracterized by a team and a type
        Position is tuple (int, int) with the current coordinates of the peon on the board
        Also include board to be able to calculate possibilites of move and interact with other peon.
        With the combination of position and board we can also determine on which cell is the peon.
        :param board:
        :param position:
        :param team:
        """
        self.board = board
        self.alive = True
        self.position = position
        self.team = team
        self.die_if_surrounded_by_bodies = False

    @abc.abstractmethod
    def available_moves(self):
        """
        Return the list of all valid positions to move
        """
        pass

    @abc.abstractmethod
    def after_move(self):
        """
        Actions to perform once the peon moved
        Default implementation kills the potential present peon and replace it on an available cell
        :return:
        """
        concurrent_peon = self.cell.peons[1]
        if concurrent_peon:
            concurrent_peon.die(self.team)
            self.board.selected_cell = self.cell
            self.board.state = const.BOARD_STATE_MOVING_PEON
            self.board.update_text()
        else:
            self.board.next_turn()

    @property
    @abc.abstractmethod
    def image_path(self):
        """
        Return the path to the image representing this peon type
        """
        pass

    @property
    def cell(self):
        """
        Shortcut to get the cell containing this peon
        :return:
        """
        return self.board.cells[self.position[0]][self.position[1]]

    def die(self, killed_by):
        """
        Kill the current peon
        Overload to add specific action to perform
        :param killed_by: Team killer
        """
        self.alive = False

    def select_adjacent(self, peon):
        """
        Action to perform when a peon select an adjacent peon.
        Currently only implemented by Reporter type
        :param peon: the selected Peon
        """
        pass

    def __repr__(self):
        return f"{type(self).__name__} {self.team}{' dead' if not self.alive else ''}"


class Militant(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position, can_use_enemy=True, maximum_steps=2)

    def after_move(self):
        """
        Inherit default comportment
        """
        super().after_move()

    @property
    def image_path(self):
        return "assets/icons/militant.png"


class Assassin(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position, can_use_enemy=True)

    def after_move(self):
        # Kill peon if there's one, and move it on the initial position
        concurrent_peon = self.cell.peons[1]
        if concurrent_peon:
            concurrent_peon.die(self.team)
            self.board.move(concurrent_peon, self.board.selected_cell)
        self.board.next_turn()

    @property
    def image_path(self):
        return "assets/icons/assassin.png"


class Chief(Peon):
    def __init__(self, board, position: tuple, team):
        super().__init__(board, position, team)
        self.die_if_surrounded_by_bodies = True

    def available_moves(self):
        return get_available_moves(self.board, self.position, can_use_enemy=True)

    def after_move(self):
        """
        Inherit default comportment
        """
        super().after_move()

    def die(self, killed_by):
        """
        Chief die => owner looses and the killer steal all his peons
        """
        super().die(killed_by)
        for row in self.board.cells:
            for cell in row:
                peon = cell.primary_peon
                if peon and peon.team == self.team:
                    peon.team = killed_by
                    cell.redraw_image()
        self.board.teams_alive.remove(self.team)

    @property
    def image_path(self):
        return "assets/icons/chief.png"


class Reporter(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position)

    def after_move(self):
        """
        If the reporter have an adjacent enemy living peon, he can select him
        Else, the turn is over
        """
        if get_adjacent_alive_enemies(self):
            self.board.selected_cell = self.cell
            self.board.state = const.BOARD_STATE_SELECT_ADJACENT
            self.board.update_text()
        else:
            self.board.next_turn()

    def select_adjacent(self, peon):
        """
        Kill the adjacent peon, but let it at it's current position
        :return:
        """
        peon.die(self.team)
        peon.cell.redraw_image()
        self.board.next_turn()

    @property
    def image_path(self):
        return "assets/icons/reporter.png"


class Diplomate(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position, can_use_enemy=True)

    def after_move(self):
        """
        When a diplomat move on an occupied cell, move the peon to the place of your choice
        """
        concurrent_peon = self.cell.peons[1]
        if concurrent_peon:
            self.board.selected_cell = self.cell
            self.board.state = const.BOARD_STATE_MOVING_PEON
            self.board.update_text()
        else:
            self.board.next_turn()

    @property
    def image_path(self):
        return "assets/icons/diplomate.png"


class Necromobile(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position, can_use_body=True)

    def after_move(self):
        """
        Necromobile can move a body situated on the same cell as him.
        """
        concurrent_peon = self.cell.peons[1]
        if concurrent_peon:
            self.board.selected_cell = self.cell
            self.board.state = const.BOARD_STATE_MOVING_PEON
            self.board.update_text()
        else:
            self.board.next_turn()

    @property
    def image_path(self):
        return "assets/icons/necromobile.png"


def peon_factory(board, peon_type: str, team, position: tuple) -> Peon:
    """
    Initialize a peon with a string representing of its type and its constructor arguments
    :param board:
    :param peon_type:
    :param team:
    :param position:
    :return:
    """
    return {
        'chief': Chief,
        'assassin': Assassin,
        'reporter': Reporter,
        'militant': Militant,
        'diplomat': Diplomate,
        'necromobile': Necromobile
    }[peon_type](board, position, team)
