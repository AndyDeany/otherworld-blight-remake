class Item:
    """Class for representing an item that can be picked up by the player."""

    def __init__(self, name, image, loot_image=None):
        """Create an Item instance."""
        self.name = name
        self.image = image
        self.display = self.image.display
        self.loot_image = loot_image
