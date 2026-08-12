# Damage rolls, targeting strategies, and the cover mechanic.

# This module is the "rules" layer - it answers questions like "how much
# damage does this hit do" and "who gets targeted", but doesn't know anything
# about turn order or the overall flow of a battle. That lives in battle.py.

import random

from .grid import FRONT_X, manhattan_distance
from .characters import Character

CRIT_CHANCE = 0.15
CRIT_MULT = 1.5
DAMAGE_VARIANCE = 0.15
COVER_DAMAGE_REDUCTION = 0.3  # tune this - 30% off incoming damage while covered


def roll_damage(attacker: Character, defender: Character) -> tuple[int, bool]:
    """Returns (damage_dealt, was_crit)."""
    base = max(1, attacker.atk - defender.defense * 0.5)
    variance = random.uniform(1 - DAMAGE_VARIANCE, 1 + DAMAGE_VARIANCE)
    is_crit = random.random() < CRIT_CHANCE
    dmg = base * variance * (CRIT_MULT if is_crit else 1.0)
    return round(dmg), is_crit

# Returns the living ally providing cover for `defender`, or None.

# Rule (simple v1): a unit standing on its side's back column is covered if
# a living ally occupies the front column in the same row. Front-column
# units are never covered - there's nothing in front of them to hide behind.

# Ideas for later, once this feels too simple:
#   - scale reduction by the provider's remaining HP% (cover gets "weaker"
#     as the tank gets low)
#   - let cover be broken/consumed after N hits instead of being permanent
#   - only apply cover against ranged/back-line attackers, not melee
#   - give specific characters a "Cover" skill that pulls aggro instead of
#     this being purely positional
def find_cover_provider(defender: Character, defender_team: list[Character]) -> Character | None:
    front_x = FRONT_X[defender.side]
    if defender.pos[0] == front_x:
        return None  # already front-line, nothing to cover it

    for ally in defender_team:
        if ally is not defender and ally.is_alive and ally.pos == (front_x, defender.pos[1]):
            return ally
    return None

# Returns (damage_reduction_fraction, provider_or_None).
def get_cover_reduction(defender: Character, defender_team: list[Character]) -> tuple[float, Character | None]:
    provider = find_cover_provider(defender, defender_team)
    if provider is None:
        return 0.0, None
    return COVER_DAMAGE_REDUCTION, provider


def pick_target(attacker: Character, enemies: list[Character], strategy) -> Character:
    living = [e for e in enemies if e.is_alive]
    if strategy == "random":
        return random.choice(living)
    if strategy == "nearest":
        return min(living, key=lambda e: manhattan_distance(attacker.pos, e.pos))
    raise ValueError(f"Unknown target strategy: {strategy}")