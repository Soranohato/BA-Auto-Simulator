# Cover objects: manually-placed obstacles on the grid that reduce incoming
# damage, replacing the old "hide behind a living ally" mechanic.

from dataclasses import dataclass
import random

from .characters import Character
from .grid import euclidean_distance, GRID_HEIGHT, GRID_WIDTH, FRONT_X

COVER_DAMAGE_REDUCTION = 0.3  # default reduction; per-object override via `reduction`
COVER_RADIUS = 0.5

COVER_X_MIN = FRONT_X["A"]
CENTER_X = GRID_WIDTH / 2
CENTER_Y = GRID_HEIGHT / 2
COVER_Y_MARGIN = 0.5

MIN_COVER_SPACING = 1.5
MAX_PLACEMENT_ATTEMPTS = 20


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

def _far_enough(x: float, y: float, placed: list[CoverObject]) -> bool:
    return all(euclidean_distance((x, y), c.pos) >= MIN_COVER_SPACING for c in placed)

def make_cover_layout(n_per_side: int, include_center: bool,
                       seed: int | None = None) -> list[CoverObject]:
    
    if n_per_side % 2 != 0:
        raise ValueError

    rng = random.Random(seed)
    cover_objects: list[CoverObject] = []
    rolls_needed = n_per_side // 2
    counter = 0

    for _ in range(rolls_needed):
        for attempt in range(MAX_PLACEMENT_ATTEMPTS):
            x = rng.uniform(COVER_X_MIN, CENTER_X - 0.5)
            y = rng.uniform(COVER_Y_MARGIN, CENTER_Y - 0.5)
            mirror_x = GRID_WIDTH - x
            mirror_y = GRID_HEIGHT - y
            if _far_enough(x, y, cover_objects) and _far_enough(x, mirror_y, cover_objects):
                break # TODO: decide what to do if max placement attempts is exceeded, currently still places regardless

        counter += 1
        cover_objects.append(CoverObject(f"Cover{counter}A_top", (x, y), COVER_DAMAGE_REDUCTION, 25000))
        cover_objects.append(CoverObject(f"Cover{counter}A_bot", (x, mirror_y), COVER_DAMAGE_REDUCTION, 25000))
        cover_objects.append(CoverObject(f"Cover{counter}B_top", (mirror_x, y), COVER_DAMAGE_REDUCTION, 25000))
        cover_objects.append(CoverObject(f"Cover{counter}B_bot", (mirror_x, mirror_y), COVER_DAMAGE_REDUCTION, 25000)) 

    if include_center:
        cover_objects.append(CoverObject("CoverMid", (CENTER_X, CENTER_Y), COVER_DAMAGE_REDUCTION, 50000))

    return cover_objects




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