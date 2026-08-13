# The character roster. Plain data - swap this out for a JSON/dict-loaded
# roster later without touching anything else in the project.

from .characters import Character


def make_roster() -> dict[str, Character]:
    return {
        "Hoshino":  Character("Hoshino",  max_hp=120, atk=28, defense=10, spd=14, atk_range=2.5,  role="striker"),
        "Aru":      Character("Aru",      max_hp=90,  atk=32, defense=6,  spd=18, atk_range=5.0,  role="striker"),
        "Hifumi":   Character("Hifumi",   max_hp=110, atk=18, defense=14, spd=10, atk_range=7.0,  role="support"),
        "Iori":     Character("Iori",     max_hp=140, atk=20, defense=18, spd=8,  atk_range=5.0,  role="tank"),
        "Shiroko":  Character("Shiroko",  max_hp=100, atk=26, defense=8,  spd=16, atk_range=2.5,  role="striker"),
        "Yuzu":     Character("Yuzu",     max_hp=105, atk=22, defense=12, spd=12, atk_range=7.5,  role="support"),
    }