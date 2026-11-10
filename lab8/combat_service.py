from typing import Tuple
from lab8.models import Character
from lab8.dice_service import DiceService
from lab8.inventory_repository import InventoryRepository

class CombatService:
    def __init__(self, dice_service: DiceService, repository: InventoryRepository):
        self.dice_service = dice_service
        self.repository = repository

    def execute_attack(self, attacker: Character, target: Character, target_ac: int) -> Tuple[bool, int]:
        if attacker.current_hp <= 0:
            raise ValueError("Dead attacker cannot attack")
        if target.current_hp <= 0:
            raise ValueError("Target is already dead")

        roll = self.dice_service.roll_d20()
        total_to_hit = roll + attacker.strength_modifier

        if roll == 20 or (roll != 1 and total_to_hit >= target_ac):
            weapon_dice = attacker.equipped_weapon.damage_dice if attacker.equipped_weapon else "1d4"
            base_damage = self.dice_service.roll_dice(weapon_dice)
            if roll == 20:
                base_damage += self.dice_service.roll_dice(weapon_dice)
            damage = max(1, base_damage + attacker.strength_modifier)
            target.take_damage(damage)
            self.repository.save_character(target)
            return True, damage

        return False, 0

    def rest_character(self, character_name: str) -> int:
        char = self.repository.get_character(character_name)
        if not char:
            raise KeyError(f"Character {character_name} not found")
        hit_dice_value = self.dice_service.roll_dice("1d8")
        healed_hp = char.heal(hit_dice_value + char.constitution_modifier)
        self.repository.save_character(char)
        return healed_hp
