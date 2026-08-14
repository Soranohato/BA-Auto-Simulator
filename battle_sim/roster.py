# The character roster. Loaded from data/roster.json

import json
from pathlib import Path

from .characters import Character

DATA_PATH = Path(__file__).parent / "data" / "roster.json"


def make_roster() -> dict[str, Character]:
    with open(DATA_PATH, "r") as f:
        raw = json.load(f)

    return {name: Character(name=name, **stats) for name, stats in raw.items}