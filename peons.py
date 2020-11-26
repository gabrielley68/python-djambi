import abc

from utils import get_available_moves, get_adjacent_alive_enemies
import const


class Peon(abc.ABC):
    """
    Basic abstract class for peons
    """
    def __init__(self, board, position: tuple, team):
        self.board = board
        self.alive = True
        self.position = position
        self.team = team

    @abc.abstractmethod
    def available_moves(self):
        pass

    @abc.abstractmethod
    def after_move(self):
        concurrent_peon = self.cell.peons[1]
        if concurrent_peon:
            concurrent_peon.die(self)
            self.board.selected_cell = self.cell
            self.board.state = const.BOARD_STATE_MOVING_PEON
            self.board.update_text()
        else:
            self.board.next_turn()

    @property
    @abc.abstractmethod
    def image_path(self):
        pass

    @property
    def cell(self):
        return self.board.cells[self.position[0]][self.position[1]]

    def die(self, killed_by):
        self.alive = False

    def select_adjacent(self, peon):
        pass

    def __repr__(self):
        return f"{type(self).__name__} {self.team}{' dead' if not self.alive else ''}"


class Militant(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position, can_use_enemy=True, maximum_steps=2)

    def after_move(self):
        super().after_move()

    @property
    def image_path(self):
        return "assets/icons/militant.png"


class Assassin(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position, can_use_enemy=True)

    def after_move(self):
        # Kill arrival peon if there's one
        concurrent_peon = self.cell.peons[1]
        if concurrent_peon:
            concurrent_peon.die(self)
            self.board.move(concurrent_peon, self.board.selected_cell)
        self.board.next_turn()

    @property
    def image_path(self):
        return "assets/icons/assassin.png"


class Chief(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position, can_use_enemy=True)

    def after_move(self):
        super().after_move()

    def die(self, killed_by):
        """
        Chief die => owner looses and the killer gets all his peons
        :param killed_by:
        :return:
        """
        super().die(killed_by)
        for row in self.board.cells:
            for cell in row:
                peon = cell.primary_peon
                if peon and peon.team == self.team:
                    peon.team = killed_by.team
                    cell.redraw_image()
        self.board.teams_alive.remove(self.team)

    @property
    def image_path(self):
        return "assets/icons/chief.png"


class Reporter(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position)

    def after_move(self):
        if get_adjacent_alive_enemies(self):
            self.board.selected_cell = self.cell
            self.board.state = const.BOARD_STATE_SELECT_ADJACENT
            self.board.update_text()
        else:
            self.board.next_turn()

    def select_adjacent(self, peon):
        peon.die(self)
        peon.cell.redraw_image()
        self.board.next_turn()

    @property
    def image_path(self):
        return "assets/icons/reporter.png"


class Diplomate(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position, can_use_enemy=True)

    def after_move(self):
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
    Initialize a peon with a string representing its type and its constructor arguments
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
