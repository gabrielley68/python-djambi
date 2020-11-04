class BoardCell:
    def __init__(self):
        self.peons = []


class Board:
    def __init__(self, width=9, height=9):
        self.cells = [[BoardCell() for _ in range(width)] for _ in range(height)]

    def move(self, departure, arrival):
        pass
