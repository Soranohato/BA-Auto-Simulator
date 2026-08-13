
#Grid layout and positioning.

# 6 columns (0-5) x 3 rows (0-2). Team A holds cols 0-2, Team B holds cols 3-5.
# Column 2 is Team A's front line, column 3 is Team B's front line


from .characters import Character
import math

GRID_WIDTH = 6
GRID_HEIGHT = 3
FRONT_X = {"A": 2, "B": 3}
BACK_X = {"A": 0, "B": 5}
FRONT_ROLES = {"tank", "striker"}
MOVE_SPEED = 1.0

def euclidean_distance(pos_a: tuple[float, float], pos_b: tuple[float, float]) -> float:
    return math.dist(pos_a, pos_b)


def assign_positions(team: list[Character], side: str):
    # Front-line roles go to the side's front column, everyone else goes
    # to the back column. Stacks units down the y-axis within their row.
    y_front = 0
    y_back = 1
    for c in team:
        c.side = side
        if c.role in FRONT_ROLES:
            c.pos = (FRONT_X[side], y_front % GRID_HEIGHT)
            y_front += 1
        else:
            c.pos = (BACK_X[side], y_back % GRID_HEIGHT)
            y_back += 1