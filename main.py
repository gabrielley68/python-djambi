from board import *
from team import *
import const

teams = [Team(color) for color in const.COLORS]
b = Board()

# Temp testing
for row in b.cells:
    for col in row:
        print(col.peons)
    print("-----------------")
