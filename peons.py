import abc


class Pion(abc.ABC):
    def __init__(self, board, position: tuple, color: str):
        self.board = board
        self.alive = True
        self.position: position
        self.color: color

    @property
    def alive(self) -> bool:
        return self.alive

    @alive.setter
    def alive(self, alive: bool):
        self.alive = alive

    @property
    def position(self) -> tuple:
        return self.position

    @position.setter
    def position(self, value: tuple):
        self.position = value

    @property
    def color(self) -> str:
        return self.color

    @color.setter
    def color(self, value: str):
        self.color = value

    @abc.abstractmethod
    def available_moves(self):
        pass

    @abc.abstractmethod
    def after_move(self):
        pass


class Militant(Pion):
    def available_moves(self):
        pass

    def after_move(self):
        pass


class Assassin(Pion):
    def available_moves(self):
        pass

    def after_move(self):
        pass


class Chef(Pion):
    def available_moves(self):
        pass

    def after_move(self):
        pass


class Reporter(Pion):
    def available_moves(self):
        pass

    def after_move(self):
        pass


class Diplomate(Pion):
    def available_moves(self):
        pass

    def after_move(self):
        pass


class Necromobile(Pion):
    def available_moves(self):
        pass

    def after_move(self):
        pass
