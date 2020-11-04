import abc


class Peon(abc.ABC):
    def __init__(self, board, position: tuple, color: str):
        self.board = board
        self.alive = True
        self.position = position
        self.color = color

    @abc.abstractmethod
    def available_moves(self):
        pass

    @abc.abstractmethod
    def after_move(self):
        pass

    def __repr__(self):
        return f"{type(self).__name__} {self.color}{' dead' if not self.alive else ''}"


class Militant(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass


class Assassin(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass


class Chief(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass


class Reporter(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass


class Diplomat(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass


class Necromobile(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass


def peon_factory(board, peon_type: str, color: str, position: tuple) -> Peon:
    """
    Initialize a peon with a string representing its type and its constructor arguments
    :param board:
    :param peon_type:
    :param color:
    :param position:
    :return:
    """
    return {
        'chief': Chief,
        'assassin': Assassin,
        'reporter': Reporter,
        'militant': Militant,
        'diplomat': Diplomat,
        'necromobile': Necromobile
    }[peon_type](board, position, color)
