import pytest
from unittest.mock import Mock, MagicMock
from lab8.models import Character, Item, Weapon
from lab8.dice_service import DiceService
from lab8.inventory_repository import InventoryRepository
from lab8.combat_service import CombatService

@pytest.fixture
def sample_hero():
    return Character(
        name="Артур",
        char_class="Воин",
        level=3,
        strength=16,
        dexterity=14,
        constitution=14,
        max_hp=30,
        current_hp=30,
        equipped_weapon=Weapon(name="Длинный меч", weight=3.0, cost_gp=15, damage_dice="1d8")
    )

@pytest.fixture
def sample_monster():
    return Character(
        name="Гоблин",
        char_class="Монстр",
        level=1,
        strength=8,
        dexterity=14,
        constitution=10,
        max_hp=12,
        current_hp=12
    )

def test_character_strength_modifier(sample_hero):
    assert sample_hero.strength_modifier == 3

def test_character_invalid_empty_name():
    with pytest.raises(ValueError, match="Character name cannot be empty"):
        Character("   ", "Воин", 1, 10, 10, 10, 10, 10)

def test_character_invalid_level():
    with pytest.raises(ValueError, match="Level must be between 1 and 20"):
        Character("Маг", "Волшебник", 25, 10, 10, 10, 10, 10)

def test_character_invalid_hp_range():
    with pytest.raises(ValueError, match="Current HP must be within 0 and max_hp"):
        Character("Лучник", "Следопыт", 1, 10, 14, 12, 10, 15)

def test_carrying_capacity_and_encumbrance(sample_hero):
    assert sample_hero.carrying_capacity == 240.0
    assert not sample_hero.is_encumbered()
    heavy_chest = Item(name="Сундук с золотом", weight=250.0, cost_gp=1000)
    sample_hero.inventory.append(heavy_chest)
    assert sample_hero.is_encumbered()

def test_item_negative_weight():
    with pytest.raises(ValueError, match="Item weight cannot be negative"):
        Item("Сломанный кинжал", -1.5, 5)

def test_take_damage_normal_and_lethal(sample_monster):
    sample_monster.take_damage(5)
    assert sample_monster.current_hp == 7
    sample_monster.take_damage(100)
    assert sample_monster.current_hp == 0

def test_heal_character(sample_hero):
    sample_hero.take_damage(20)
    assert sample_hero.current_hp == 10
    sample_hero.heal(15)
    assert sample_hero.current_hp == 25
    sample_hero.heal(50)
    assert sample_hero.current_hp == 30

def test_heal_dead_character_raises_exception(sample_hero):
    sample_hero.take_damage(30)
    assert sample_hero.current_hp == 0
    with pytest.raises(ValueError, match="Cannot heal dead character with normal heal"):
        sample_hero.heal(10)

def test_dice_service_roll_dice_valid():
    dice = DiceService()
    result = dice.roll_dice("2d6")
    assert 2 <= result <= 12

def test_dice_service_invalid_format():
    dice = DiceService()
    with pytest.raises(ValueError):
        dice.roll_dice("bad_dice_str")

def test_combat_successful_hit_with_dice_stub(sample_hero, sample_monster):
    dice_stub = Mock(spec=DiceService)
    dice_stub.roll_d20.return_value = 15
    dice_stub.roll_dice.return_value = 6
    repo_stub = Mock(spec=InventoryRepository)

    combat = CombatService(dice_service=dice_stub, repository=repo_stub)
    hit, damage = combat.execute_attack(sample_hero, sample_monster, target_ac=15)

    assert hit is True
    assert damage == 9
    assert sample_monster.current_hp == 3
    repo_stub.save_character.assert_called_once_with(sample_monster)

def test_combat_critical_hit_doubles_dice(sample_hero, sample_monster):
    dice_stub = Mock(spec=DiceService)
    dice_stub.roll_d20.return_value = 20
    dice_stub.roll_dice.side_effect = [7, 5]
    repo_mock = Mock(spec=InventoryRepository)

    combat = CombatService(dice_service=dice_stub, repository=repo_mock)
    hit, damage = combat.execute_attack(sample_hero, sample_monster, target_ac=30)

    assert hit is True
    assert damage == 15
    assert sample_monster.current_hp == 0
    repo_mock.save_character.assert_called_once()

def test_combat_miss_does_not_save_target(sample_hero, sample_monster):
    dice_stub = Mock(spec=DiceService)
    dice_stub.roll_d20.return_value = 2
    repo_spy = Mock(spec=InventoryRepository)

    combat = CombatService(dice_service=dice_stub, repository=repo_spy)
    hit, damage = combat.execute_attack(sample_hero, sample_monster, target_ac=18)

    assert hit is False
    assert damage == 0
    assert sample_monster.current_hp == 12
    repo_spy.save_character.assert_not_called()

def test_combat_service_rest_character(sample_hero):
    sample_hero.take_damage(15)
    repo_mock = Mock(spec=InventoryRepository)
    repo_mock.get_character.return_value = sample_hero
    dice_stub = Mock(spec=DiceService)
    dice_stub.roll_dice.return_value = 6

    combat = CombatService(dice_service=dice_stub, repository=repo_mock)
    new_hp = combat.rest_character("Артур")

    assert new_hp == 23
    repo_mock.get_character.assert_called_once_with("Артур")
    repo_mock.save_character.assert_called_once_with(sample_hero)
