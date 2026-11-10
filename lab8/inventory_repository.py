from typing import Dict, Optional
from lab8.models import Character, Item

class InventoryRepository:
    def __init__(self):
        self._storage: Dict[str, Character] = {}

    def save_character(self, character: Character) -> bool:
        if not character or not character.name:
            raise ValueError("Invalid character")
        self._storage[character.name] = character
        return True

    def get_character(self, name: str) -> Optional[Character]:
        return self._storage.get(name)

    def add_item_to_character(self, character_name: str, item: Item) -> bool:
        char = self.get_character(character_name)
        if not char:
            raise KeyError(f"Character {character_name} not found")
        char.inventory.append(item)
        return True

    def delete_character(self, name: str) -> bool:
        if name in self._storage:
            del self._storage[name]
            return True
        return False
