# Movement: advancing a character's float position toward a target at a
# fixed speed, and checking whether an attacker is currently in range.

import math

from .characters import Character
from .cover import CoverObject, COVER_RADIUS
from .grid import MOVE_SPEED, euclidean_distance

ARRIVAL_EPSILON = 0.05


def is_in_range(attacker: Character, defender: Character) -> bool:
    return euclidean_distance(attacker.pos, defender.pos) <= attacker.atk_range


# Best cover position to head for, or None if nothing applies
# A cover object qualifies if:
#   - it isnt destroyed
#   - being in it would put the defender within character.atk_range
#   - no other living character is already occupying it (within COVER_RADIUS)
# Picks closest qualifying cover
def _find_best_cover_position(character: Character, defender: Character,
                               cover_objects: list[CoverObject],
                               all_units: list[Character]) -> tuple[float, float] | None:
    candidates = []
    for cover in cover_objects:
        if cover.is_destroyed:
            continue
        if euclidean_distance(cover.pos, defender.pos) > character.atk_range:
            continue # would cause defender to be out of range

        occupied = any(
            other is not character and other.is_alive
            and euclidean_distance(other.pos, cover.pos) <= COVER_RADIUS
            for other in all_units
        )
        if occupied:
            continue

        candidates.append(cover)

    if not candidates:
        return None

    return min(candidates, key=lambda c: euclidean_distance(character.pos, c.pos)).pos

# Advance character.pos by up to MOVE_SPEED this tick.
# Prefers heading to a qualifying, unoccupied cover object that would put
# defender in range once reached. Falls back to moving straight at
# defender.pos if no such cover exists. Updates isMoving based on
# whether the character has arrived at its destination this tick.
def move_toward(character: Character, defender: Character,
                 cover_objects: list[CoverObject], all_units: list[Character]) -> None:
    target_pos = _find_best_cover_position(character, defender, cover_objects, all_units)
    if target_pos is None:
        target_pos = defender.pos

    dx = target_pos[0] - character.pos[0]
    dy = target_pos[1] - character.pos[1]
    dist = math.hypot(dx, dy)

    if dist <= ARRIVAL_EPSILON:
        character.pos = target_pos
        character.isMoving = False
        return

    step = min(MOVE_SPEED, dist)
    character.pos = (
        character.pos[0] + dx / dist * step,
        character.pos[1] + dy / dist * step,
    )
    character.isMoving = (dist - step) > ARRIVAL_EPSILON