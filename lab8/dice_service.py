import random

class DiceService:
    def roll_d20(self) -> int:
        return random.randint(1, 20)

    def roll_dice(self, dice_str: str) -> int:
        parts = dice_str.lower().split('d')
        if len(parts) != 2:
            raise ValueError(f"Invalid dice format: {dice_str}")
        count = int(parts[0]) if parts[0] else 1
        sides = int(parts[1])
        if count <= 0 or sides <= 0:
            raise ValueError("Dice count and sides must be positive")
        return sum(random.randint(1, sides) for _ in range(count))

    def roll_with_advantage(self) -> int:
        r1 = self.roll_d20()
        r2 = self.roll_d20()
        return max(r1, r2)
