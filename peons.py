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

    @property
    @abc.abstractmethod
    def image_path(self):
        pass

    def __repr__(self):
        return f"{type(self).__name__} {self.color}{' dead' if not self.alive else ''}"


class Militant(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass

    def image_path(self):
        return "assets/icons/militant.png"


class Assassin(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass

    def image_path(self):
        return "assets/icons/assassin.png"


class Chief(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass

    def image_path(self):
        return "assets/icons/chief.png"


class Reporter(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass

    def image_path(self):
        return "assets/icons/reporter.png"


class Diplomate(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass

    def image_path(self):
        return "assets/icons/diplomate.png"


class Necromobile(Peon):
    def available_moves(self):
        pass

    def after_move(self):
        pass

    def image_path(self):
        return "assets/icons/necromobile.png"


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
        'diplomat': Diplomate,
        'necromobile': Necromobile
    }[peon_type](board, position, color)
