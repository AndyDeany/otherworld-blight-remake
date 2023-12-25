import pygame

from lib.surfaces import Text


class NumberDropper:
    """Class for creating and displaying number drops."""

    def __init__(self, ):
        self.drops = []

    def create(self, drop_type, character, value):
        """Create a new number drop."""
        self.drops.append(NumberDrop(drop_type, character, value))

    def logic(self):
        """Run the logic for handling number drops."""
        self.display()
        self.drops = [drop for drop in self.drops if not drop.is_finished]

    def display(self):
        """Display all currently active number drops."""
        for drop in self.drops:
            drop.display()


class NumberDrop:
    """Class for representing a number drop (exp, damage, healing)."""

    TYPE_DAMAGE = "damage"
    TYPE_HEALING = "healing"
    TYPE_EXP = "exp"

    FONT = pygame.font.SysFont("Impact", 20, False, False)
    COLORS = {
        TYPE_DAMAGE: (255, 0, 0),
        TYPE_HEALING: (43, 255, 0),
        TYPE_EXP: (255, 215, 0),
    }

    TRAVEL_DISTANCE_PER_FRAME = 3
    TOTAL_TRAVEL_DISTANCE = 90

    def __init__(self, drop_type, character, value):
        self.x = character.x + character.width // 2
        self.y = character.y + character.height // 2
        self.start_y = self.y
        self.text = Text(value, self.FONT, self.COLORS[drop_type])
        self.is_finished = False

    def display(self):
        """Display the number drop."""
        self.text.display(self.x, self.y)
        self.y -= self.TRAVEL_DISTANCE_PER_FRAME
        self.is_finished = self.start_y - self.y >= self.TOTAL_TRAVEL_DISTANCE
