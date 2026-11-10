from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class Item:
    name: str
    weight: float
    cost_gp: int

    def __post_init__(self):
        if self.weight < 0:
            raise ValueError("Item weight cannot be negative")
        if self.cost_gp < 0:
            raise ValueError("Item cost cannot be negative")

@dataclass
class Weapon(Item):
    damage_dice: str = "1d6"
    damage_type: str = "slashing"

@dataclass
class Character:
    name: str
    char_class: str
    level: int
    strength: int
    dexterity: int
    constitution: int
    max_hp: int
    current_hp: int
    inventory: List[Item] = field(default_factory=list)
    equipped_weapon: Optional[Weapon] = None

    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("Character name cannot be empty")
        if self.level < 1 or self.level > 20:
            raise ValueError("Level must be between 1 and 20")
        for stat in [self.strength, self.dexterity, self.constitution]:
            if stat < 1 or stat > 30:
                raise ValueError("Ability scores must be between 1 and 30")
        if self.max_hp <= 0:
            raise ValueError("Max HP must be positive")
        if self.current_hp < 0 or self.current_hp > self.max_hp:
            raise ValueError("Current HP must be within 0 and max_hp")

    @property
    def strength_modifier(self) -> int:
        return (self.strength - 10) // 2

    @property
    def dexterity_modifier(self) -> int:
        return (self.dexterity - 10) // 2

    @property
    def constitution_modifier(self) -> int:
        return (self.constitution - 10) // 2

    @property
    def carrying_capacity(self) -> float:
        return float(self.strength * 15)

    @property
    def total_weight(self) -> float:
        weapon_w = self.equipped_weapon.weight if self.equipped_weapon else 0.0
        return sum(item.weight for item in self.inventory) + weapon_w

    def is_encumbered(self) -> bool:
        return self.total_weight > self.carrying_capacity

    def take_damage(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("Damage cannot be negative")
        self.current_hp = max(0, self.current_hp - amount)
        return self.current_hp

    def heal(self, amount: int) -> int:
        if amount < 0:
            raise ValueError("Heal cannot be negative")
        if self.current_hp == 0:
            raise ValueError("Cannot heal dead character with normal heal")
        self.current_hp = min(self.max_hp, self.current_hp + amount)
        return self.current_hp
