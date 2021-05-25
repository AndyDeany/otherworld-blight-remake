from lib.surfaces import Image


class Hud:
    """Class for representing the player's HUD (Heads Up Display)."""

    HUD = Image("hud/hud.png", (0, 0))
    HEALTH_ORB = Image("hud/health_orb.png")
    EXP_BAR = Image("hud/expbar.png")
    EXP_BACK = Image("hud/expback.png", (0, 0))

    def display(self, spells, inventory, player):
        """Display the HUD."""
        self.EXP_BACK.display()
        self.EXP_BAR.display(728, 951, area=(0, 0, (player.exp / 100.0) * 467, 130))
        self.HUD.display()
        self.HEALTH_ORB.display(1025, 994 + (1 - (player.current_life / player.max_life)) * 87,
                                area=(0, (1 - (player.current_life / player.max_life)) * 87,
                                      123, (player.current_life / player.max_life) * 87))

        for index, spell in enumerate(spells):
            if spell.cooldown > 0:
                icon_image = spell.icon_cooldown_image
            else:
                icon_image = spell.icon_image
            icon_image.display(760 + 51 * index, 1029)

        for index, item in enumerate(inventory):
            item.display(964 + 51 * index, 1029)
