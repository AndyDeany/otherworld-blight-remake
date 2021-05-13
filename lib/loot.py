from lib.base import Base
from lib.surfaces import Image


class Loot(Base):
    """Class for repesenting a loot capsule."""

    SIZE = 6
    loot_images = {
        "controls": Image("loot/controls.png"),
        "loot0": Image("loot/loot0.png"),
        "loot1": Image("loot/loot1.png"),
        "loot2": Image("loot/loot2.png"),
        "loot3": Image("loot/loot3.png"),
        "loot4": Image("loot/loot4.png"),
        "loot5": Image("loot/loot5.png"),
        "slime_chunk": Image("loot/slime_chunk.png"),
    }

    def __init__(self, *items):
        self.items = list(items) + [None for _ in range(self.SIZE - len(items))]
        self._selected_slot = 0
        self.is_displaying = False

    def __bool__(self):
        return any((item is not None for item in self.items))

    def display(self, inventory):
        """returns False when the loot menu is closed"""
        if self.session.keys.escape or self.session.keys.backspace:
            return False

        self.loot_images["loot" + str(self._selected_slot)].display(0, 0)

        for index, item in enumerate(self.items):
            if item is not None:
                self.loot_images[item].display(781, 225 + 89*index)

        self.loot_images["controls"].display(0, 0)

        if (self.session.keys.up_arrow or self.session.keys.w) and self._selected_slot > 0:
            self._selected_slot -= 1
        if (self.session.keys.down_arrow or self.session.keys.s) and self._selected_slot < 5:
            self._selected_slot += 1

        if self.session.keys.enter:
            self.take_item(self._selected_slot, inventory)
        if self.session.keys.e:
            for slot in range(self.SIZE):
                self.take_item(slot, inventory)

        return True

    def take_item(self, slot, inventory):
        """Add the item in the given slot to the player's inventory."""
        if self.items[slot] is not None:
            inventory.append(self.items[slot])
            self.items[slot] = None
