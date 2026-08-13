# Cover objects: manually-placed obstacles on the grid that reduce incoming
# damage, replacing the old "hide behind a living ally" mechanic.

from dataclasses import dataclass

from .characters import Character
from .grid import euclidean_distance

COVER_DAMAGE_REDUCTION = 0.3  # default reduction; per-object override via `reduction`
COVER_RADIUS = 0.5


@dataclass
class CoverObject:
    name: str
    pos: tuple[int, int]
    reduction: float = COVER_DAMAGE_REDUCTION
    hp: int | None = None  # None = indestructible. Set a value to make it breakable later.

    @property
    def is_destroyed(self) -> bool:
        return self.hp <= 0

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)

def make_cover_layout() -> list[CoverObject]:
    
    # TODO: make this a random set of cover mirrored horizontally and vertically in the future
    return [
        CoverObject("CoverFA", pos=(8.0, 2.0), hp=50),
        CoverObject("CoverBA", pos=(8.0, 8.0), hp=50),
        CoverObject("CoverFB", pos=(12.0, 2.0), hp=50),
        CoverObject("CoverBB", pos=(12.0, 8.0), hp=50),
        CoverObject("CoverMid", pos=(10.0, 5.0), hp=75),  # contested centerpiece
    ]

# determines if a Character is behind cover or not. To be behind cover a Character must be
# within COVER_RADIUS of the coer object
def find_cover_object(defender: Character, cover_objects: list[CoverObject]) -> CoverObject | None:
    if defender.isMoving: 
        return None # cannot be under cover while moving
    for cover in cover_objects:
        if euclidean_distance(defender.pos, cover.pos) <= COVER_RADIUS and not cover.is_destroyed:
            return cover
    return None

# Returns (cover_damage_reduction, provider OR None)
def get_cover_reduction(defender: Character, cover_objects: list[CoverObject]) -> tuple[float, CoverObject | None]:
    provider = find_cover_object(defender, cover_objects)
    if provider is None:
        return 0.0, None
    return provider.reduction, provider