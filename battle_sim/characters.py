#The Character data model - just stats and state, no combat logic here.

from dataclasses import dataclass, field


@dataclass
class Character:
    name: str
    max_hp: int
    atk: int
    defense: int
    spd: int
    atk_range: float
    role: str = "striker"       # tank, striker, support, healer
    pos: tuple[float, float] = (0.0, 0.0)
    side: str = ""              # "A" or "B", set by assign_positions
    hp: int = field(init=False)
    isMoving: bool = False
    atb: float = field(init=False, default=0.0)

    def __post_init__(self):
        self.hp = self.max_hp

    @property
    def is_alive(self) -> bool:
        return self.hp > 0

    def take_damage(self, amount: int):
        self.hp = max(0, self.hp - amount)