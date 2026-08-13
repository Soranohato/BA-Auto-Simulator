
#Grid layout and positioning.

from .characters import Character
import math

GRID_WIDTH = 20.0
GRID_HEIGHT = 10.0
FRONT_X = {"A": 8.0, "B": 12.0}
BACK_X = {"A": 2.0, "B": 18.0}
FRONT_ROLES = {"tank", "striker"}
MOVE_SPEED = 1.0

def euclidean_distance(pos_a: tuple[float, float], pos_b: tuple[float, float]) -> float:
    return math.dist(pos_a, pos_b)


def assign_positions(team: list[Character], side: str):
    rows = [2.0, 5.0, 8.0]  # evenly spread across GRID_HEIGHT=10
    y_front = 0
    y_back = 0
    for c in team:
        c.side = side
        if c.role in FRONT_ROLES:
            c.pos = (FRONT_X[side], rows[y_front % len(rows)])
            y_front += 1
        else:
            c.pos = (BACK_X[side], rows[y_back % len(rows)])
            y_back += 1