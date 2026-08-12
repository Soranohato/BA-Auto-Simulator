
#Grid layout and positioning.

# 6 columns (0-5) x 3 rows (0-2). Team A holds cols 0-1, Team B holds cols 4-5.
# Column 1 is Team A's front line, column 4 is Team B's front line - they face
# each other across the middle "no man's land" (cols 2-3).


from .characters import Character

GRID_WIDTH = 6
GRID_HEIGHT = 3
FRONT_X = {"A": 1, "B": 4}
BACK_X = {"A": 0, "B": 5}
FRONT_ROLES = {"tank", "striker"}


def manhattan_distance(pos_a: tuple[int, int], pos_b: tuple[int, int]) -> int:
    return abs(pos_a[0] - pos_b[0]) + abs(pos_a[1] - pos_b[1])


def assign_positions(team: list[Character], side: str):
    # Front-line roles go to the side's front column, everyone else goes
    # to the back column. Stacks units down the y-axis within their row.
    y_front = 0
    y_back = 0
    for c in team:
        c.side = side
        if c.role in FRONT_ROLES:
            c.pos = (FRONT_X[side], y_front % GRID_HEIGHT)
            y_front += 1
        else:
            c.pos = (BACK_X[side], y_back % GRID_HEIGHT)
            y_back += 1