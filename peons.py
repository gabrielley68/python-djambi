import abc

from utils import get_available_moves


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
        pass

    @property
    @abc.abstractmethod
    def image_path(self):
        pass

    def __repr__(self):
        return f"{type(self).__name__} {self.team}{' dead' if not self.alive else ''}"


class Militant(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position, can_kill=True, maximum_steps=2)

    def after_move(self):
        pass

    @property
    def image_path(self):
        return "assets/icons/militant.png"


class Assassin(Peon):
    def available_moves(self):
        get_available_moves(self.board, self.position, can_kill=True)

    def after_move(self):
        pass

    @property
    def image_path(self):
        return "assets/icons/assassin.png"


class Chief(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position, can_kill=True)

    def after_move(self):
        pass

    @property
    def image_path(self):
        return "assets/icons/chief.png"


class Reporter(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position)

    def after_move(self):
        pass

    @property
    def image_path(self):
        return "assets/icons/reporter.png"


class Diplomate(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position)

    def after_move(self):
        pass

    @property
    def image_path(self):
        return "assets/icons/diplomate.png"


class Necromobile(Peon):
    def available_moves(self):
        return get_available_moves(self.board, self.position, can_use_body=True)

    def after_move(self):
        pass

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
